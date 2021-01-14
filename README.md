To reproduce the work, ensure you carefully understand and follow the below steps.

Points to remember:

- Covid_bot.ipynb :  Contains the source code to build and deploy the machine learning model.
- app_version3 : Contains the flask code to build the user interface and process the user input, so to be sent to the loaded ML model.
- templates : Contains the index.html file that is displayed on the front end.
- static : Contains the CSS and JavaScript files used in building the UI.
- preprocessor.py : Contains functions built to pre-process the user input sent from the front end.
- api.py : Contains the code used to pull Clinical trials using the ClinicalTrials API.

- new_intent.json : The training data used in building our model.
- model-v3.h5 : The saved model from jupyter notebook.
- tokenizer_t.pkl : The saved tokenizer object of the training data, that used to encode the new user input.
- vocab.pkl : The saved vocabulary of the training data.

- medical_condition.csv : The csv file used for medical condition entity extraction from user input.
- world-cities_csv.csv : The csv file used for location entity extraction from user input.


To test the bot on your local machine: 
- Run app_version3.py from Pycharm or your terminal and it opens up in your local host.
- To modify the model, make changes to the Covid_bot.ipynb and rerun the app_version3.py.

An active version of the bot is available at 
https://blooming-earth-31686.herokuapp.com/

After answering the requested questions, you can ask for clinical trials data such as 'Show me some covid trials available in Vancouver' or 'Find me some cancer trials in California'. Relevant clinical trials available in the mentioned location will be preseneted to users.

