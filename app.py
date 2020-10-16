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

original_input_text = ''

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
            default_response = 'Hi {}, I am Bowhead Bot, I can help you get to know more about Bowhead Health and the services we provide. I can also help you find information about medical trials'.format(user_name)
            response = default_response
        else:
            response = get_response(df2, pred)
            response = bot_response(response)
    elif pred == 1:
        input_string = df_input.iloc[0]['questions']
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
    input_text = st.text_input("You: ", key=5)
    # input_text = 'I want to find trials for hepatitis B'
    global original_input_text
    original_input_text = input_text

    if st.button('Voice recognition On'):
        import speech_recognition as sr
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            voice_data = r.record(source, duration=10)
            text = r.recognize_google(voice_data, language='en')
            print(text)

        st.write(text)
    df_input = pd.DataFrame([input_text], columns=['questions'])
    return df_input


st.sidebar.title("Bowhead Bot")
st.title("""
Bowhead Bot  
Bowhead Bot's main functionality is to help you find the information about medical trials
""")
st.sidebar.write('Please enter you name')
user_name = st.sidebar.text_input('You', key=1)
st.sidebar.write('Please enter your city')
user_location = st.sidebar.text_input('You', key=2)
st.sidebar.write('Please enter your age in years')
user_age = st.sidebar.text_input('You', key=3)
user_age = user_age + ' ' + 'years'
st.sidebar.write('Please enter your gender')
user_gender = st.sidebar.text_input('You', key=4)

# st.image(center, width=700)
# st.sidebar.image(federer_image)
# st.sidebar.image(nadal, width=350)
user_input = get_text()
response = botResponse(user_input, user_name, user_location, user_age, user_gender)

if not user_name or not user_location or not user_age:
    response = 'Hello user, Please enter your name and location on the left panel before proceeding'

if response:
    st.text_area("Bot:", value=response, height=200, max_chars=None, key=None)



