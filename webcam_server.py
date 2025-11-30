#!/usr/bin/env python3
"""
Web-based camera streaming server with live controls.
Access at http://localhost:5000
"""
import cv2
import threading
import time
from flask import Flask, render_template, jsonify, request
from pathlib import Path

app = Flask(__name__)

# Global camera state
camera_state = {
    'brightness': 0,
    'contrast': 1.0,
    'night_mode': False,
    'frame': None,
    'lock': threading.Lock(),
    'running': True,
    'fps': 0,
    'frame_count': 0,
}

def capture_frames():
    """Background thread for camera capture"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open camera")
        return
    
    # Camera settings
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # Warm up camera
    print("Warming up camera...")
    time.sleep(2)
    for _ in range(5):
        cap.read()
        time.sleep(0.2)
    
    print("Camera ready! Streaming...")
    
    last_time = time.time()
    
    while camera_state['running']:
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Apply night mode if enabled
        if camera_state['night_mode']:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            cap.set(cv2.CAP_PROP_EXPOSURE, -8)
            cap.set(cv2.CAP_PROP_GAIN, 40)
            cap.set(cv2.CAP_PROP_BRIGHTNESS, 20)
            brightness = -5
            contrast = 1.3
        else:
            cap.set(cv2.CAP_PROP_EXPOSURE, -1)
            cap.set(cv2.CAP_PROP_GAIN, 0)
            brightness = camera_state['brightness']
            contrast = camera_state['contrast']
        
        # Apply brightness/contrast
        adjusted = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness * 2)
        
        # Convert to JPEG
        ret, buffer = cv2.imencode('.jpg', adjusted, [cv2.IMWRITE_JPEG_QUALITY, 80])
        frame_bytes = buffer.tobytes()
        
        with camera_state['lock']:
            camera_state['frame'] = frame_bytes
            camera_state['frame_count'] += 1
            
            # Calculate FPS
            current_time = time.time()
            if current_time - last_time >= 1.0:
                camera_state['fps'] = camera_state['frame_count']
                camera_state['frame_count'] = 0
                last_time = current_time
    
    cap.release()
    print("Camera closed")

def generate_frames():
    """Generator for streaming frames"""
    while camera_state['running']:
        with camera_state['lock']:
            frame = camera_state['frame']
        
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n'
                   b'Content-Length: ' + str(len(frame)).encode() + b'\r\n\r\n'
                   + frame + b'\r\n')
        else:
            time.sleep(0.01)

@app.route('/')
def index():
    """Serve the web interface"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Stream video frames"""
    return app.response_class(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/api/state', methods=['GET'])
def get_state():
    """Get current camera state"""
    with camera_state['lock']:
        return jsonify({
            'brightness': camera_state['brightness'],
            'contrast': camera_state['contrast'],
            'night_mode': camera_state['night_mode'],
            'fps': camera_state['fps'],
        })

@app.route('/api/brightness', methods=['POST'])
def set_brightness():
    """Set brightness value"""
    data = request.get_json()
    value = int(data.get('value', 0))
    value = max(-50, min(50, value))  # Clamp to -50..50
    camera_state['brightness'] = value
    return jsonify({'brightness': camera_state['brightness']})

@app.route('/api/contrast', methods=['POST'])
def set_contrast():
    """Set contrast value"""
    data = request.get_json()
    value = float(data.get('value', 1.0))
    value = max(0.5, min(2.0, value))  # Clamp to 0.5..2.0
    camera_state['contrast'] = value
    return jsonify({'contrast': camera_state['contrast']})

@app.route('/api/night_mode', methods=['POST'])
def toggle_night_mode():
    """Toggle night mode"""
    data = request.get_json()
    camera_state['night_mode'] = data.get('enabled', False)
    return jsonify({'night_mode': camera_state['night_mode']})

@app.route('/api/capture', methods=['POST'])
def capture_image():
    """Capture current frame to file"""
    data = request.get_json()
    output_dir = Path(data.get('output_dir', './frames'))
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with camera_state['lock']:
        frame = camera_state['frame']
    
    if frame:
        # Find next filename
        existing_files = list(output_dir.glob('frame_*.jpg'))
        next_num = len(existing_files)
        filename = output_dir / f'frame_{next_num:04d}.jpg'
        
        with open(filename, 'wb') as f:
            f.write(frame)
        
        return jsonify({
            'success': True,
            'filename': str(filename)
        })
    
    return jsonify({'success': False, 'error': 'No frame available'}), 500

if __name__ == '__main__':
    # Start camera capture thread
    camera_thread = threading.Thread(target=capture_frames, daemon=True)
    camera_thread.start()
    
    # Start Flask server
    print("Starting web server at http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
