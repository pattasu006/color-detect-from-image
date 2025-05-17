import streamlit as st
import cv2
import pandas as pd
from PIL import Image
import numpy as np
@st.cache_data
def load_colors():
    return pd.read_csv('colors.csv')

colors = load_colors()

def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ''
    for i in range(len(colors)):
        d = abs(R - int(colors.loc[i, 'R'])) + abs(G - int(colors.loc[i, 'G'])) + abs(B - int(colors.loc[i, 'B']))
        if d < minimum:
            minimum = d
            cname = colors.loc[i, 'color_name']
    return cname

st.title("🎨 Color Detection App")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    st.image(image, caption='Uploaded Image')

    if st.button("Click here to detect color using OpenCV"):
        def show_image_with_click(img_array):
            def click_event(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    b, g, r = img_array[y, x]
                    color_name = get_color_name(r, g, b)
                    text = f'{color_name} (R={r} G={g} B={b})'
                    img_copy = img_array.copy()
                    cv2.rectangle(img_copy, (20, 20), (600, 60), (int(b), int(g), int(r)), -1)
                    cv2.putText(img_copy, text, (30, 50), 1, 1.5, (255-int(b), 255-int(g), 255-int(r)), 2)
                    cv2.imshow('Color Detection', img_copy)

            cv2.namedWindow('Color Detection')
            cv2.setMouseCallback('Color Detection', click_event)

            while True:
                cv2.imshow('Color Detection', img_array)
                if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
                    break
            cv2.destroyAllWindows()

        show_image_with_click(img_array.copy())
