import streamlit as st
import cv2
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="Image Size & Flip Tool", layout="centered")

st.title("🖼️ Image Resize & Flip Tool")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Load and display original image
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    st.image(image, caption="📷 Uploaded Image", use_column_width=True)

    # Resize inputs
    st.subheader("Resize Options")
    Height = st.number_input("Set Height", min_value=1, value=image_np.shape[0])
    Width = st.number_input("Set Width", min_value=1, value=image_np.shape[1])

    # Flip options
    st.subheader("Flip Options")
    flip_option = st.selectbox(
        "Flip Image",
        options=["None", "Horizontal", "Vertical", "Both"],
        index=0
    )

    if st.button("Process Image"):
        # Resize
        resized_image = cv2.resize(image_np, (Width, Height))

        # Flip if selected
        if flip_option == "Horizontal":
            resized_image = cv2.flip(resized_image, 1)
        elif flip_option == "Vertical":
            resized_image = cv2.flip(resized_image, 0)
        elif flip_option == "Both":
            resized_image = cv2.flip(resized_image, -1)

        # Show result
        st.image(resized_image, caption="🖼️ Processed Image", use_column_width=True)

        # Prepare for download
        with io.BytesIO() as buff:
            result_image = Image.fromarray(resized_image)
            result_image.save(buff, format="PNG")
            st.download_button(
                label="📥 Download Processed Image",
                data=buff.getvalue(),
                file_name="processed_image.png",
                mime="image/png"
            )
