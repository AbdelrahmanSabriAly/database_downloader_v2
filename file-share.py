import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import numpy as np


def process_image(image_data):
    # Convert the image data to a numpy array
    img_array = np.array(Image.open(image_data))

    # Process the image using OpenCV
    # Example: Convert the image to grayscale
    gray_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

    # Example: Apply a Gaussian blur to the image
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Example: Perform edge detection using the Canny edge detector
    edges = cv2.Canny(blurred_image, 50, 150)

    # Convert the processed image back to PIL Image format
    processed_image = Image.fromarray(edges)

    # Display the processed image
    st.image(processed_image)

with st.form("Attendance"):
    components.html(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                body{
                    color: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
            </style>
        </head>
        <body>
            <input type="file" accept="image/*" capture="camera" name="photo" id="photo" required>
            <button type="submit" id="submit-btn" style="display: none;"></button>
        </body>
        <script>
        document.getElementById('photo').addEventListener('change', function() {
            document.getElementById('submit-btn').click();
        });
        </script>
        </html>
        """
    )


    submitted = st.form_submit_button("Submit")

    # Process the uploaded image if the form is submitted
    if submitted:
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image_data = uploaded_file.read()
            # Call the process_image function to process the image
            process_image(image_data)