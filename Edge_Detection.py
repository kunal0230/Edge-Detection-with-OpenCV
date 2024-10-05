import cv2
import numpy as np

# Step 1: Load the image
image = cv2.imread('x.jpg')

# Step 2: Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 3: Apply Gaussian Blur to reduce noise and improve edge detection
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Step 4: Perform Canny edge detection
edges = cv2.Canny(blurred_image, 100, 200)

# Step 5: Create a comparison image by stacking the original and processed images horizontally
edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)  # Convert edge-detected to BGR for comparison
comparison_image = np.hstack((image, edges_bgr))

# Step 6: Save the processed and comparison images
cv2.imwrite("edge_detected_image.jpg", edges)
cv2.imwrite("comparison_image.jpg", comparison_image)

# (Optional) Display the images
cv2.imshow("Edge Detected Image", edges)
cv2.imshow("Comparison Image", comparison_image)

# Step 7: Wait for a key press (e.g., 'q') to close the program
print("Press 'q' to close the windows.")

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

# Cleanup: Close all windows properly
cv2.destroyAllWindows()
