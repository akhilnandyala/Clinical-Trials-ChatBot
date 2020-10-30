from flask import Flask, render_template, render_template_string, request, session
import numpy as np
import pandas as pd
import preprocessor as p
from tensorflow.keras.models import load_model
import joblib
from pathlib import Path
import re
import api as api
import secrets


# load artifacts
tokenizer_t = joblib.load(Path.joinpath(Path.cwd(), 'tokenizer_t.pkl'))
vocab = joblib.load(Path.joinpath(Path.cwd(), 'vocab.pkl'))

df2 = pd.read_csv(Path.joinpath(Path.cwd(), 'responses.csv'))
condition_df = pd.read_csv(Path.joinpath(Path.cwd(), 'medical_condition.csv'))
world_cities_df = pd.read_csv(Path.joinpath(Path.cwd(), 'world-cities_csv.csv'))

original_input_text = ''
# voice_input_check = 0

def get_pred(encoded_input):
    model = load_model(Path.joinpath(Path.cwd(), 'model-v1.h5'))
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

    pred = get_pred(encoded_input)
    pred = bot_precausion(df_input, pred)
    a = df_input.iloc[0]['questions']
    if pred == 0:
        if not a:
            default_response = 'Hi {}, I am Bowhead Bot, I can help you get to know more about Bowhead Health and the services we provide. Also I can help you find information about medical trials.'.format(user_name)
            response = default_response
        else:
            response = get_response(df2, pred)
            response = bot_response(response)
    elif pred == 1:
        for i, r in condition_df.iterrows():
            med_condition_word_list = r['med_condition'].split()
            med_condition_word_combo_list = list(map(' '.join, zip(med_condition_word_list[:-1], med_condition_word_list[1:])))
            if re.search(r['med_condition'], original_input_text, re.IGNORECASE) or any(x in original_input_text.upper() for x in med_condition_word_combo_list):
                user_condition = r['med_condition']
                break
            else:
                user_condition = 'none'

        if user_condition == 'none':
            for i, r in condition_df.iterrows():
                med_condition_word_list = r['med_condition'].split()
                if re.search(r['med_condition'], original_input_text, re.IGNORECASE) or any(x in original_input_text.upper() for x in med_condition_word_list):
                    user_condition = r['med_condition']
                    break
                else:
                    user_condition = 'none'

        trial_data = api.trial_details(user_condition, user_location, user_age, user_gender)
        response = trial_data
    else:
        response = get_response(df2, pred)
        response = bot_response(response)

    return {'response': response, 'pred': pred}

def get_text(user_input):
    global original_input_text
    original_input_text = user_input
    df_input = pd.DataFrame([user_input], columns=['questions'])
    return df_input


app = Flask(__name__)
secret = 'adifjh34g5j43h534akjfn'
app.secret_key = secret

def get_user_details():
    if session.get('user_name_check') == 0:
        bot_response = 'Please enter your name'
        return render_template('index.html', bot_response=bot_response)
    if session.get('user_location_check') == 0:
        bot_response = 'Please enter your location'
        return render_template('index.html', user_input=session.get('user_name'), bot_response=bot_response)
    if session.get('user_age_check') == 0:
        bot_response = 'Please enter your age'
        return render_template('index.html', user_input=session.get('user_location'), bot_response=bot_response)
    if session.get('user_gender_check') == 0:
        bot_response = 'Please enter your gender'
        return render_template('index.html', user_input=session.get('user_age'), bot_response=bot_response)

def flush_all_values():
    session['user_name_check'] = 0
    session['user_location_check'] = 0
    session['user_age_check'] = 0
    session['user_gender_check'] = 0
    session['all_checked_check'] = 0
    session['user_name'] = ''
    session['user_location'] = ''
    session['user_age'] = 0
    session['user_gender'] = ''

@app.route('/')
def index():
    session['user_name_check'] = 0
    session['user_location_check'] = 0
    session['user_age_check'] = 0
    session['user_gender_check'] = 0
    session['all_checked_check'] = 0
    session['user_name'] = ''
    session['user_location'] = ''
    session['user_age'] = 0
    session['user_gender'] = ''
    session['initialize_check'] = 0
    return render_template('index.html')

@app.route('/initialize', methods=['POST'])

def initialize():
    if request.form['initialize_bot'] == 'Initialize':
        session['initialize_check'] = 1
        flush_all_values()
        print('x')
        x = get_user_details()
        return x
    else:
        return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if session.get('initialize_check') == 1:
        if session.get('user_name_check') == 0:
            session['user_name'] = request.form['user_input']
            if session.get('user_name').isalpha():
                session['user_name_check'] = 1
                x = get_user_details()
                return x
            else:
                return render_template('index.html', bot_response='Name should only contain alphabets, Please enter your name again')
        if session.get('user_location_check') == 0:
            session['user_location'] = str(request.form['user_input'])
            if session.get('user_location').upper() in (city.upper() for city in world_cities_df['name'].values):
                session['user_location_check'] = 1
                x = get_user_details()
                return x
            else:
                return render_template('index.html', bot_response='Please enter correct city name')
        if session.get('user_age_check') == 0:
            user_age_to_modify = request.form['user_input']
            if user_age_to_modify.isdigit() and 1 <= int(user_age_to_modify) <= 100:
                session['user_age'] = str(user_age_to_modify) + ' ' + 'years'
                session['user_age_check'] = 1
                x = get_user_details()
                return x
            else:
                return render_template('index.html', bot_response='Please enter valid age value')
        if session.get('user_gender_check') == 0:
            user_gender_to_check = str(request.form['user_input'])
            if user_gender_to_check in ['male', 'female', 'other', 'Male', 'Female', 'Other']:
                session['user_gender'] = user_gender_to_check
                session['user_gender_check'] = 1
                session['all_checked_check'] = 1
            else:
                return render_template('index.html', bot_response='Please ensure gender value is among "Male", "Female" and "Other" ')

        if session.get('user_name_check') == 1 and session.get('user_location_check') == 1 and session.get('user_age_check') == 1 and session.get('user_gender_check') == 1:
            print("all checked")
            if session.get('all_checked_check') == 1:
                default_response = 'Hi {}, I am Bowhead Bot, I can help you get to know more about Bowhead Health and the services we provide. Also I can help you find information about medical trials.'.format(session.get('user_name'))
                session['all_checked_check'] = 2
                return render_template('index.html', bot_response=default_response)
            print('if',session.get('user_name_check'),session.get('user_location_check'),session.get('user_age_check'),session.get('user_gender_check'),session.get('all_checked_check'))
            user_name = session.get('user_name')
            user_location = session.get('user_location')
            user_age = session.get('user_age')
            user_gender = session.get('user_gender')
            user_input = request.form['user_input']
            user_input_df = get_text(user_input)
            print(user_name,user_location,user_age,user_gender,user_input_df)
            bot_response_pred = botResponse(user_input_df, user_name, user_location, user_age, user_gender)
            bot_response = bot_response_pred['response']
            bot_pred = bot_response_pred['pred']
            return render_template('index.html', user_input=user_input, bot_response=bot_response)
        else:
            print('else',session.get('user_name_check'),session.get('user_location_check'),session.get('user_age_check'),session.get('user_gender_check'),session.get('all_checked_check'))
            return render_template('index.html', bot_response='Please enter correct values to user details')
    else:
        return render_template('index.html', bot_response='Please initialize the bot before first use')


if __name__ == '__main__':
    app.run(port=5002)