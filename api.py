import json
import requests
import pandas as pd
from pytrials.client import ClinicalTrials

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.2f}'.format)


def trial_details(user_condition, user_location):
    ct = ClinicalTrials()

    # ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=50)

    search_query = '{} AND SEARCH[Location](AREA[LocationCity]{})'.format(user_condition, user_location)
    corona_fields = ct.get_study_fields(
        search_expr=search_query,
        fields=["NCTId", "Condition", "BriefTitle", "LocationFacility", "LocationCity"],
        max_studies=50,
        fmt="csv",
    )

    ct_df = pd.DataFrame.from_records(corona_fields[1:], columns=corona_fields[0])
    print(ct_df)
    return ct_df.iloc[0]['NCTId']


trial_details("diabetes",'Ottawa')