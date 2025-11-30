# CCTV Webcam Capture

A Python script and web interface for capturing frames from USB webcams with adjustable brightness, contrast, and night mode support.

## Features

- 📷 **Frame Capture**: Capture multiple frames from USB cameras
- 🎚️ **Brightness & Contrast Control**: Adjust image processing parameters
- 🌙 **Night Mode**: Low-light mode with black & white conversion, high exposure, and high gain
- 🎬 **MJPEG Support**: Efficient MJPEG codec for better compatibility
- 📁 **Flexible Output**: Save frames to custom directories
- 🌐 **Web Interface**: Stream camera live to browser with real-time controls
- 📱 **Remote Access**: Control camera from any device on your network

## Requirements

- Python 3.x
- OpenCV (cv2)
- A USB webcam with V4L2 support

### Install Dependencies

```bash
pip install opencv-python flask
```

## Usage

### Web Interface (Recommended)

Start the web server:

```bash
python webcam_server.py
```

Then open your browser to:
- **Local machine:** http://localhost:5000
- **Remote machine:** http://server_ip:5000

Features:
- 📹 Live camera stream
- 🎚️ Real-time brightness/contrast sliders
- 🌙 Night mode toggle
- 📸 Capture frames directly from browser
- 📊 FPS display

### Command-Line Interface

Capture 5 frames from device 0 (default):

```bash
sudo python webcam.py -n 5
```

### Brightness & Contrast Adjustment

Increase brightness by 20 and contrast to 1.5:

```bash
sudo python webcam.py -n 10 -b 20 -c 1.5
```

### Night Mode

Enable night mode (black & white, high exposure, high gain):

```bash
sudo python webcam.py --night -n 5
```

You can still adjust brightness/contrast in night mode:

```bash
sudo python webcam.py --night -n 5 -b -10 -c 1.2
```

### Custom Output Directory

```bash
sudo python webcam.py -n 10 -o ./frames_custom
```

### Custom Camera Device & Resolution

```bash
sudo python webcam.py -d 1 --width 1920 --height 1080 -n 5
```

## Command-Line Arguments

```
-d, --device          Camera device index (default: 0) or URL
--width               Frame width in pixels (default: 1280)
--height              Frame height in pixels (default: 720)
-o, --output          Output directory (default: ./frames)
-n, --num-frames      Number of frames to capture (default: 10)
-b, --brightness      Brightness adjustment -50 to 50 (default: 0)
-c, --contrast        Contrast adjustment 0.5 to 2.0 (default: 1.0)
--night               Enable night mode (B&W, high exposure/gain)
-h, --help            Show help message
```

## Examples

### Capture 20 frames in normal mode
```bash
sudo python webcam.py -n 20
```

### Capture 15 frames in night mode with reduced brightness
```bash
sudo python webcam.py --night -n 15 -b -5 -o ./frames_night
```

### Capture from device 1 with high contrast
```bash
sudo python webcam.py -d 1 -n 8 -c 1.8
```

### Capture at 1920x1080 resolution
```bash
sudo python webcam.py --width 1920 --height 1080 -n 5
```

## Output

Frames are saved as JPEG files with sequential numbering:
- `frame_0000.jpg`
- `frame_0001.jpg`
- `frame_0002.jpg`
- etc.

Output format: (720, 1280, 3) for default resolution (BxW x Height x Channels)

## Troubleshooting

### Permission Denied

The script requires access to `/dev/video*` devices. Use `sudo` to run:

```bash
sudo python webcam.py
```

If you want to avoid sudo, add your user to the video group:

```bash
sudo usermod -aG video $USER
# Then log out and back in
```

### Camera Not Found

Check available cameras:

```bash
sudo v4l2-ctl --list-devices
```

Use the appropriate device number with `-d` flag.

### Frames Too Bright/Dark

Adjust brightness and contrast:

```bash
# Too bright: reduce brightness
sudo python webcam.py -b -20 -c 1.0

# Too dark: increase brightness
sudo python webcam.py -b 20 -c 1.3
```

### Night Mode Too Washed Out

Reduce brightness when using night mode:

```bash
sudo python webcam.py --night -b -10 -c 1.1
```

## Camera Support

Tested with:
- JOYACCESS JA-Webcam (USB)

Should work with any V4L2-compatible USB camera.

## License

MIT
