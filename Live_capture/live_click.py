# Code to Test on live using Intel Realsense Depth 435i Camera

#Libraries Required
import pyrealsense2 as rs
import numpy as np
import cv2
import os
import math
from ultralytics import YOLO


# Function to get the depth of point based on its pixel value.
def get_depth_for_pixel(pixel_x, pixel_y, depth_frame, depth_intrin, color_intrin, depth_to_color_extrin):
    # 1. Deproject the RGB pixel coordinate to a point in 3D space
    undistorted = rs.rs2_deproject_pixel_to_point(color_intrin, [pixel_x, pixel_y], 1.0)

    # 2. Transform the point from the color camera coordinate system to the depth camera coordinate system
    transformed = rs.rs2_transform_point_to_point(depth_to_color_extrin, undistorted)

    # 3. Project the point from the depth camera coordinate system to the depth camera image plane
    depth_pixel = rs.rs2_project_point_to_pixel(depth_intrin, transformed)
    depth_pixel = [int(depth_pixel[0]), int(depth_pixel[1])]

    # 4. Retrieve the depth value if the depth pixel coordinate is within the valid range
    if (0 <= depth_pixel[0] < depth_intrin.width and
        0 <= depth_pixel[1] < depth_intrin.height):
        dist_to_center = depth_frame.get_distance(depth_pixel[0], depth_pixel[1])
        return dist_to_center
    else:
        return None

# Load your YOLOv8 model
model = YOLO('node_best_pt_seg.pt')
model.to("cuda")



# Pipeline setup for Realsense Camera
pipeline = rs.pipeline()
config = rs.config()

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))
found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

# Get the depth stream configurations
depth_sensor = device.query_sensors()[0]
depth_stream_profiles = [s.as_video_stream_profile() for s in depth_sensor.profiles if s.stream_type() == rs.stream.depth and s.format() == rs.format.z16]

if not depth_stream_profiles:
    print("No valid depth stream profiles found")
    exit(1)

depth_resolutions = [s.intrinsics for s in depth_stream_profiles]
max_depth_resolution = max(depth_resolutions, key=lambda res: res.width * res.height)

# Get the RGB stream configurations
rgb_sensor = device.query_sensors()[1]
rgb_stream_profiles = [s.as_video_stream_profile() for s in rgb_sensor.profiles if s.stream_type() == rs.stream.color and s.format() == rs.format.bgr8]

if not rgb_stream_profiles:
    print("No valid RGB stream profiles found")
    exit(1)

rgb_resolutions = [s.intrinsics for s in rgb_stream_profiles]
max_rgb_resolution = max(rgb_resolutions, key=lambda res: res.width * res.height)

# Enable the maximum available resolution for both streams
config.enable_stream(rs.stream.depth, max_depth_resolution.width, max_depth_resolution.height, rs.format.z16, 30)
config.enable_stream(rs.stream.color, max_rgb_resolution.width, max_rgb_resolution.height, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: ", depth_scale)

# Create an align object
align_to = rs.stream.color
align = rs.align(align_to)

# Initialize variables for capturing data
screen_width = max_rgb_resolution.width
screen_height = max_rgb_resolution.height
capture_data = False
i = 2

# Create directories to save images and txt files
os.makedirs("images_final_11_06", exist_ok=True)
os.makedirs("txt_final_11_06", exist_ok=True)

try:
    while True:
        # Capturing Frames 
        
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        depth_image = cv2.resize(depth_image, (screen_width, screen_height))
        color_image = cv2.resize(color_image, (screen_width, screen_height))

        depth_image_scaled = cv2.convertScaleAbs(depth_image, alpha=0.1)

        cv2.imshow("Bgr frame", color_image)
        # cv2.imshow("Depth frame", depth_image_scaled)

        key = cv2.waitKey(1)
        
        # To Process the Frame through a model
        if key == ord('s'): #Keyboard Key Press
            capture_data = True
            results = model.track(source=color_image, stream=True,device=0) # Prediction on the image using segmented model

            # Processing the Results to extract data from it
            for result in results:
                if result.masks!=None and result.boxes!=None:      # If Results are empty then it will skip this part
                    tracked_mask = result.masks.xyn         # getting masks xy in nomalized form
                    tracked_boxes = result.boxes.data       # getting boxes data of a result (Boundary Box) 
                    object_data = []                

                    for j, mask in enumerate(tracked_mask):
                        # Calculate the centroid of the mask
                        x_coords = mask[:, 0]       
                        y_coords = mask[:, 1]
                        cx = int(np.mean(x_coords) * screen_width)  #Center point x of a mask
                        cy = int(np.mean(y_coords) * screen_height) # Center point y of a mask
                        obj_id = int(tracked_boxes[j, 5])      
                        x=cx-960    #Calculating x with respect to center (Cartesian Rule)
                        y=540-cy    #Calculating y with respect to center (Catestian Rule)
                        
                        #Calculating angles to find the real_x and real_y (Resolution 1920*1080)
                        angle_x=x*0.0359375         
                        angle_y=y*0.03888888888888888888888888888889


                        depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
                        color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
                        depth_to_color_extrin = aligned_depth_frame.profile.get_extrinsics_to(color_frame.profile)

                        # Find the depth of that pixel
                        depth_value = get_depth_for_pixel(cx, cy, aligned_depth_frame, depth_intrin, color_intrin, depth_to_color_extrin)
                        
                        if depth_value is None:
                            continue
                        
                        # Converting the depth value in cm from meter
                        depth_value=depth_value*100    

                        #Calculating Real_x and Real_y
                        real_x = math.tan(math.radians(angle_x))*depth_value
                        l = math.sqrt(math.pow(depth_value, 2) + math.pow(real_x, 2))
                        real_y = math.tan(math.radians(angle_y))*l
                        object_data.append([obj_id, cx, cy,real_x,real_y, depth_value])
                        

                        #Displaying Data on the Image
                        label = f"ID: {obj_id}, {real_x:.2f}, {real_y:.2f} , Depth: {depth_value:.2f} cm "
                        image = cv2.circle(color_image, (cx, cy), radius=10, color=(0, 0, 255), thickness=-1)
                        color_image = cv2.putText(color_image, label, (cx, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 1)
                        color_image = cv2.circle(color_image, (960, 540), radius=5, color=(0, 0, 0), thickness=-1)
                    
                    cv2.imshow("Annotated Frame", color_image)

                    key = cv2.waitKey(0)
                    
                    # if we press X on keyboard it will save that frame and continue displaying the Feed of the camera
                    if key == ord('x'):
                        cv2.imwrite(f'images_final/annotated_image{i}.png', color_image)

                        txt_file_path = f'csv_final/object_data{i}.txt'
                        with open(txt_file_path, 'w') as txt_file:
                            for obj_data in object_data:
                                txt_file.write(f"id - {obj_data[0]}, cx - {obj_data[1]}px, cy - {obj_data[2]}px, real_x - {obj_data[3]}cm, real_y - {obj_data[4]}cm, depth - {obj_data[5]}cm\n")

                        i += 1
                        cv2.destroyWindow("Annotated Frame")

        if key & 0xFF == ord('q') or key == 27:
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
