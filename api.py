import json
import requests
import pandas as pd
import codecs
import re
from pytrials.client import ClinicalTrials

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.2f}'.format)


def make_clickable(link):
    text = link.split('/')[4]
    return f'<a target="_blank" href="{link}">{text}</a>'

def trial_details(user_condition, location_code, user_location, user_age, user_gender):
    ct = ClinicalTrials()

    if location_code == 1:
        location_parameter = 'LocationCity'
    elif location_code == 2:
        location_parameter = 'LocationState'
    elif location_code == 3:
        location_parameter = 'LocationCountry'

    print(location_code, location_parameter, user_location)

    search_query = '{} AND (SEARCH[Location](AREA[{}]{}) AND AREA[MinimumAge]RANGE[MIN,{}] AND (AREA[Gender]All OR  AREA[Gender]{}))'.format(user_condition, location_parameter, user_location, user_age, user_gender)

    print(search_query)

    corona_fields = ct.get_study_fields(
        search_expr=search_query,
        fields=["Gender", "MinimumAge", "NCTId", "Condition", "BriefTitle"],
        fmt="csv",
    )

    ct_df = pd.DataFrame.from_records(corona_fields[1:], columns=corona_fields[0])
    ct_df['NCTId'] = ct_df['NCTId'].apply(lambda x: 'https://clinicaltrials.gov/show/' + x)
    ct_df['NCTId'] = ct_df['NCTId'].apply(make_clickable)

    user_condition_word_list = user_condition.split()
    user_condition_word_combo_list = list(map(' '.join, zip(user_condition_word_list[:-1], user_condition_word_list[1:])))

    for i, r in ct_df.iterrows():
        if any(x in r['Condition'].upper() for x in user_condition_word_combo_list):
            continue
        elif not re.search(user_condition, r['Condition'], re.IGNORECASE):
            ct_df.drop(i, inplace=True)
        else:
            continue

    ct_df.drop(columns=['Rank'], inplace=True)
    print(ct_df)

    if ct_df.empty:
        ct_df = 'No results found for the medical condition based on given information. You can modify your question or you can re-initialize the bot to modify your preferences. Thank you.'
    else:
        ct_df = ct_df.to_html(escape=False, border=0)

    info = ct.api_info
    print(info)
    return ct_df

# trial_details("Covid", 1, 'Ottawa', '20 years', "Male")

