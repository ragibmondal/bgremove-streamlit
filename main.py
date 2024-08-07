import streamlit as st
from PIL import Image
import numpy as np
from rembg import remove
from io import BytesIO

def remove_background(image):
    # Convert PIL Image to numpy array
    img_array = np.array(image)
    
    # Remove background
    output = remove(img_array)
    
    # Convert back to PIL Image
    return Image.fromarray(output)

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
                result = remove_background(image)
            st.image(result, caption="Image with Background Removed", use_column_width=True)
            
            # Allow downloading the result
            buffered = BytesIO()
            result.save(buffered, format="PNG")
            st.download_button(
                label="Download result",
                data=buffered.getvalue(),
                file_name="background_removed.png",
                mime="image/png"
            )

    st.write("---")
    st.write("Note: While this app aims for high accuracy, perfect background removal may not always be achievable.")
    st.write("Created with ❤️ using Streamlit and rembg")

if __name__ == "__main__":
    main()
