import streamlit as st
from streamlit.logger import get_logger
from pathlib import Path
import os

LOGGER = get_logger(__name__)

if __name__ == "__main__":
    st.write("## Please Upload Your Video Here")
    theme = st.selectbox(
            "Select your video cateogry",
            ("Funny", "Sad", "Celebration"),
            key='category'
        )
    # Allow users to upload a video file
    video_file = st.file_uploader("Upload Video File", type=['mp4', 'avi', 'mov'])

    # Button to confirm upload
    clicked = st.button('Upload')

    if video_file is not None:
        # Show the video immediately
        st.video(video_file)

        if clicked:
            # Save the uploaded file
            parent_path = Path(__file__).parent.parent.resolve()
            save_path = os.path.join(parent_path, "")
            os.makedirs(save_path, exist_ok=True)  # Ensure the directory exists
            complete_name = os.path.join(save_path, video_file.name)

            with open(complete_name, "wb") as destination_file:
                destination_file.write(video_file.read())

            st.success(f"Video saved to: {complete_name}")
