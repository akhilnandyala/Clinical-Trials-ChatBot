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

def trial_details(user_condition, user_location, user_age, user_gender):
    ct = ClinicalTrials()

    # ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=50)

    search_query = '{} AND (SEARCH[Location](AREA[LocationCity]{}) AND AREA[MinimumAge]RANGE[MIN,{}] AND AREA[MaximumAge]RANGE[{},MAX] AND (AREA[Gender]All OR  AREA[Gender]{}))'.format(user_condition, user_location, user_age, user_age, user_gender)
    corona_fields = ct.get_study_fields(
        search_expr=search_query,
        fields=["Gender", "MaximumAge", "MinimumAge", "StdAge", "NCTId", "Condition", "BriefTitle"],
        max_studies=50,
        fmt="csv",
    )

    ct_df = pd.DataFrame.from_records(corona_fields[1:], columns=corona_fields[0])
    ct_df['NCTId'] = ct_df['NCTId'].apply(lambda x: 'https://clinicaltrials.gov/show/' + x)

    ct_df['NCTId'] = ct_df['NCTId'].apply(make_clickable)

    ct_df.to_html('trials.html',escape=False)

    import codecs
    ct_df = codecs.open("trials.html", 'r')
    ct_df_style = codecs.open("trialsCSS.css", 'r')

    print(ct_df.read())
    ApplyGenericCSS('trials.html','trialsCSS.css')
    print(ct_df.read())
    ct_df = pd.read_html('trials.html')
    return ct_df

def ApplyGenericCSS (InputFile, CSSFile):
    with open(CSSFile,'r') as f:
        newlines = []
        for line in f.readlines():
            newlines.append(line)
    f.close()

    with open(InputFile,'r') as f:
        for line in f.readlines():
            newlines.append(line.replace('class="dataframe"','class="TrialsTable"'))
    f.close()
    with open(InputFile, 'w') as f:
        for line in newlines:
            f.write(line)


trial_details("covid",'Ottawa', '20 years', "Male")

