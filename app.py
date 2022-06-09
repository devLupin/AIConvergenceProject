
import streamlit as st
import os, errno
from PIL import Image
import subprocess
import csv
from pathlib import Path

from silence_tensorflow import silence_tensorflow
silence_tensorflow()


st.set_page_config(
    page_title="Personal information Detection",
    page_icon="🙍‍♂️",
)

def _max_width_():
    max_width_str = f"max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


def load_image(image_file):
    img = Image.open(image_file)
    return img


def remove(file):
    try:
        os.remove(file)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
    

_max_width_()

c30, c31, c32 = st.columns([2.5, 1, 3])

with c30:
    # st.image("logo.png", width=400)
    st.title("🔑 Personal information Detection")
    st.header("")



with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   You can check whether personal information has been leaked from [DCInside](https://www.dcinside.com/).
-   Use [ArcFace](https://arxiv.org/abs/1801.07698) to find posts with images of the same person.
	    """
    )

    st.markdown("")
    
    st.markdown("### 🎮 **Usage**")
    
    video_file = open('demo.mp4', 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)



st.markdown("")
st.markdown("## 📌 **Personal information leakage detection**")
with st.form(key="my_form"):

    ce, c1, ce, c2, c3 = st.columns([0.07, 1, 0.07, 5, 0.07])
    with c1:
        st.radio(
            "Model",
            ["ArcFace"],
            help="",
        )
        
        backbone_type = st.radio(
            "Backbone",
            ["ResNet50"],
            help="",
        )


    image_file = None
    img = None
    with c2:
        # st.subheader("Image")
        
        image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
        
        check_button = st.form_submit_button(label="✔ Check")
        if image_file is not None:
            # file_details = {"filename":image_file.name, "filetype":image_file.type,
            #                 "filesize":image_file.size}
            # st.write(file_details)
            st.image(load_image(image_file), caption='upload image')
            
            # before resizing
            with open("raw.png", "wb") as f:
                f.write((image_file).getbuffer())
            
            # after resizing  ==> temp.png
            subprocess.run(['python', 'detection.py'])
            
        
    if image_file is None:
        st.stop()
    submit_button = st.form_submit_button(label="✨ Run")
    

if not submit_button:
    st.stop()



# recognition
subprocess.run(['python', 'recognition.py'])

st.markdown("")
st.markdown("## 🔓 **Leaked Status**")

if len(os.listdir('output')) == 0:
    st.write('None')


def search_leaked_image(im):
    log = open('log.csv', 'r')
    rdr = csv.reader(log)
        
    user_img_name = Path(im).stem
    
    for line in rdr:
        words = line
        
        if len(words) == 0 or words[0] == 'link':
            continue
        
        f_name = words[1]
        f_name = Path(f_name).stem
        link = words[0]
        
        if(user_img_name == f_name):
            return link
    
    return 0


for im in os.listdir('output'):
    st.image(load_image(os.path.join('output', im)), caption='Leaked image')
    
    link = search_leaked_image(im)
    
    if link == 0:
        st.write("Leaked image")
    else:
        st.write(f"[Go to post]({link})")
    remove(os.path.join('output', im))

remove('raw.png')
remove('temp.png')