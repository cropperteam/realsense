# Live Testing

This folder contains a Python script for live testing using an Intel RealSense Depth 435i Camera. The script captures live feed, processes the frames with a YOLOv8 segmentation model, and calculates the real-world coordinates and depth of detected objects.

## live_testing.py

This script combines live feed capture, object detection, and depth extraction into one comprehensive workflow. It uses a YOLOv8 custom-trained segmentation model to detect objects in the captured frames and computes the real-world coordinates of the objects' centers.

### Features

1. Captures live feed from the Intel RealSense Depth 435i Camera.
2. Processes frames with a YOLOv8 segmentation model to detect objects.
3. Calculates the center point of detected segments.
4. Extracts the depth information for the center point.
5. Uses trigonometry to compute real-world coordinates (real_x, real_y) based on the depth and camera field of view.
6. Annotates the frame with detected objects' IDs, real-world coordinates, and depth.
7. Saves the annotated frame and a corresponding text file with the detection details when a key is pressed.

### Usage

1. Ensure the Intel RealSense camera is connected to your system.
2. Install the required dependencies:
   ```bash
   pip install pyrealsense2 numpy opencv-python ultralytics
   ```
3. Run the script:
   ```bash
   python live_testing.py
   ```
4. Press 's' to process the current frame with the YOLOv8 model.
5. Press 'x' to save the annotated frame and the detection details to a text file.
6. Press 'q' or 'Esc' to quit the script.

### Dependencies

- pyrealsense2
- numpy
- opencv-python
- ultralytics

### File Structure

- `live_testing.py`: Main script for capturing, processing, and saving frames and detection details.
- `node_best_pt_seg.pt`: YOLOv8 custom-trained segmentation model (ensure this is in the same directory or provide the correct path).

### Example

When you run the script and press 's', the YOLOv8 model will process the current frame, and the detected objects will be annotated on the frame with their real-world coordinates and depth. Press 'x' to save the annotated frame and a text file with detection details.

### Note

- Ensure the YOLOv8 model file (`node_best_pt_seg.pt`) is correctly placed in the directory or update the script with the correct path.
- The script uses trigonometric calculations based on the camera's field of view and the detected depth to compute real-world coordinates. Adjust the calculations if you use a different camera or configuration.
```
