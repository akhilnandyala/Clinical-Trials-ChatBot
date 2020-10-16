import json
import requests
import pandas as pd
import codecs
from pytrials.client import ClinicalTrials

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.2f}'.format)


def make_clickable(link):
    text = link.split('/')[4]
    return f'<a target="_blank" href="{link}">{text}</a>'

def trial_details(user_condition, user_location, user_age, user_gender):
    ct = ClinicalTrials()

    # ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=50)

    search_query = '{} AND (SEARCH[Location](AREA[LocationCity]{}) AND AREA[MinimumAge]RANGE[MIN,{}] AND AREA[MaximumAge]RANGE[{},MAX] AND (AREA[Gender]All OR  AREA[Gender]{}))'.format(user_condition, user_location, user_age, user_age, user_gender)
    corona_fields = ct.get_study_fields(
        search_expr=search_query,
        fields=["Gender", "MinimumAge", "MaximumAge", "NCTId", "Condition", "BriefTitle"],
        max_studies=50,
        fmt="csv",
    )

    ct_df = pd.DataFrame.from_records(corona_fields[1:], columns=corona_fields[0])
    ct_df['NCTId'] = ct_df['NCTId'].apply(lambda x: 'https://clinicaltrials.gov/show/' + x)

    ct_df['NCTId'] = ct_df['NCTId'].apply(make_clickable)

    ct_df = ct_df.to_html(escape=False,border=0)

    print(ct_df)
    return ct_df

trial_details("hepatitis B",'Ottawa', '30 years', "Male")

