#!/usr/bin/env python3
"""Test which camera devices are available."""
import cv2
import sys

print("Testing camera devices...\n")

for device_id in range(4):  # Test devices 0-3
    print(f"Testing /dev/video{device_id}...", end=" ")
    cap = cv2.VideoCapture(device_id)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✓ SUCCESS! Frame shape: {frame.shape}")
        else:
            print("✗ Failed to read frame")
        cap.release()
    else:
        print("✗ Failed to open")

print("\n" + "="*50)
print("To use a camera in the notebook, update the default device:")
print("  Change: default=\"1\"")
print("  To: default=\"X\"  (where X is the working device)")
print("="*50)
