# Deployment con Docker

Todos los comandos deben ejecutarse desde la carpeta `docker` del repositorio.

## Estructura esperada

```text
docker/
│
├── inferencia.py
├── Dockerfile
├── requirements.txt
├── modelo_final.keras
├── preprocessing_metadata.joblib
├── preprocessor.joblib
├── knn_scaler.joblib
├── knn_imputer.joblib
├── final_columns.joblib
├── threshold.joblib
│
└── files/
    ├── input.csv
    └── output.csv
```

El archivo de entrada debe colocarse en:

```text
files/input.csv
```

Las predicciones serán guardadas automáticamente en:

```text
files/output.csv
```

---

## Construcción de la imagen

```bash
docker build -t weather-rain .
```

---

## Ejecución del contenedor

### Opción 1: utilizando los archivos incluidos en la imagen

```bash
docker run --rm weather-rain
```

### Opción 2: compartiendo la carpeta `files` con el host

Linux / macOS:

```bash
docker run --rm -v "$(pwd)/files:/app/files" weather-rain
```

Windows PowerShell:

```powershell
docker run --rm -v "${PWD}/files:/app/files" weather-rain
```

De esta manera, el archivo `output.csv` generado por el contenedor quedará disponible directamente en la carpeta local `files`.

---

## Entrada

El archivo `input.csv` debe contener las mismas columnas utilizadas durante el entrenamiento del modelo climático.

Ejemplo:

```text
Date
Location
MinTemp
MaxTemp
Rainfall
Evaporation
Sunshine
WindGustDir
WindGustSpeed
WindDir9am
WindDir3pm
WindSpeed9am
WindSpeed3pm
Humidity9am
Humidity3pm
Pressure9am
Pressure3pm
Cloud9am
Cloud3pm
Temp9am
Temp3pm
RainToday
```

Las columnas objetivo (`RainTomorrow` y `RainfallTomorrow`) son opcionales y serán ignoradas durante la inferencia si están presentes.

---

## Salida

El script genera un archivo:

```text
output.csv
```

con una columna:

```text
RainTomorrow_Pred
```

donde:

- `0` = No lloverá mañana.
- `1` = Lloverá mañana.

Ejemplo:

```text
RainTomorrow_Pred
0
0
1
0
1
```

---

## Modelo utilizado

Se utiliza una red neuronal entrenada con TensorFlow y optimizada mediante búsqueda de hiperparámetros. Durante la inferencia se aplican automáticamente todas las etapas de preprocesamiento utilizadas durante el entrenamiento:

- Imputación básica de valores faltantes.
- Imputación en cascada por ubicación y mes.
- Imputación KNN para variables meteorológicas seleccionadas.
- Creación de variables indicadoras de valores faltantes.
- Codificación cíclica de la fecha.
- One-Hot Encoding de variables categóricas.
- Ingeniería de características.
- Escalado de variables numéricas.
- Aplicación del umbral óptimo de clasificación.