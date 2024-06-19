
### Installation Guide for Librealsense on Jetson Devices

This guide provides instructions to install Intel's librealsense on NVIDIA Jetson devices using scripts from the [JetsonHacksNano repository](https://github.com/JetsonHacksNano/installLibrealsense).

#### Prerequisites

- NVIDIA Jetson Nano Developer Kit
- Internet connection

#### Installation Options

There are two primary ways to install librealsense:

1. **Install from Intel Librealsense Debian Repository**:
    - This method does not require patching the kernel or modules.
    - Run the following command to install:
      ```bash
      ./installLibrealsense.sh
      ```

2. **Build Librealsense from Source**:
    - This method is useful if you need to compile from source.
    - Run the following command to build:
      ```bash
      ./buildLibrealsense.sh [ -v | --version <version> ] [ -j | -jobs <number of jobs> ] [ -n | --no_cuda ]
      ```
    - Options:
      - `<version>`: Specify the version of librealsense (e.g., v2.49.0).
      - `<number of jobs>`: Specify the number of jobs to run concurrently when building. Defaults to 1 if the Jetson has ≤ 4GB memory.
      - `<no_cuda>`: Compile without CUDA support. Defaults to using CUDA.

#### Notes

- The current recommendation from Intel is to use UVC for video input on Jetson devices.
- If using `realsense-ros`, ensure the versions of librealsense and realsense-ros are compatible.
- Refer to the [installation_jetson.md](https://github.com/IntelRealSense/librealsense/blob/master/doc/installation_jetson.md) for more advanced configurations and communication interfaces.

---
