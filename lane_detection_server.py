import os
import cv2
import numpy as np
import base64
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def region_of_interest(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def draw_lines(image, lines, color=(0, 255, 0), thickness=2):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), color, thickness)

def detect_lanes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    height, width = edges.shape
    roi_vertices = [(0, height), (width / 2, height / 2), (width, height)]
    roi = region_of_interest(edges, np.array([roi_vertices], np.int32))

    lines = cv2.HoughLinesP(roi, 1, np.pi / 180, threshold=50, minLineLength=100, maxLineGap=50)
    line_image = np.zeros_like(image)
    draw_lines(line_image, lines)

    #  "Good lane keeping"
    cv2.putText(line_image, 'Good lane keeping!!!', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # timestamp
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(line_image, current_datetime, (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    result = cv2.addWeighted(image, 0.8, line_image, 1, 0)
    return result

@app.route('/')
def index():
    return render_template('lane.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    frame_data = request.json.get('frame', None)
    if frame_data:
     
        frame_bytes = frame_data.split(',')[1].encode()
        nparr = np.frombuffer(base64.b64decode(frame_bytes), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        processed_frame = detect_lanes(frame)
        
        # output folder
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"output_{timestamp}.jpg"
        output_path = os.path.join(output_dir, output_filename)
        cv2.imwrite(output_path, processed_frame)
        
        #codec used
        out_video_path = os.path.join(output_dir, "output_video.mp4")
        if not os.path.exists(out_video_path):
            fps = 30  
            height, width, _ = frame.shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(out_video_path, fourcc, fps, (width, height))
        else:
            out = cv2.VideoWriter(out_video_path, fourcc, fps, (width, height), True)

        out.write(processed_frame)
        out.release()
        
        return jsonify({'success': True, 'output_video': out_video_path})
    else:
        return jsonify({'success': False, 'error': 'No frame data received'})

if __name__ == '__main__':
    app.run(debug=True)
