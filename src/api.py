import pandas as pd
from fastapi import FastAPI
from pydantic import create_model
from xgboost import XGBRegressor

from src.data import UTILES

Medicion = create_model("Medicion", **{c: (float, ...) for c in UTILES})

modelo = XGBRegressor()
modelo.load_model("models/xgb_rul.json")

app = FastAPI(title="RUL de motores turbofan")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(m: Medicion):
    fila = pd.DataFrame([m.model_dump()])[UTILES]
    rul = float(modelo.predict(fila)[0])
    return {"rul_estimada_ciclos": round(rul, 1)}