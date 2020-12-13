from flask import Flask, render_template, render_template_string, request, session, json
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
world_places_df = pd.read_csv(Path.joinpath(Path.cwd(), 'world-cities_csv.csv'))

original_input_text = ''
# voice_input_check = 0

def get_pred(encoded_input):
    model = load_model(Path.joinpath(Path.cwd(), 'model-v3.h5'))
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
    elif pred == 8:
        for i, r in condition_df.iterrows():
            med_condition_word_list = r['med_condition'].split()
            med_condition_word_combo_list = list(map(' '.join, zip(med_condition_word_list[:-1], med_condition_word_list[1:])))
            # print(original_input_text)
            # print(r['med_condition'])
            if re.search(r['med_condition'], original_input_text, re.IGNORECASE) or any(x in original_input_text.upper() for x in med_condition_word_combo_list):
                # print(r['med_condition'])
                user_condition = r['med_condition']
                # print(user_condition)
                print('found in combo')
                break
            else:
                user_condition = 'none'

        if user_condition == 'none':
            for i, r in condition_df.iterrows():
                med_condition_word_list = r['med_condition'].split()
                med_condition_word_list = [i.upper() for i in med_condition_word_list]
                original_input_text_words = original_input_text.split()
                original_input_text_words = [i.upper() for i in original_input_text_words]
                for x in med_condition_word_list:
                    print(x)
                    if x in original_input_text_words:
                        print(med_condition_word_list)
                        print(x)
                        user_condition = x
                        print('found in single')
                        check = 1
                        break
                    else:
                        check = 0
                if check == 1:
                    break
                else:
                    user_condition = 'none'

        world_cities = [i.upper() for i in world_places_df['city']]
        world_countries = [i.upper() for i in world_places_df['country']]
        world_states = [i.upper() for i in world_places_df['state']]

        for i, r in world_places_df.iterrows():
            original_input_text_words = original_input_text.split()
            original_input_text_words = [i.upper() for i in original_input_text_words]
            # print('city', r['city'])
            if r['city'].upper() in original_input_text_words:
                print('city', r['city'])
                user_location = r['city']
                location_code = 1
                break
            elif r['state'].upper() in original_input_text_words:
                print('state', r['state'])
                user_location = r['state']
                location_code = 2
                break
            elif r['country'].upper() in original_input_text_words:
                print('country', r['country'])
                user_location = r['country']
                location_code = 3
                break
            else:
                location_code = 1

        print(user_condition)
        trial_data = api.trial_details(user_condition, location_code, user_location, user_age, user_gender)
        response = trial_data

    elif pred == 4:
        response = call_services()

    elif pred == 6:
        response = call_surveys()

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
default_template = 'index.html'

def get_user_details():
    if session.get('user_name_check') == 0:
        bot_response = "Hi, I am BowHead Bot ! Please let me know your name before we proceed."
        # return render_template(default_template, bot_response=bot_response)
        return json.dumps({"bot_response": bot_response})
    if session.get('user_location_check') == 0:
        bot_response = 'Thank you {}, Just a few more things before I can help you. What is your location? (city)'.format(session.get('user_name'))
        # return render_template(default_template, user_input=session.get('user_name'), bot_response=bot_response)
        return json.dumps({"bot_response": bot_response})
    if session.get('user_age_check') == 0:
        bot_response = 'Almost done {}, Please enter your age in years.'.format(session.get('user_name'))
        # return render_template(default_template, user_input=session.get('user_location'), bot_response=bot_response)
        return json.dumps({"bot_response": bot_response})
    if session.get('user_gender_check') == 0:
        bot_response = 'Yay! Finishing things up {}. Just one more thing, Please let us know your gender for future reference (Others, Female, Male)'.format(session.get('user_name'))
        # return render_template(default_template, user_input=session.get('user_age'), bot_response=bot_response)
        return json.dumps({"bot_response": bot_response})


def call_services():
    link = f"""<a target="_blank" href = "https://bowheadhealth.com/" >Bowhead Health</a>"""
    output = 'We provide the following services: Surveys and Health check ups. You can get to know more by asking me about surveys or check out our website at {}'.format(link)
    return output

def call_surveys():
    link = f"""<a target="_blank" href = "https://bowheadhealth.com/" >Bowhead Health</a>"""
    output = 'The following surveys are offered at present: Migraine survey and Covid survey. More information is available at {}'.format(link)
    return output

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
    return render_template(default_template)

@app.route('/initialize', methods=['GET','POST'])
def initialize():
    if request.form['initialize_bot'] == 'Initialize':
    # if request.args.get('initialize_bot') == 'Initialize':
        session['initialize_check'] = 1
        flush_all_values()
        print('x')
        x = get_user_details()
        return x
    else:
        return render_template(default_template)

@app.route('/process', methods=['GET','POST'])
def process():
    if session.get('initialize_check') == 1:
        if session.get('user_name_check') == 0:
            session['user_name'] = request.form['user_input']
            if session.get('user_name').isalpha():
                session['user_name_check'] = 1
                x = get_user_details()
                return x
            else:
                # return render_template(default_template, bot_response='Name should only contain alphabets, Please enter your name again')
                return json.dumps({"bot_response": 'Name should only contain alphabets, Please enter your name again'})
        if session.get('user_location_check') == 0:
            session['user_location'] = str(request.form['user_input'])
            if session.get('user_location').upper() in (city.upper() for city in world_places_df['city'].values):
                session['user_location_check'] = 1
                x = get_user_details()
                return x
            else:
                # return render_template(default_template, bot_response='Please enter correct city name')
                return json.dumps({"bot_response": 'Please enter correct city name'})
        if session.get('user_age_check') == 0:
            user_age_to_modify = request.form['user_input']
            if user_age_to_modify.isdigit() and 1 <= int(user_age_to_modify) <= 100:
                session['user_age'] = str(user_age_to_modify) + ' ' + 'years'
                session['user_age_check'] = 1
                x = get_user_details()
                return x
            else:
                # return render_template(default_template, bot_response='Please enter valid age value')
                return json.dumps({"bot_response": 'Please enter valid age value'})
        if session.get('user_gender_check') == 0:
            user_gender_to_check = str(request.form['user_input'])
            if user_gender_to_check in ['male', 'female', 'other', 'Male', 'Female', 'Other']:
                session['user_gender'] = user_gender_to_check
                session['user_gender_check'] = 1
                session['all_checked_check'] = 1
            else:
                # return render_template(default_template, bot_response='Please ensure gender value is among "Male", "Female" and "Other" ')
                return json.dumps({"bot_response": 'Please ensure gender value is among "Male", "Female" and "Other" ' })
        if session.get('user_name_check') == 1 and session.get('user_location_check') == 1 and session.get('user_age_check') == 1 and session.get('user_gender_check') == 1:
            print("all checked")
            if session.get('all_checked_check') == 1:
                default_response = 'Great {}! I can now help you get to know more about Bowhead Health and the services we provide. Also, you can ask information about any medical trial you require.'.format(session.get('user_name'))
                session['all_checked_check'] = 2
                # return render_template(default_template, bot_response=default_response)
                return json.dumps({"bot_response": default_response})
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
            # return render_template(default_template, user_input=user_input, bot_response=bot_response)
            return json.dumps({"bot_response": bot_response})
        else:
            print('else',session.get('user_name_check'),session.get('user_location_check'),session.get('user_age_check'),session.get('user_gender_check'),session.get('all_checked_check'))
            # return render_template(default_template, bot_response='Please enter correct values to user details')
            return json.dumps({"bot_response": 'Please enter correct values to user details'})
    else:
        # return render_template(default_template, bot_response='Please initialize the bot before first use')
        return json.dumps({"bot_response": 'Please initialize the bot before first use'})


if __name__ == '__main__':
    app.run(port=5002)
