import streamlit as st
import ffmpeg
import tempfile
import os

#can change logo if needed
logo_image = "https://i.ibb.co/vHJZL0y/insightly.png"
st.image(logo_image, width=300)

#extracting  video frames
def extract_frames(video_file, num_frames, temp_dir):
    probe = ffmpeg.probe(video_file)
    duration = float(probe['streams'][0]['duration'])
    width = probe['streams'][0]['width']
    intervals = duration / num_frames

    frame_list = []
    for i in range(num_frames):
        start_time = i * intervals
        output_filename = f'Image{i}.jpg'
        output_filepath = os.path.join(temp_dir, output_filename)
        (
            ffmpeg
            .input(video_file, ss=start_time)
            .filter('scale', width, -1)
            .output(output_filepath, vframes=1)
            .run(overwrite_output=True)
        )
        frame_list.append(output_filepath)

    return frame_list

# added streamlit
def main():
    st.title("Video Frame Extraction")

    uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])

    if uploaded_file is not None:
        #can change max and min values of frames extracted
        num_frames = st.slider("Number of Frames to Extract", min_value=1, max_value=10, value=3)

        #temporary directory
        temp_dir = tempfile.mkdtemp()  
        if st.button("Extract Frames"):
            with st.spinner("Extracting frames..."):
                video_path = os.path.join(temp_dir, uploaded_file.name)
                with open(video_path, 'wb') as video_file:
                    video_file.write(uploaded_file.read())
                frame_list = extract_frames(video_path, num_frames, temp_dir)
                st.success("Frames extracted successfully!")

                for frame in frame_list:
                    st.image(frame, caption="Extracted Frame", use_column_width=True)

if __name__ == "__main__":
    main()
