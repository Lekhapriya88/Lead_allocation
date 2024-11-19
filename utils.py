import spacy

def assign_experience_value(condition):
    """
    Assigns a numerical value to the experience condition.
    
    :param condition: A string representing the experience condition (e.g., '>4', '<2', '2-4', etc.)
    :return: A float representing the numerical value of the experience condition.
    """
    value = 0
    if condition.startswith('<'):
        # For conditions like '<x', return a value slightly lower than x
        value = float(condition[1:]) - 0.5
    elif condition.startswith('>'):
        # For conditions like '>x', return a value slightly higher than x
        value = float(condition[1:]) + 1.0
    elif '-' in condition:
        # For range conditions like 'x-y', return the midpoint of the range
        lower, upper = map(float, condition.split('-'))
        value = (lower + upper) / 2
    else:
        # For single numeric values, return the number itself
        value = float(condition)
    #print(f"The computed value for {condition} is {value}")
    return value

def state_to_primary_language(state_input):
    # Dictionary mapping Indian states to their primary language
    state_language_map = {
        "Andhra Pradesh": "Telugu",
        "Arunachal Pradesh": "English",
        "Assam": "Assamese",
        "Bihar": "Hindi",
        "Chhattisgarh": "Hindi",
        "Goa": "Konkani",
        "Gujarat": "Gujarati",
        "Haryana": "Hindi",
        "Himachal Pradesh": "Hindi",
        "Jharkhand": "Hindi",
        "Karnataka": "Kannada",
        "Kerala": "Malayalam",
        "Madhya Pradesh": "Hindi",
        "Maharashtra": "Marathi",
        "Manipur": "Meitei (Manipuri)",
        "Meghalaya": "English",
        "Mizoram": "Mizo",
        "Nagaland": "English",
        "Odisha": "Odia",
        "Punjab": "Punjabi",
        "Rajasthan": "Hindi",
        "Sikkim": "English",
        "Tamil Nadu": "Tamil",
        "Telangana": "Telugu",
        "Tripura": "Bengali",
        "Uttar Pradesh": "Hindi",
        "Uttarakhand": "Hindi",
        "West Bengal": "Bengali",
        "Delhi": "Hindi",
        "Puducherry": "Tamil"
    }

    # Load the small English model in SpaCy
    nlp = spacy.load("en_core_web_sm")
    # Convert input and states to SpaCy Doc objects for comparison
    input_doc = nlp(state_input)
    state_docs = {state: nlp(state) for state in state_language_map.keys()}

    # Find the best semantic match based on similarity
    closest_match = max(state_docs, key=lambda state: input_doc.similarity(state_docs[state]))
    language = state_language_map[closest_match]
    #print("########################################")
    #print(f"The closest match is : {closest_match} and the language is {language}")
    return language 
    #return state_language_map.get(state, "Unknown State")
    
def process_counsellor_df(df):
    """
    Process the df and creates new features that are easier to use in Rules
    
    :df: a dataframe of counsellors
    :return: a dataframe of counsellors with a new column  having numerical value of the experience condition.
    """
    print("---------------------- in process_counsellor_df")
    
    df['f_Overall Experience ( In years ) Experience Score'] = df['Overall Experience ( In years )'].apply(assign_experience_value)
    df['f_USDC Experience   ( In years ) Experience Score'] = df['USDC Experience   ( In years )'].apply(assign_experience_value)
    #print(df.to_string(index=False))
    return df

def process_lead_df(df):
    """
    Process the df and creates new features that are easier to use in Rules
    
    :df: a dataframe of leads
    :return: a dataframe of leads with a new column  having numerical value of the experience condition.
    """

    print("---------------------- in process_lead_df")
    df['f_Primary Language'] = df['State'].apply(state_to_primary_language)
    #print(df.to_string(index=False))
    return df

