import traceback
import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Load the trained pipeline (SVM + preprocessing)
with open('svm_pipeline.pkl', 'rb') as fp:
    model = pickle.load(fp)

# Initialize FastAPI app
app = FastAPI(title='Heart Disease API')

# Define input schema
class ClinicalInformation(BaseModel):
    age: float
    sex: int
    cp: int
    trestbps: float
    chol: float
    fbs: int
    restecg: int
    thalach: float
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

@app.post("/heart-disease-predictor")
def predict_disease(inputs: ClinicalInformation):
    try:
        input_df = pd.DataFrame([inputs.dict()])
        print("Input received:\n", input_df)

        prediction = model.predict(input_df)
        print("Prediction result:", prediction)

        return {
            "prediction": (
                "The patient does NOT have symptoms of a heart attack."
                if prediction[0] == 0
                else "The patient is having symptoms of a heart attack."
            )
        }

    except Exception as e:
        print("Internal server error:")
        traceback.print_exc()  # This prints the full traceback
        return {"error": str(e)}
