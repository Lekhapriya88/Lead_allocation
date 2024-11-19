from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Define the input data models
class Lead(BaseModel):
    id: int
    # Add other lead attributes here (e.g., name, preferences)

class Counsellor(BaseModel):
    id: int
    # Add other counsellor attributes here (e.g., expertise, availability)

class PairScore(BaseModel):
    lead_id: int
    counsellor_id: int
    score: float

# Define the output data model
class PairingResponse(BaseModel):
    pairs: List[PairScore]

# Example function to process leads and counsellors
def pair_leads_with_counsellors(leads: List[Dict], counsellors: List[Dict]) -> List[Dict]:
    # Example processing logic here
    results = []
    for lead in leads:
        for counsellor in counsellors:
            score = calculate_score(lead, counsellor)  # Define this function based on your criteria
            results.append({"lead_id": lead["id"], "counsellor_id": counsellor["id"], "score": score})
    return results

# API endpoint
@app.post("/pair-leads-counsellors", response_model=PairingResponse)
async def pair_leads_counsellors(leads: List[Lead], counsellors: List[Counsellor]):
    # Convert pydantic models to dictionaries for processing
    leads_data = [lead.dict() for lead in leads]
    counsellors_data = [counsellor.dict() for counsellor in counsellors]

    # Call the pairing function
    pairs = pair_leads_with_counsellors(leads_data, counsellors_data)

    # Prepare response
    response = PairingResponse(pairs=pairs)
    return response

# Example score calculation function
def calculate_score(lead, counsellor):
    # Implement your scoring logic here
    return 1.0  # Example score