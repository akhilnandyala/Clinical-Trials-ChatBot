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
from gtts import gTTS
import os
from playsound import playsound


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
            default_response = 'Hi {}, I am Bowhead Bot, I can help you get to know more about Bowhead Health and the services we provide. Also I can help you find information about medical trials. Would you like to find them now ?'.format(user_name)
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
    input_text = st.text_input("You: ", key=3)
    global original_input_text
    original_input_text = input_text
    df_input = pd.DataFrame([input_text], columns=['questions'])
    return df_input

def get_user_name():
    response = 'Hello user, Let me get some details before I can help you. Please enter your name.'
    return response


st.title("""
Bowhead Bot  
Bowhead Bot's main functionality is to help you find the information about medical trials
""")

# if user_name and user_location and user_age:
#     response = botResponse(user_input, user_name, user_location, user_age, user_gender)

response = get_user_name()
if response:
    st.text_area("Bot:", value=response, height=200, max_chars=None, key=None)
user_input = get_text()
