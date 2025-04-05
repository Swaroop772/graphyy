import streamlit as st
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

# Function to encode the message into the image
def encode_message(image, message):
    d = {chr(i): i for i in range(255)}  # Mapping characters to pixel values
    img = np.array(image)
    m, n, z = 0, 0, 0

    for char in message:
        img[n, m, z] = d[char]
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3

    return img

# Function to decode the message from the image
def decode_message(image, message_length):
    c = {i: chr(i) for i in range(255)}
    img = np.array(image)
    m, n, z = 0, 0, 0
    message = ""

    try:
        for _ in range(message_length):
            message += c[img[n, m, z]]
            n = (n + 1) % img.shape[0]
            m = (m + 1) % img.shape[1]
            z = (z + 1) % 3
    except KeyError:
        return "Message extraction error."

    return message

st.title("Secure Data Hiding in Image Using Steganography (Simulated Cloud Storage)")

option = st.radio("Choose an option:", ("Encrypt Message", "Decrypt Message"))

if option == "Encrypt Message":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        st.image(image, caption="Original Image", use_column_width=True, channels="BGR")

        message = st.text_input("Enter your secret message:")
        if st.button("Encrypt and Upload (Simulated Cloud Storage)"):
            encrypted_img = encode_message(image, message)

            # Save encrypted image to memory (simulate cloud)
            is_success, buffer = cv2.imencode(".png", encrypted_img)
            if is_success:
                # Store the image bytes and original image for comparison
                st.session_state['encrypted_image_bytes'] = buffer.tobytes()
                st.session_state['message_length'] = len(message)
                st.success("Image encrypted and uploaded (stored in memory)")
                st.image(encrypted_img, caption="Encrypted Image", use_column_width=True, channels="BGR")

elif option == "Decrypt Message":
    uploaded_file = st.file_uploader("Upload the encrypted image", type=["jpg", "png"])
    if uploaded_file:
        file_bytes = uploaded_file.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        uploaded_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        st.image(uploaded_image, caption="Uploaded Image for Decryption", use_column_width=True, channels="BGR")

        if st.button("Decrypt Message"):
            if 'encrypted_image_bytes' not in st.session_state:
                st.warning("No encrypted image found in memory. Please encrypt and upload first.")
            else:
                # Compare uploaded image to the stored encrypted image
                stored_bytes = st.session_state['encrypted_image_bytes']
                if file_bytes == stored_bytes:
                    message_length = st.session_state['message_length']
                    decrypted_message = decode_message(uploaded_image, message_length)
                    st.success(f"Decrypted Message: {decrypted_message}")
                else:
                    st.error("Uploaded image does not match the encrypted image.")
