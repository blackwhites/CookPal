import os
import streamlit as st
from PIL import Image
from VertexAIChat import ChatBot

st.set_page_config('CookPal', ':cook:')
st.title('CookPal :cook:')

ROOT_DIR = os.path.dirname(__file__)
with open(os.path.join(ROOT_DIR, 'about.txt')) as f:
    about = f.read()

chatbot = ChatBot(dict(st.secrets))
# load food_recognizer model here

tab1, tab2 = st.tabs(['Recognize Food', 'About'])

with tab1:
    input = st.radio('Choose an input method:', ['Camera', 'Text'])

    if input == 'Camera':
        buffer = st.camera_input('Take a picture of food items!')
        if buffer:
            img = Image.open(buffer)
            # preprocess (resize, noramlize) and inference
            food_tags = '' # list of recognized food items
        else:
            food_tags = ''
    else:
        food_tags = st.text_input('Food Tags:')

    if food_tags:
        prompt = f'''
        Provide 1-3 recipe suggestions for these food items: {food_tags}
        Write in this structure:
        <dish name> (in bold)
        <instructions>
        1. 
        2. 
        3. 
        Don't write ingredients.
        '''
        response = chatbot.send_msg(prompt)
        st.write(response)


with tab2:
    st.write(about)
