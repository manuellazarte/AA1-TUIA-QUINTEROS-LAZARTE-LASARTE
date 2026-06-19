# Deployment con Docker

## Construcción de la imagen

```bash
docker build -t weather-predictor .
```

## Ejecución del contenedor

```bash
docker run --rm \
-v $(pwd):/data \
weather-predictor \
/data/weatherAUS_2026C1.csv
```

## Salida

El script genera un archivo:

```text
predicciones.csv
```

con una columna:

```text
RainTomorrow_Pred
```

donde:

* 0 = No lloverá mañana
* 1 = Lloverá mañana

```
```
