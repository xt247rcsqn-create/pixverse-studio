import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Pixverse Studio", layout="wide")
st.title("📸 Pixverse Studio")

uploaded = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])

if uploaded is not None:
    # Bild einlesen und anzeigen
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original", use_column_width=True)

    # Filterauswahl
    filter_option = st.selectbox("Filter wählen", ["None", "Weichzeichnen", "Schärfen"])
    strength = st.slider("Stärke", 0.1, 3.0, 1.0, 0.1)

    # Filter anwenden
    if st.button("Filter anwenden"):
        img_f = img.astype(np.float32) / 255.0
        if filter_option == "Weichzeichnen":
            ksize = max(3, int(5 * strength))
            result = cv2.GaussianBlur(img_f, (ksize, ksize), 0)
        elif filter_option == "Schärfen":
            kernel = np.array([[0, -1, 0],
                               [-1, 5 * strength, -1],
                               [0, -1, 0]])
            result = cv2.filter2D(img_f, -1, kernel)
        else:
            result = img_f

        result = (result * 255).astype(np.uint8)
        st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), caption="Ergebnis", use_column_width=True)

        # Download-Button
        result_pil = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        st.download_button("💾 Download", data=result_pil.tobytes(), file_name="pixverse_result.png", mime="image/png")
else:
    st.info("⬆️ Bitte lade ein Bild hoch, um zu beginnen.")
