import pandas as pd
from lead import Lead
from counsellor import Counsellor
from rule_engine import RuleEngine

# Function to load leads from CSV or Excel file
def load_leads(file_path):
    df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
    leads = []
    for _, row in df.iterrows():
        lead = Lead(
            id=row['id'],
            name=row['name'],
            location=row['location'],
            course_interest=row['course_interest'],
            language=row['language'],
            engagement_level=row['engagement_level'],
            decision_stage=row['decision_stage']
        )
        leads.append(lead)
    return leads

# Function to load counsellors from CSV or Excel file
def load_counsellors(file_path):
    df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
    counsellors = []
    for _, row in df.iterrows():
        counsellor = Counsellor(
            id=row['id'],
            name=row['name'],
            location=row['location'],
            specialization=row['specialization'],
            language=row['language'],
            conversion_rate=float(row['conversion_rate']),
            workload=int(row['workload'])
        )
        counsellors.append(counsellor)
    return counsellors

def main():
    # Load leads and counsellors from CSV or Excel files
    leads = load_leads('leads.csv')  # Change to 'leads.xlsx' if using Excel
    counsellors = load_counsellors('counsellors.csv')  # Change to 'counsellors.xlsx' if using Excel

    # Initialize the rule engine with external rules
    rule_engine = RuleEngine('rules.json')

    # Apply matching for each lead
    for lead in leads:
        best_counsellor = rule_engine.apply_rules(lead, counsellors)
        print(f"Lead {lead.name} matched with Counsellor {best_counsellor.name}")

if __name__ == '__main__':
    main()