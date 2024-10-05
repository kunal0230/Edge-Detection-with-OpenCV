import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# Directory to save uploaded and processed images
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edge-detection')
def edge_detection():
    return render_template('edge_detection.html')



@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Save the uploaded image
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'original.jpg')
        file.save(file_path)

        # Process the image for edge detection
        process_image(file_path)

        return redirect(url_for('display_images'))

def process_image(image_path):
    # Read the uploaded image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Perform Canny edge detection
    edges = cv2.Canny(blurred_image, 100, 200)

    # Save the edge-detected image
    edge_path = os.path.join(app.config['UPLOAD_FOLDER'], 'edges.jpg')
    cv2.imwrite(edge_path, edges)

    # Create a comparison image (original and processed side by side)
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    comparison_image = np.hstack((image, edges_bgr))
    
    # Save the comparison image
    comparison_path = os.path.join(app.config['UPLOAD_FOLDER'], 'comparison.jpg')
    cv2.imwrite(comparison_path, comparison_image)

@app.route('/display')
def display_images():
    # Render the page to display the images and allow download
    return render_template('display.html')

@app.route('/download/<filename>')
def download_file(filename):
    # Allow the user to download images
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
