To reproduce the work, ensure you carefully understand and follow the below steps.

Points to remember:

1.Covid_bot.ipynb -  Contains the source code to build and deploy the machine learning model.
2.app_version3 - Contains the flask code to build the user interface and process the user input, so to be sent to the loaded ML model.
3.templates - Contains the index.html file that is displayed on the front end.
4.static - Contains the CSS and JavaScript files used in building the UI.
5.preprocessor.py - Contains functions built to pre-process the user input sent from the front end.
6.api.py -  Contains the code used to pull Clinical trials using the ClinicalTrials API.

7.new_intent.json - The training data used in building our model.
8.model-v3.h5 - The saved model from jupyter notebook.
9.tokenizer_t.pkl - The saved tokenizer object of the training data, that used to encode the new user input.
10.vocab.pkl - The saved vocabulary of the training data.

11.medical_condition.csv - The csv file used for medical condition entity extraction from user input.
12.world-cities_csv.csv - The csv file used for location entity extraction from user input.


To test the bot on your local machine: 
- Run app_version3.py from Pycharm or your terminal and it opens up in your local host.
- To modify the model, make changes to the Covid_bot.ipynb and rerun the app_version3.py.

An active version of the bot is available at 
https://blooming-earth-31686.herokuapp.com/

