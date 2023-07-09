import os
import streamlit as st
from PIL import Image
from GCPVertexAI import ChatBot
from ClarifaiAPI import FoodRecognizer

st.set_page_config('CookPal', ':cook:')
st.title('CookPal :cook:')

ROOT_DIR = os.path.dirname(__file__)
with open(os.path.join(ROOT_DIR, 'about.txt')) as f:
    about = f.read()

chatbot = ChatBot(dict(st.secrets['gcp_service_account']))
food_recognizer = FoodRecognizer(st.secrets['clarifai_api']['PAT'])

tab1, tab2 = st.tabs(['Recognize Food', 'About'])

with tab1:
    input = st.radio('Choose an input method:', ['Camera', 'Text'])
    num_of_rcps = st.number_input('Select number of suggested recipes:', 1, 3, 1, 1)

    if input == 'Camera':
        buffer = st.camera_input('Take a picture of food items!')
        if buffer:
            img = Image.open(buffer)
            response = food_recognizer.recognize(img)
            food_tags = ', '.join(response.keys())
            st.info(f'Food Tags Recognized: {food_tags}')
        else:
            food_tags = ''
    else:
        food_tags = st.text_input('Food Tags:')

    if food_tags:
        prompt = f'''
        Provide {num_of_rcps} recipe suggestions for these food items: {food_tags}
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
