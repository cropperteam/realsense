# RealSense Depth Camera Project

This repository contains scripts for capturing and processing frames from an Intel RealSense Depth 435i Camera. The main functionalities include capturing RGB and depth images, extracting depth information at specific pixel points, and running live object detection with YOLOv8 segmentation.

## Repository Structure

- **capture_and_extract**
  - `capture.py`: Captures frames from the RealSense camera, saves RGB and depth images, and stores depth data in a CSV file.
  - `extract.py`: Extracts the depth value at a specific pixel point from the depth CSV file.
  - [README.md](capture_and_extract/README.md): Documentation for the capture and extract scripts.

- **live_testing**
  - `live_testing.py`: Combines live feed capture, YOLOv8 object detection, and depth extraction in one script.
  - [README.md](live_testing/README.md): Documentation for the live testing script.

- **installation_guide**
  - `installLibrealsense.sh`: Script to install librealsense from the Intel Debian repository.
  - `buildLibrealsense.sh`: Script to build librealsense from source.
  - [README.md](installation_guide/README.md): Guide to install librealsense on Jetson devices.

## Getting Started

### Prerequisites

- Intel RealSense Depth 435i Camera
- NVIDIA Jetson Nano Developer Kit (for installation guide)

### Installation

Refer to the [Installation Guide](installation_guide/README.md) for detailed instructions on setting up librealsense on Jetson devices.

### Scripts Overview

1. **Capture and Extract**
   - Use `capture.py` to capture and save frames from the RealSense camera.
   - Use `extract.py` to extract depth information at specific pixel points.
   - Detailed usage is provided in the [Capture and Extract README](capture_and_extract/README.md).

2. **Live Testing**
   - Use `live_testing.py` for live object detection and depth extraction.
   - Detailed usage is provided in the [Live Testing README](live_testing/README.md).

### File Structure

```
RealSense_Depth_Camera_Project/
├── capture_and_extract/
│   ├── capture.py
│   ├── extract.py
│   ├── README.md
├── live_testing/
│   ├── live_testing.py
│   ├── README.md
├── installation_guide/
│   ├── installLibrealsense.sh
│   ├── buildLibrealsense.sh
│   ├── README.md
├── node_best_pt_seg.pt
└── main_README.md
```

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.
```


## Jetson Installation Guide

For instructions on installing librealsense on Jetson devices, refer to the [Jetson Installation Guide](./jetson_installation/Jetson_Installation_Guide.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or support, please open an issue in this repository.

---
