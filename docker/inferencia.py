import sys
import joblib
import logging
import numpy as np
import pandas as pd
from sys import stdout
import tensorflow as tf
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(filename)s: %(message)s")
console_handler = logging.StreamHandler(stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info("Inicio de inferencia")

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "files" / "input.csv"
OUTPUT_FILE = BASE_DIR / "files" / "output.csv"

metadata = joblib.load(BASE_DIR / "preprocessing_metadata.joblib")
wind_stats = metadata["wind_stats"]
numeric_stats = metadata["numeric_stats"]
wind_thresholds = metadata["wind_thresholds"]
rainfall_extreme_threshold = metadata["rainfall_extreme_threshold"]

logger.info("Metadata cargada")

preprocessor = joblib.load(BASE_DIR / "preprocessor.joblib")
knn_scaler = joblib.load(BASE_DIR / "knn_scaler.joblib")
knn_imputer = joblib.load(BASE_DIR / "knn_imputer.joblib")
final_columns = joblib.load(BASE_DIR / "final_columns.joblib")
threshold = joblib.load(BASE_DIR / "threshold.joblib")
model = tf.keras.models.load_model(BASE_DIR / "modelo_final.keras")

logger.info("Artefactos cargados correctamente")

df = pd.read_csv(INPUT_FILE)
clima = df.copy()
clima = clima.drop(columns=["Unnamed: 0", "RainfallTomorrow", "RainTomorrow"], errors="ignore")
clima["Date"] = pd.to_datetime(clima["Date"])
clima["Month"] = clima["Date"].dt.month
clima["Month_sin"] = np.sin(2*np.pi*clima["Month"]/12)
clima["Month_cos"] = np.cos(2*np.pi*clima["Month"]/12)
clima = clima.drop(columns=["Date"])
clima["Rainfall"] = clima["Rainfall"].fillna(0)
clima["RainToday"] = clima["RainToday"].fillna("No")
cols_flag = ['Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Temp9am', 'Temp3pm', 'Cloud9am', 'Cloud3pm', 'Evaporation', 'Sunshine']

for c in cols_flag:
  clima[c + "_missing"] = clima[c].isna().astype(int)

def imputar_cascada(X, col, stat_loc_month, stat_loc, stat_global):
  keys = pd.MultiIndex.from_arrays([X["Location"].values, X["Month"].values])
  vals = stat_loc_month.reindex(keys).values
  X[col] = X[col].fillna(pd.Series(vals, index=X.index))
  X[col] = X[col].fillna(X["Location"].map(stat_loc))
  X[col] = X[col].fillna(stat_global)

for c in wind_stats:
  s = wind_stats[c]
  imputar_cascada(clima, c, s["loc_month"], s["loc"], s["global"])

for c in numeric_stats:
  s = numeric_stats[c]
  imputar_cascada(clima, c, s["loc_month"], s["loc"], s["global"])

cols_mediana = ['MinTemp', 'MaxTemp', 'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm', 'Temp9am', 'Temp3pm']
cols_knn = ['Pressure9am', 'Pressure3pm', 'Evaporation', 'Sunshine', 'Cloud9am', 'Cloud3pm']
cols_contexto = (cols_mediana + ['Rainfall'] + cols_knn)

logger.info("Aplicando escalado para KNN")

scaled = knn_scaler.transform(clima[cols_contexto])

logger.info("Aplicando KNN Imputer")

scaled = knn_imputer.transform(scaled)

tmp = pd.DataFrame(knn_scaler.inverse_transform(scaled), columns=cols_contexto, index=clima.index)
clima[cols_knn] = tmp[cols_knn]

for c in ['Cloud9am', 'Cloud3pm']:
  clima[c] = np.clip(np.round(clima[c]), 0, 8)

clima["RainToday"] = (clima["RainToday"].map({"Yes": 1, "No": 0}).astype(int))
clima = clima.drop(columns=["Location", "Month"])
clima = pd.get_dummies(clima, columns=["WindGustDir", "WindDir9am", "WindDir3pm"])

cols_viento = ["WindGustSpeed", "WindSpeed9am", "WindSpeed3pm"]
for c in cols_viento:
  umbral_99 = wind_thresholds[c]
  clima[c + "_Extreme"] = (clima[c] > umbral_99).astype(int)
  clima[c] = np.clip(clima[c], a_min=None, a_max=umbral_99)

clima["Rainfall_Extreme"] = (clima["Rainfall"] > rainfall_extreme_threshold).astype(int)
clima["Rainfall"] = np.log1p(clima["Rainfall"])
clima["Evaporation"] = np.log1p(clima["Evaporation"])
clima["Delta_Pressure"] = (clima["Pressure3pm"] - clima["Pressure9am"])
clima["Delta_Humidity"] = (clima["Humidity3pm"] - clima["Humidity9am"])
clima["Delta_Temp"] = (clima["Temp3pm"] - clima["Temp9am"])
clima = clima.reindex(columns=final_columns, fill_value=0)

X = preprocessor.transform(clima)
X = np.asarray(X, dtype=np.float32)

logger.info("Ejecutando predicciones")

probs = model.predict(X, verbose=1)
preds = (probs >= threshold).astype(int)
resultado = pd.DataFrame({"RainTomorrow_Pred": preds.flatten()})
resultado.to_csv(OUTPUT_FILE,index=False)

logger.info(f"Predicciones guardadas en {OUTPUT_FILE}")