import streamlit as st
import numpy as np
import cv2
from PIL import Image
from io import BytesIO

def simple_background_remove(image):
    # Convert PIL Image to OpenCV format
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale and threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Noise removal using morphological operations
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
    
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Marker labelling
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown==255] = 0
    
    # Apply watershed algorithm
    markers = cv2.watershed(img, markers)
    img[markers == -1] = [0,0,0]
    
    # Create a transparent background
    transparent = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
    transparent[:,:,0:3] = img
    transparent[:,:,3] = (markers != 1).astype(np.uint8) * 255
    
    # Convert back to PIL Image
    result = Image.fromarray(cv2.cvtColor(transparent, cv2.COLOR_BGRA2RGBA))
    return result

def main():
    st.set_page_config(page_title="Background Removal App", page_icon="🖼️")
    
    st.title("🖼️ Photo Background Removal App")
    st.write("Upload an image and remove its background with just one click!")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_column_width=True)
        
        if st.button("Remove Background"):
            with st.spinner('Removing background...'):
                result = simple_background_remove(image)
            st.image(result, caption="Image with Background Removed", use_column_width=True)
            
            buffered = BytesIO()
            result.save(buffered, format="PNG")
            st.download_button(
                label="Download result",
                data=buffered.getvalue(),
                file_name="background_removed.png",
                mime="image/png"
            )

    st.write("---")
    st.write("Note: This app uses a simple color-based segmentation for background removal.")
    st.write("Results may vary depending on the complexity of the image.")
    st.write("Created with ❤️ using Streamlit and OpenCV")

if __name__ == "__main__":
    main()
