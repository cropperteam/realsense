import pyrealsense2 as rs
import numpy as np
import cv2
import json
import csv
import os

# Initialize a list to store the data
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
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
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

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
screen_width = 640
screen_height = 480
capture_data = False
i = 8

# Create directories to save images and CSV files
os.makedirs("images", exist_ok=True)
os.makedirs("csv", exist_ok=True)

try:
    while True:
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        depth_image = cv2.resize(depth_image, (screen_width, screen_height))
        color_image = cv2.resize(color_image, (screen_width, screen_height))
        print(depth_image)
        depth_image_scaled = cv2.convertScaleAbs(depth_image, alpha=0.1)

        cv2.imshow("Bgr frame", color_image)
        cv2.imshow("Depth frame", depth_image_scaled)

        key = cv2.waitKey(1)

        # Press 's' to capture and store data
        if key == ord('s'):
            capture_data = True
            # Store color frame and its corresponding depth image
            cv2.imwrite(f'images/color_image{i}.png', color_image)
            cv2.imwrite(f'images/depth_image{i}.png', depth_image_scaled)
            # Save depth data to CSV
            print(depth_image_scaled)
            with open(f'csv/depth_data{i}.csv', 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(depth_image_scaled.tolist())
            i += 1

        # Press 'q' to terminate the program
        if key & 0xFF == ord('q') or key == 27:
            break

finally:
    # Stop the pipeline and close windows
    pipeline.stop()
    cv2.destroyAllWindows()
