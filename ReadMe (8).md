# How to run the following Lead-Counseller Matching System

## Prereqs

1. Install python
2. Unzip the Lead-Counsellor Matching System code in a folder of your choice on your system. **Say folder X.**

## Install a virtual environment

1. Open a command prompt in the folder X, that is the folder in which you have the Lead-Counsellor Matching system code.
2. Run the following commands in the given sequence in folder X:
   1. Open a command window in folder X
   2. `python -m venv venv`
   3. `venv\Scripts\activate`
      1. the above command is for a windows operating system
   4. `pip install -r requirements.txt`
   5. `python -m spacy download en_core_web_sm`

## Run the Application

Execute the following steps:

1. Open a command window in folder X
2. `venv\Scripts\activate`
   1. the above command is for the windows operating system
3. `streamlit run app.py`

These commands should openup the user interface on your default web browser.

You can alternatively access the application by typing: `localhost:8501` in your browser.

## How to run the API?

Execute the following steps in a command window in folder X:

1. `uvicorn api:app --reload`

   1. Note 'api' in the above command is based on the name of the file in which the api exists. In this case the name of the file is: `api.py`
   2. In a browser type: `http://127.0.0.1:8000/docs`
   3. You will see an api definition page open. Click on the /calculate_scores api as shown in the following step.
   4. ![1730267051414](image/ReadMe/1730267051414.png)
   5. Click on "Try it out" button.
2. In the request body type the following json and then press the 'Execute' button:

   ```json
      {
           "leads": [
               {
                   "data": {
                       "id": "lead1",
                       "name": "Alice",
                       "State": "Karnataka"
                   }
               }
           ],
           "counsellors": [
               {
                   "data": {
                       "id": "counsellor1",
                       "name": "Dr. Nair",
                       "Overall Experience ( In years )": "6",
                       "Languages Known [Kannada]": "Expert",
                       "Languages Known [Hindi]": "Intermediate"
                   }
               }
           ]
       }
   ```

   Now you should see the response of the execution as a follows:
3. ```json
   [
     {
       "lead_id": "lead1",
       "lead_name": "Alice",
       "counsellor_id": "counsellor1",
       "counsellor_name": "Dr. Nair",
       "matching_score": 4
     }
   ]

   ```

## Unit testing the api

In a command prompt, run `pytest test_api.py`

## How to use the application to demo?

### The frontpage of the application

![1730089259721](image/ReadMe/1730089259721.png)

### Upload the Leads, Counsellors, and the Rules

Upload the files as shown in the snapshot below from the folder X/dataset

![1730089656254](image/ReadMe/1730089656254.png)

### Click on the "Run Lead-Counsellor Matching Method" button as shown in the snapshot below.

![1730089975811](image/ReadMe/1730089975811.png)

### The result of clicking the button above looks as in the snaphot below

![1730090122387](image/ReadMe/1730090122387.png)
