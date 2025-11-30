import cv2
import argparse
import sys
import os
import time
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Capture camera frames with brightness/contrast adjustment"
    )
    parser.add_argument(
        "-d", "--device",
        default="0",
        help="Camera device index (e.g. 0, 1) or URL (RTSP/HTTP)."
    )
    parser.add_argument(
        "--width", type=int, default=1280,
        help="Requested frame width."
    )
    parser.add_argument(
        "--height", type=int, default=720,
        help="Requested frame height."
    )
    parser.add_argument(
        "-o", "--output",
        default="./frames",
        help="Output directory for captured frames."
    )
    parser.add_argument(
        "-n", "--num-frames", type=int, default=10,
        help="Number of frames to capture."
    )
    parser.add_argument(
        "-b", "--brightness", type=int, default=0,
        help="Brightness adjustment (-50 to 50)."
    )
    parser.add_argument(
        "-c", "--contrast", type=float, default=1.0,
        help="Contrast adjustment (0.5 to 2.0)."
    )
    parser.add_argument(
        "--night", action="store_true",
        help="Enable night mode (high exposure, high gain, black & white)."
    )
    
    # Filter out Jupyter kernel arguments before parsing
    args_to_parse = [arg for arg in sys.argv[1:] if not arg.startswith('--f=')]
    args = parser.parse_args(args_to_parse)

    # Device can be index or string (URL)
    try:
        dev = int(args.device)
    except ValueError:
        dev = args.device

    cap = cv2.VideoCapture(dev)
    if not cap.isOpened():
        raise SystemExit(f"Could not open camera: {args.device}")

    # Try to set resolution (may or may not be honored by driver)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    # Try MJPEG codec for better compatibility
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    # Reduce buffers to avoid latency
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # Night mode settings
    if args.night:
        print("  Night mode: enabled")
        cap.set(cv2.CAP_PROP_EXPOSURE, -8)  # Manual exposure, longer
        cap.set(cv2.CAP_PROP_GAIN, 40)      # Moderate gain
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 20)  # Reduced brightness
        args.brightness = -5   # Reduce brightness
        args.contrast = 1.3    # Moderate contrast
    
    # Allow camera to warm up
    print("Warming up camera...", end="", flush=True)
    time.sleep(2)
    for _ in range(5):
        cap.read()
        time.sleep(0.2)
    print(" ready!")

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Capturing {args.num_frames} frames from device {args.device}")
    print(f"Brightness: {args.brightness}, Contrast: {args.contrast}")
    print(f"Saving to: {output_dir.absolute()}\n")

    frame_count = 0
    failed_count = 0
    while frame_count < args.num_frames and failed_count < 3:
        ret, frame = cap.read()
        if not ret:
            print(f"  Warning: Failed to grab frame (attempt {failed_count + 1}/3)")
            failed_count += 1
            time.sleep(0.1)
            continue

        failed_count = 0  # Reset on successful read
        
        # Convert to grayscale in night mode
        if args.night:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # Convert back to 3-channel for consistency
        
        # Apply brightness/contrast adjustment
        # alpha = contrast, beta = brightness offset
        adjusted = cv2.convertScaleAbs(frame, alpha=args.contrast, beta=args.brightness * 2)

        # Save frame
        output_file = output_dir / f"frame_{frame_count:04d}.jpg"
        cv2.imwrite(str(output_file), adjusted)
        print(f"  [{frame_count + 1}/{args.num_frames}] Saved: {output_file.name} ({frame.shape})")
        
        frame_count += 1

    cap.release()
    print(f"\nDone! Captured {frame_count} frames to {output_dir.absolute()}")

if __name__ == "__main__":
    main()