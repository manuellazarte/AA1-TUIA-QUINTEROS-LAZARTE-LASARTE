# Australia Rain Prediction

Proyecto de **Machine Learning para predecir si lloverá al día siguiente en Australia**, desarrollado como trabajo práctico de la materia Aprendizaje Automático 1.

El proyecto aborda un problema de **clasificación binaria** utilizando datos meteorológicos de Australia y compara diferentes estrategias de modelado y preprocesamiento.

## Descripción general

El objetivo es predecir la variable `RainTomorrow`, indicando si se espera lluvia al día siguiente:

* `0` → No lloverá.
* `1` → Lloverá.

El proyecto incluye análisis y preprocesamiento de datos, ingeniería de características, entrenamiento de modelos de clasificación y evaluación de resultados.

## Preprocesamiento

El pipeline incluye diferentes etapas para preparar los datos:

* Tratamiento de valores faltantes.
* Imputación por ubicación y mes.
* Imputación mediante **KNN** para variables meteorológicas seleccionadas.
* Creación de variables indicadoras de valores faltantes.
* Ingeniería de características.
* Codificación cíclica de variables relacionadas con fechas.
* One-Hot Encoding de variables categóricas.
* Escalado de variables numéricas.

Para la inferencia se conservan los artefactos necesarios del pipeline de preprocesamiento, permitiendo aplicar las mismas transformaciones utilizadas durante el entrenamiento.

## Modelado

El proyecto trabaja con modelos de clasificación y una red neuronal desarrollada con **TensorFlow/Keras**.

El modelo final utiliza un **umbral de clasificación optimizado**, almacenado junto con los demás artefactos necesarios para realizar inferencias.

## Inferencia con Docker

El proyecto incluye una implementación para ejecutar el modelo mediante Docker sin necesidad de configurar manualmente el entorno de Machine Learning.

### Construcción

Desde la carpeta `docker`:

```bash
docker build -t weather-rain .
```

### Ejecución

Utilizando los archivos incluidos en la imagen:

```bash
docker run --rm weather-rain
```

O compartiendo la carpeta de archivos con el sistema local.

**Windows PowerShell:**

```powershell
docker run --rm -v "${PWD}/files:/app/files" weather-rain
```

**Linux / macOS:**

```bash
docker run --rm -v "$(pwd)/files:/app/files" weather-rain
```

El archivo de entrada debe ubicarse en:

```text
docker/files/input.csv
```

y las predicciones generadas se guardan en:

```text
docker/files/output.csv
```

El resultado contiene la columna:

```text
RainTomorrow_Pred
```

## Ejecución del proyecto

Para trabajar con la notebook, crear un entorno virtual desde la raíz del repositorio:

```bash
python -m venv .venv
```

En Linux:

```bash
python3 -m venv .venv
```

Activar el entorno:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate
```

**Linux**

```bash
source ./.venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Tecnologías

* Python
* Pandas
* NumPy
* Scikit-learn
* TensorFlow / Keras
* Matplotlib
* Seaborn
* Joblib
* Docker
* Jupyter Notebook

## Estructura principal

```text
├── docker/
│   ├── Dockerfile
│   ├── inferencia.py
│   ├── requirements.txt
│   ├── modelo_final.keras
│   ├── preprocessing_metadata.joblib
│   ├── preprocessor.joblib
│   ├── knn_scaler.joblib
│   ├── knn_imputer.joblib
│   ├── final_columns.joblib
│   ├── threshold.joblib
│   └── files/
│       └── input.csv
│
├── files/
├── TP_clasificacion_AA1.ipynb
├── requirements.txt
├── weatherAUS_2026C1.csv
└── README.md
```

## Contexto académico

Proyecto desarrollado en el marco de la materia **Aprendizaje Automático 1** de la **Tecnicatura Universitaria en Inteligencia Artificial (TUIA)** de la **Universidad Nacional de Rosario**.

Proyecto realizado de manera grupal por:

* Manuel Lazarte
* Facundo Quinteros
* Rober Lasarte
