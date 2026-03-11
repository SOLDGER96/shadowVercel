from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date, timedelta

app = FastAPI(title="Shadow Date Decoder")

# Enable CORS so the frontend can make requests to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace "*" with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the expected request body
class DecodeRequest(BaseModel):
    days_since_epoch: int = Field(..., description="Days since Jan 1, 1970")

@app.post("/api/decode")
def decode_shadow_date(request: DecodeRequest):
    """
    Takes the number of days since the Unix Epoch and returns the exact date.
    """
    # Validation: Ensure it's not a negative number
    if request.days_since_epoch < 0:
        raise HTTPException(status_code=400, detail="Days since epoch must be a positive integer.")
    
    # Base Unix Epoch date
    epoch_start = date(1970, 1, 1)
    
    # Calculate the exact date
    calculated_date = epoch_start + timedelta(days=request.days_since_epoch)
    
    return {
        "last_password_change": str(calculated_date)
    }

