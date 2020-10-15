import json
import requests
import pandas as pd
from pytrials.client import ClinicalTrials

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.2f}'.format)


def make_clickable(link):
    text = link.split('/')[4]
    return f'<a target="_blank" href="{link}">{text}</a>'

def trial_details(user_condition, user_location):
    ct = ClinicalTrials()

    # ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=50)

    search_query = '{} AND SEARCH[Location](AREA[LocationCity]{})'.format(user_condition, user_location)
    corona_fields = ct.get_study_fields(
        search_expr=search_query,
        fields=["NCTId", "Condition", "BriefTitle"],
        max_studies=50,
        fmt="csv",
    )

    ct_df = pd.DataFrame.from_records(corona_fields[1:], columns=corona_fields[0])
    ct_df['NCTId'] = ct_df['NCTId'].apply(lambda x: 'https://clinicaltrials.gov/show/' + x)

    ct_df['NCTId'] = ct_df['NCTId'].apply(make_clickable)
    ct_df = ct_df.to_html(escape=False)
    # st.write(df, unsafe_allow_html=True)
    # print(ct_df)
    return ct_df

# trial_details("diabetes",'Ottawa')



