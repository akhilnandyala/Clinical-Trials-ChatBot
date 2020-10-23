import numpy as np
import pandas as pd
import preprocessor as p
from tensorflow.keras.models import load_model
import joblib
from pathlib import Path
from PIL import Image
import streamlit as st
import api as api
import re
import speech_recognition as sr

#include these packages when using audio
# from gtts import gTTS
# import os
# from playsound import playsound


# paths
# img_path = Path.joinpath(Path.cwd(), 'images')
# artifacts_path = Path.joinpath(Path.cwd(), 'model_artifacts')
# datasets_path = Path.joinpath(Path.cwd(), 'dataset')

# load images
# center = Image.open(Path.joinpath(img_path, 'center.jpg'))
# federer_image = Image.open(Path.joinpath(img_path, 'federer.jpg'))
# nadal = Image.open(Path.joinpath(img_path, 'Nadal.jpg'))

# load artifacts
model = load_model(Path.joinpath(Path.cwd(), 'model-v1.h5'))
tokenizer_t = joblib.load(Path.joinpath(Path.cwd(), 'tokenizer_t.pkl'))
vocab = joblib.load(Path.joinpath(Path.cwd(), 'vocab.pkl'))

df2 = pd.read_csv(Path.joinpath(Path.cwd(), 'responses.csv'))
condition_df = pd.read_csv(Path.joinpath(Path.cwd(), 'medical_condition.csv'))
world_cities_df = pd.read_csv(Path.joinpath(Path.cwd(), 'world-cities_csv.csv'))

original_input_text = ''
voice_input_check = 0

def get_pred(model, encoded_input):
    pred = np.argmax(model.predict(encoded_input))
    return pred


def bot_precausion(df_input, pred):
    words = df_input.questions[0].split()
    if len([w for w in words if w in vocab]) == 0:
        pred = 0
    return pred


def get_response(df2, pred):
    upper_bound = df2.groupby('labels').get_group(pred).shape[0]
    r = np.random.randint(0, upper_bound)
    resp = list(df2.groupby('labels').get_group(pred).responses)
    return resp[r]


def bot_response(response, ):
    return response


def botResponse(user_input, user_name, user_location, user_age, user_gender='All'):
    df_input = user_input

    df_input = p.remove_stop_words_for_input(p.tokenizer, df_input, 'questions')
    encoded_input = p.encode_input_text(tokenizer_t, df_input, 'questions')

    pred = get_pred(model, encoded_input)
    pred = bot_precausion(df_input, pred)
    a = df_input.iloc[0]['questions']
    if pred == 0:
        if not a:
            default_response = 'Hi {}, I am Bowhead Bot, I can help you get to know more about Bowhead Health and the services we provide. I can also help you find information about medical trials.'.format(user_name)
            response = default_response
        else:
            response = get_response(df2, pred)
            response = bot_response(response)
    elif pred == 1:
        for i, r in condition_df.iterrows():
            med_condition_word_list = r['med_condition'].split()
            med_condition_word_combo_list = list(map(' '.join, zip(med_condition_word_list[:-1], med_condition_word_list[1:])))
            print(original_input_text)
            print(med_condition_word_combo_list)
            if re.search(r['med_condition'], original_input_text, re.IGNORECASE) or any(x in original_input_text.upper() for x in med_condition_word_combo_list):
                user_condition = r['med_condition']
                break
            else:
                user_condition = 'none'

        if user_condition == 'none':
            for i, r in condition_df.iterrows():
                med_condition_word_list = r['med_condition'].split()
                print(original_input_text)
                print(med_condition_word_list)
                if re.search(r['med_condition'], original_input_text, re.IGNORECASE) or any(x in original_input_text.upper() for x in med_condition_word_list):
                    user_condition = r['med_condition']
                    break
                else:
                    user_condition = 'none'

        trial_data = api.trial_details(user_condition, user_location, user_age, user_gender)
        response = trial_data
        # writing the reponse to a seperate streamlit write to use the parameter 'unsafe_allow_html' to display the html output
        st.write(response, unsafe_allow_html=True)
        # To hide the actual Bot response 'st.text_area' and displaying the trials html data separately using above command
        response = ''
    else:
        response = get_response(df2, pred)
        response = bot_response(response)

    return response


def get_text():
    # global voice_input_check
    # if st.button('Voice Input'):
    #     voice_input_check = 1
    #     r = sr.Recognizer()
    #     mic = sr.Microphone()
    #     with mic as source:
    #         audio = r.listen(source)
    #         try:
    #             input_text = r.recognize_google(audio, language='en-US')
    #         except sr.UnknownValueError:
    #             input_text = "Sorry could not understand, Please try again"
    #     st.write(input_text)
    # else:
    #     input_text = st.text_input("You: ", key=3)

# If above audio code is enabled, comment out the below line of code, else uncomment
    input_text = st.text_input("You: ", key=3)

    global original_input_text
    original_input_text = input_text
    df_input = pd.DataFrame([input_text], columns=['questions'])
    return df_input


st.title("""
Bowhead Bot  
Bowhead Bot's main functionality is to help you find the information about medical trials
""")
st.sidebar.title("Bowhead Bot")
st.sidebar.write('Please enter you name')
user_name = st.sidebar.text_input('You', key=1)
user_location = st.sidebar.selectbox('Please select you city', world_cities_df)
user_location = str(user_location)
user_age = st.sidebar.slider('Please select you age', 0, 100, 50, 1)
user_age = str(user_age) + ' ' + 'years'
user_gender = st.sidebar.radio('Please select your gender', ('Male', 'Female', 'Other'))

# st.image(center, width=700)
# st.sidebar.image(federer_image)
# st.sidebar.image(nadal, width=350)
user_input = get_text()
if user_name and user_location and user_age:
    response = botResponse(user_input, user_name, user_location, user_age, user_gender)

if not user_name or not user_location or not user_age:
    response = 'Hello user, Please fill the details on the left panel before proceeding.'

if response:
    st.text_area("Bot:", value=response, height=200, max_chars=None, key=None)
    # If audio is enabled, uncomment the below code, else comment it out
    # if voice_input_check:
    #     speech = gTTS(text=response, lang='en-US', slow=False)
    #     speech.save("text.mp3")
    #     playsound("text.mp3")
    #     os.remove("text.mp3")
