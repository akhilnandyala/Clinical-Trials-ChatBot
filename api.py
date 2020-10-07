import json
import requests
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.2f}'.format)


#
# response = requests.get("http://api.open-notify.org/astros.json")
# print(response.status_code)
# print(response.json())


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# jprint(response.json())
#
#
# parameters = {
#     "lat": 40.71,
#     "lon": -74
# }

response = requests.get("http://ClinicalTrials.gov/api/query/study_fields?expr=COVID-19&fields=NCTId,Condition,BriefTitle&fmt=JSON")
print(response.status_code)
print(response.json())

response = requests.get("http://ClinicalTrials.gov/api/query/study_fields?expr=Coronavirus+COVID&fields=LocationCity&SEARCH[Location](AREA[LocationCity] Bethesda AND AREA[LocationState] Maryland)&fmt=JSON")
print(response.status_code)
print(response.json())

from pytrials.client import ClinicalTrials

ct = ClinicalTrials()

# Get 50 full studies related to Coronavirus and COVID in json format.
ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=50)

# Get the NCTId, Condition and Brief title fields from 500 studies related to Coronavirus and Covid, in csv format.
corona_fields = ct.get_study_fields(
    search_expr="Coronavirus+COVID",
    fields=["NCTId", "Condition", "BriefTitle"],
    max_studies=50,
    fmt="csv",
)

# Read the csv data in Pandas
ct_df = pd.DataFrame.from_records(corona_fields[1:], columns=corona_fields[0])
print(ct_df)

corona_fields2 = ct.get_study_fields("heart attack AND SEARCH[Location](AREA[LocationCity]Ottawa)", ["LocationFacility","LocationCity","BriefTitle"], max_studies=50, fmt='csv')
ct_df = pd.DataFrame.from_records(corona_fields2)
print(ct_df)
