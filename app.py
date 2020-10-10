import numpy as np
import pandas as pd
import preprocessor as p
from tensorflow.keras.models import load_model
import joblib
from pathlib import Path
from PIL import Image
import streamlit as st

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


def get_pred(model, encoded_input):
    pred = np.argmax(model.predict(encoded_input))
    return pred


def bot_precausion(df_input, pred):
    words = df_input.questions[0].split()
    if len([w for w in words if w in vocab]) == 0:
        pred = 1
    return pred


def get_response(df2, pred):
    upper_bound = df2.groupby('labels').get_group(pred).shape[0]
    r = np.random.randint(0, upper_bound)
    responses = list(df2.groupby('labels').get_group(pred).response)
    return responses[r]


def bot_response(response, ):
    return response


def botResponse(user_input, is_startup=True):
    df_input = user_input

    df_input = p.remove_stop_words_for_input(p.tokenizer, df_input, 'questions')
    encoded_input = p.encode_input_text(tokenizer_t, df_input, 'questions')

    pred = get_pred(model, encoded_input)
    pred = bot_precausion(df_input, pred)

    response = get_response(df2, pred)
    response = bot_response(response)

    if is_startup:
        response = "Hi, I'm happy to have you here \nI am Bowhead Bot"
        is_startup = False
        return response

    else:
        return response


def get_text():
    input_text = st.text_input("You: ", "type here")
    df_input = pd.DataFrame([input_text], columns=['questions'])
    return df_input


st.sidebar.title("Bowhead Bot")
st.title("""
Bowhead Bot  
Bowhead Bot's main functionality is to help you find the info about the trials you need
""")

# st.image(center, width=700)
# st.sidebar.image(federer_image)
# st.sidebar.image(nadal, width=350)

user_input = get_text()
response = botResponse(user_input)
st.text_area("Bot:", value=response, height=200, max_chars=None, key=None)

