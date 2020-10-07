import os

with open(os.path.join("C:/Users/akhil/PycharmProjects/Covid-ChatBot", 'Procfile'), "w") as file1:
    toFile = 'web: sh setup.sh && streamlit run app.py'
    file1.write(toFile)

