import streamlit as st
import pandas as pd
import json
import uuid
import copy
import hashlib
from lead import Lead
from counsellor import Counsellor
from rule_engine import RuleEngine
import os
from utils import *
from finalize_mapping import *

# Function to load leads from DataFrame
def load_leads(df):
    leads = []
    for _, row in df.iterrows():
        lead_data = row.to_dict()
        leads.append(Lead(**lead_data))
    return leads

# Function to load counsellors from DataFrame
def load_counsellors(df):
    counsellors = []
    for _, row in df.iterrows():
        counsellor_data = row.to_dict()
        # Convert appropriate fields to correct data types if necessary
        counsellors.append(Counsellor(**counsellor_data))
    return counsellors

# Function to assign unique IDs to conditions recursively
def assign_condition_ids(conditions):
    for condition in conditions:
        condition['id'] = str(uuid.uuid4())
        if 'conditions' in condition:
            assign_condition_ids(condition['conditions'])

# Function to remove 'id' fields from conditions recursively
def remove_condition_ids(conditions):
    for condition in conditions:
        condition.pop('id', None)
        if 'conditions' in condition:
            remove_condition_ids(condition['conditions'])

# Function to display a single condition
def display_conditionX(condition, idx, rule_id):
    st.markdown(f"**Condition {idx + 1}**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        left_entity = st.selectbox(
            "Left Entity",
            ["lead", "counsellor"],
            index=["lead", "counsellor"].index(condition['left'].get('entity', 'lead')),
            key=f"left_entity_{condition['id']}"
        )
    with col2:
        # Choose attributes based on the selected left entity
        if left_entity == 'lead':
            left_attribute_options = st.session_state.get('lead_attributes', [])
        else:
            left_attribute_options = st.session_state.get('counsellor_attributes', [])
        left_attribute = st.selectbox(
            "Left Attribute",
            options=left_attribute_options,
            index=left_attribute_options.index(condition['left'].get('attribute', left_attribute_options[0])) if condition['left'].get('attribute', None) in left_attribute_options else 0,
            key=f"left_attr_{condition['id']}"
        )
    with col3:
        operator_options = ["==", "!=", ">", "<", ">=", "<=", "in", "not in"]
        operator = st.selectbox(
            "Operator",
            operator_options,
            index=operator_options.index(condition.get('operator', '==')),
            key=f"operator_{condition['id']}"
        )
    with col4:
        right_type_options = ["Value", "Attribute"]
        is_attribute = 'attribute' in condition['right']
        right_type = st.selectbox(
            "Right Type",
            right_type_options,
            index=1 if is_attribute else 0,
            key=f"right_type_{condition['id']}"
        )
        if right_type == "Value":
            right_value = st.text_input(
                "Right Value",
                value=str(condition['right'].get('value', '')),
                key=f"right_value_{condition['id']}"
            )
            condition['right'] = {'value': right_value}
        else:
            right_entity = st.selectbox(
                "Right Entity",
                ["lead", "counsellor"],
                index=["lead", "counsellor"].index(condition['right'].get('entity', 'lead')),
                key=f"right_entity_{condition['id']}"
            )
            # Choose attributes based on the selected right entity
            if right_entity == 'lead':
                right_attribute_options = st.session_state.get('lead_attributes', [])
            else:
                right_attribute_options = st.session_state.get('counsellor_attributes', [])
            right_attribute = st.selectbox(
                "Right Attribute",
                options=right_attribute_options,
                index=right_attribute_options.index(condition['right'].get('attribute', right_attribute_options[0])) if condition['right'].get('attribute', None) in right_attribute_options else 0,
                key=f"right_attr_{condition['id']}"
            )
            condition['right'] = {'entity': right_entity, 'attribute': right_attribute}

    # Update condition
    condition['left'] = {'entity': left_entity, 'attribute': left_attribute}
    condition['operator'] = operator

# Function to display a single condition
def display_condition(condition, idx, rule_id):
    st.markdown(f"**Condition {idx + 1}**")
    col1, col2, col3  = st.columns(3)
    with col1:
        left_entity = st.selectbox(
            "Left Entity",
            ["lead", "counsellor"],
            index=["lead", "counsellor"].index(condition['left'].get('entity', 'lead')),
            key=f"left_entity_{condition['id']}"
        )
        # Choose attributes based on the selected left entity
        if left_entity == 'lead':
            left_attribute_options = st.session_state.get('lead_attributes', [])
        else:
            left_attribute_options = st.session_state.get('counsellor_attributes', [])
        left_attribute = st.selectbox(
            "Left Attribute",
            options=left_attribute_options,
            index=left_attribute_options.index(condition['left'].get('attribute', left_attribute_options[0])) if condition['left'].get('attribute', None) in left_attribute_options else 0,
            key=f"left_attr_{condition['id']}"
        )
        
    with col2:
        operator_options = ["==", "!=", ">", "<", ">=", "<=", "in", "not in"]
        operator = st.selectbox(
            "Operator",
            operator_options,
            index=operator_options.index(condition.get('operator', '==')),
            key=f"operator_{condition['id']}"
        )
    with col3:
        right_type_options = ["Value", "Attribute"]
        is_attribute = 'attribute' in condition['right']
        right_type = st.selectbox(
            "Right Type",
            right_type_options,
            index=1 if is_attribute else 0,
            key=f"right_type_{condition['id']}"
        )
        if right_type == "Value":
            right_value = st.text_input(
                "Right Value",
                value=str(condition['right'].get('value', '')),
                key=f"right_value_{condition['id']}"
            )
            condition['right'] = {'value': right_value}
        else:
            right_entity = st.selectbox(
                "Right Entity",
                ["lead", "counsellor"],
                index=["lead", "counsellor"].index(condition['right'].get('entity', 'lead')),
                key=f"right_entity_{condition['id']}"
            )
            # Choose attributes based on the selected right entity
            if right_entity == 'lead':
                right_attribute_options = st.session_state.get('lead_attributes', [])
            else:
                right_attribute_options = st.session_state.get('counsellor_attributes', [])
            right_attribute = st.selectbox(
                "Right Attribute",
                options=right_attribute_options,
                index=right_attribute_options.index(condition['right'].get('attribute', right_attribute_options[0])) if condition['right'].get('attribute', None) in right_attribute_options else 0,
                key=f"right_attr_{condition['id']}"
            )
            condition['right'] = {'entity': right_entity, 'attribute': right_attribute}

    # Update condition
    condition['left'] = {'entity': left_entity, 'attribute': left_attribute}
    condition['operator'] = operator

def display_conditions(conditions, parent_condition):
    for idx, condition in enumerate(conditions):
        if 'conditions' in condition:
            # Nested condition group
            st.markdown(f"**Nested Condition Group {idx + 1}**")
            sub_logic = st.selectbox(
                "Sub-Logic",
                ["AND", "OR"],
                index=["AND", "OR"].index(condition.get('logic', 'AND')),
                key=f"sub_logic_{condition['id']}"
            )
            condition['logic'] = sub_logic
            # Display the conditions within this group
            display_conditions(condition['conditions'], parent_condition=condition)
        else:
            # Display a single condition
            display_condition(condition, idx, rule_id=parent_condition['id'])
        # Delete condition or condition group
        if st.button("Delete Condition", key=f"delete_condition_{condition['id']}"):
            conditions.pop(idx)
            st.rerun()
    # Add new condition and nested condition group within this group
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add New Condition", key=f"add_condition_{parent_condition['id']}"):
            new_condition = {
                'id': str(uuid.uuid4()),
                'left': {'entity': 'lead', 'attribute': ''},
                'operator': '==',
                'right': {'value': ''}
            }
            conditions.append(new_condition)
            st.rerun()
    with col2:
        if st.button("Add New Nested Condition Group", key=f"add_nested_group_{parent_condition['id']}"):
            new_nested_group = {
                'id': str(uuid.uuid4()),
                'conditions': [],
                'logic': 'AND'
            }
            conditions.append(new_nested_group)
            st.rerun()

def initialize_rules():
    if 'rules' not in st.session_state:
        # No rules uploaded, load default rules if available
        try:
            with open('default_rules.json', 'r') as f:
                rules_data = json.load(f)
            for rule in rules_data:
                rule['id'] = str(uuid.uuid4())
                assign_condition_ids(rule['conditions'])
            st.session_state['rules'] = rules_data
        except FileNotFoundError:
            st.session_state['rules'] = []

def display_rules():
    st.header("⚙️ Rule Management 🔧")
    rules = st.session_state['rules']

    # Display existing rules with rule numbers
    for idx, rule in enumerate(rules, start=1):
        # Use the 'description' field and include the rule number
        with st.expander(f"🔹 **Rule {idx}**: {rule.get('description', 'No Description')}", expanded=False):
            # Store the rule number in the rule data
            rule['number'] = idx

            # Edit rule description
            description = st.text_input(
                "Rule Description",
                value=rule.get('description', ''),
                key=f"description_{rule['id']}"
            )
            rule['description'] = description

            # Edit rule logic
            logic = st.selectbox(
                "Logic",
                ["AND", "OR"],
                index=["AND", "OR"].index(rule.get('logic', 'AND')),
                key=f"logic_{rule['id']}"
            )
            rule['logic'] = logic

            # Edit rule weight
            weight = st.number_input(
                "Weight",
                min_value=0.0,
                value=float(rule.get('weight', 1.0)),
                key=f"weight_{rule['id']}"
            )
            rule['weight'] = weight

            # Display and edit conditions
            conditions = rule['conditions']
            display_conditions(conditions, parent_condition=rule)

            # Delete rule
            if st.button("Delete Rule", key=f"delete_rule_{rule['id']}"):
                st.session_state['rules'] = [r for r in st.session_state['rules'] if r['id'] != rule['id']]
                st.rerun()

    # Add new rule
    if st.button("➕ Add New Rule"):
        new_rule = {
            'id': str(uuid.uuid4()),
            'description': 'New Rule Description',
            'conditions': [],
            'logic': 'AND',
            'weight': 1.0
        }
        st.session_state['rules'].append(new_rule)
        st.rerun()

    # Save rules to JSON
    if st.button("💾 Save Rules to JSON"):
        rules_to_save = copy.deepcopy(st.session_state['rules'])
        # Remove 'id' fields before saving
        for rule in rules_to_save:
            rule.pop('id', None)
            rule.pop('number', None)  # Remove the rule number before saving
            remove_condition_ids(rule['conditions'])
        json_data = json.dumps(rules_to_save, indent=4)
        st.download_button(
            label="Download Rules JSON",
            data=json_data,
            file_name='rules.json',
            mime='application/json',
        )
        # Re-add 'id' fields after saving
        for idx, rule in enumerate(st.session_state['rules'], start=1):
            rule['id'] = str(uuid.uuid4())
            rule['number'] = idx  # Update rule numbers
            assign_condition_ids(rule['conditions'])

def main():
    st.title("🎓 SuperLEAP: University Lead-Counsellor Matching System 🤝")

    # Initialize attribute lists
    if 'lead_attributes' not in st.session_state:
        st.session_state['lead_attributes'] = []
    if 'counsellor_attributes' not in st.session_state:
        st.session_state['counsellor_attributes'] = []

    st.sidebar.header("⬆️ Upload Data")
    # leads_file = st.sidebar.file_uploader("Upload Leads CSV/XLSX", type=["csv"])
    # counsellors_file = st.sidebar.file_uploader("Upload Counsellors CSV", type=["csv"])
    # uploaded_rules_file = st.sidebar.file_uploader("Upload Rules JSON", type=["json"])
    leads_file = st.sidebar.file_uploader("Upload Leads CSV/XLSX",  type=["csv", "xlsx"])
    counsellors_file = st.sidebar.file_uploader("Upload Counsellors CSV/XLSX", type=["csv", "xlsx"])
    uploaded_rules_file = st.sidebar.file_uploader("Upload Rules JSON")

    # Process uploaded rules file
    if uploaded_rules_file is not None:
        # Read file content
        uploaded_rules_content = uploaded_rules_file.getvalue()
        # Compute hash
        uploaded_rules_hash = hashlib.md5(uploaded_rules_content).hexdigest()
        if 'last_uploaded_rules_hash' not in st.session_state or st.session_state['last_uploaded_rules_hash'] != uploaded_rules_hash:
            try:
                uploaded_rules = json.loads(uploaded_rules_content.decode('utf-8'))
                st.session_state['last_uploaded_rules_hash'] = uploaded_rules_hash
                st.success("Rules loaded successfully.")
                # Assign unique IDs to rules and conditions for tracking
                rules_data = uploaded_rules
                for rule in rules_data:
                    rule['id'] = str(uuid.uuid4())
                    assign_condition_ids(rule['conditions'])
                st.session_state['rules'] = rules_data
                st.rerun()
            except json.JSONDecodeError:
                st.error("Invalid JSON file.")
    else:
        # If no file uploaded, clear 'last_uploaded_rules_hash' to allow re-upload
        st.session_state.pop('last_uploaded_rules_hash', None)

    if leads_file and counsellors_file:
        # Load leads and counsellors data
        # leads_df = pd.read_csv(leads_file)
        # counsellors_df = pd.read_csv(counsellors_file)

        # Determine file type for leads_file
        leads_file_extension = os.path.splitext(leads_file.name)[1].lower()
        if leads_file_extension == '.csv':
            leads_df = pd.read_csv(leads_file)
        elif leads_file_extension in ['.xls', '.xlsx']:
            leads_df = pd.read_excel(leads_file)
        else:
            st.error("Unsupported file type for leads file.")
            return

        # Determine file type for counsellors_file
        counsellors_file_extension = os.path.splitext(counsellors_file.name)[1].lower()
        if counsellors_file_extension == '.csv':
            counsellors_df = pd.read_csv(counsellors_file)
        elif counsellors_file_extension in ['.xls', '.xlsx']:
            counsellors_df = pd.read_excel(counsellors_file)
        else:
            st.error("Unsupported file type for counsellors file.")
            return
        ################# only for testing
        leads_df = leads_df.head(int(0.1*93))
        #print(leads_df)

        
        leads_df = process_lead_df(leads_df)
        counsellors_df = process_counsellor_df(counsellors_df)
        print("<><><><><><><><><> Counsellors")
        print(counsellors_df.columns)


        # Update attribute lists
        st.session_state['lead_attributes'] = leads_df.columns.tolist()
        st.session_state['counsellor_attributes'] = counsellors_df.columns.tolist()


        # Initialize rules
        initialize_rules()

        # Display and edit rules
        display_rules()

        # Load data
        leads = load_leads(leads_df)
        counsellors = load_counsellors(counsellors_df)

        # Initialize the rule engine with updated rules
        rules_data = st.session_state['rules']
        # Remove 'id' and 'description' fields before passing to RuleEngine
        rules_for_engine = []
        for rule in rules_data:
            rule_copy = copy.deepcopy(rule)  # Use deepcopy to prevent modifying the original
            rule_copy.pop('id', None)
            rule_copy.pop('description', None)
            remove_condition_ids(rule_copy['conditions'])
            rules_for_engine.append(rule_copy)
        rule_engine = RuleEngine(rules_for_engine)

        if st.button("🚀 Run Lead-Counsellor Matching Method"):
            results = []
            # Collect all rule descriptions
            rule_descriptions = [rule.get('description', f"Rule_{i+1}") for i, rule in enumerate(rules_for_engine)]
            for lead in leads:
                for counsellor in counsellors:
                    score, rule_contributions = rule_engine.calculate_score(lead, counsellor)
                    # results.append({
                    #     'Lead ID': lead.id,
                    #     'Lead Name': lead.name,
                    #     'Counsellor ID': counsellor.id,
                    #     'Counsellor Name': counsellor.name,
                    #     'Matching Score': score
                    # })
 
                    # result_row = {
                    #     'Lead ID': lead.id,
                    #     'Lead Name': lead.name,
                    #     'Counsellor ID': counsellor.id,
                    #     'Counsellor Name': counsellor.name,
                    #     'Matching Score': score
                    # }
                    #print(lead)

                    result_row = {
                        
                        #'Lead ID': getattr(lead, 'JO LeadID', None) if getattr(lead, 'JO LeadID', None) else getattr(lead, 'id', None),
                        'Lead ID': getattr(lead, 'User Id', None) if getattr(lead, 'User Id', None) else getattr(lead, 'id', None),
                        'Lead Name': getattr(lead, 'Registered Name', None) if getattr(lead, 'Registered Name', None) else lead.name,
                        'Counsellor ID': getattr(counsellor, 'Employee ID', None) if getattr(counsellor, 'Employee ID', None) else getattr(counsellor, 'id', None),
                        'Counsellor Name': getattr(counsellor, 'Employee Name', None) if getattr(counsellor, 'Employee Name', None) else getattr(counsellor, 'name', None),
                        'Matching Score': score
                    }
                    # Add contributions from each rule
                    for desc in rule_descriptions:
                        result_row[desc] = rule_contributions.get(desc, 0)
                    #print(result_row)
                    #if int(score) > 0:
                    results.append(result_row)

            results_df = pd.DataFrame(results)
            print("############################")
            print(results_df)
            # Sort results by Matching Score in descending order
            #results_df = results_df.sort_values(by=['Lead ID', 'Matching Score'], ascending=[True, False])
            if not results_df.empty:
                results_df = results_df.sort_values(by=['Lead ID', 'Matching Score'], ascending=[True, False])
            else:
                results_df = pd.DataFrame()
            st.header("📊 Lead-Counsellor Pair Scores 🔍")

            # Highlight the top match for each lead
            def highlight_top_matches(df):
                if df.empty:
                    return df
                df_copy = df.copy()
                df_copy['Is Top Match'] = df_copy.groupby('Lead ID')['Matching Score'].transform('max') == df_copy['Matching Score']
                return df_copy

            results_df = highlight_top_matches(results_df)

            # Display the DataFrame with conditional formatting
            st.dataframe(
                results_df.style.apply(
                    lambda x: ['background-color: lightgreen' if x['Is Top Match'] else '' for _ in x],
                    axis=1
                )
            )

            matching_scores_dict = matching_scores_dictionary(results_df)
            # Rename a column
            counsellors_df_new = counsellors_df.rename(columns={'Employee ID': 'id'})
            leads_df_new = leads_df.rename(columns={'User Id': 'id'})
            capacities_dict = capacities_dictionary(counsellors_df_new)

            assignment = allocate_leads(leads_df_new, counsellors_df_new, matching_scores_dict, capacities_dict)
            # Create DataFrame for assignment results
            assignment_df = pd.DataFrame([
                {
                    'Lead ID': lead_id,
                    'Lead Name': leads_df_new.loc[leads_df_new['id'] == lead_id, 'Registered Name'].values[0],
                    'Counsellor ID': counsellor_id,
                    'Counsellor Name': counsellors_df_new.loc[counsellors_df_new['id'] == counsellor_id, 'Employee Name'].values[0]
                }
                for lead_id, counsellor_id in assignment.items()
            ])
            st.header("📊 Final Lead Allocation Results")
            st.table(assignment_df)

            # Optionally, allow downloading the results
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name='matching_results.csv',
                mime='text/csv',
            )
    else:
        st.info("Please upload (see left panel) both Leads and Counsellors CSV or XLSX files.")

if __name__ == '__main__':
    main()