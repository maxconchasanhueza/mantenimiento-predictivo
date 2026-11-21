# Mantenimiento predictivo: vida útil restante (RUL) de motores turbofan

Modelos para estimar cuántos ciclos le quedan a un motor antes de fallar, con el
dataset NASA C-MAPSS (subconjunto FD001, datos simulados), y una simulación de
costo de falla vs. mantenimiento anticipado.

## Resultados (test oficial FD001, 100 motores, último ciclo de cada uno)

| Modelo | RMSE (ciclos) | MAE (ciclos) |
|---|---|---|
| Regresión lineal | 21,9 | 17,6 |
| Random Forest | 18,1 | 13,0 |
| XGBoost | 18,5 | 13,1 |

- Los modelos de árboles mejoran a la lineal en ~15-17% de RMSE.
- Random Forest y XGBoost quedan empatados (0,4 de diferencia con 100 motores).
- Se entrena con la RUL limitada a 125 ciclos (convención habitual en este dataset)
  y se evalúa contra la RUL real, sin limitar.

## Metodología

- **Validación sin fuga de información:** los motores se separan completos
  (80 train / 20 validación), nunca filas sueltas del mismo motor en ambos lados.
- **Comparación contra líneas base:** media y regresión lineal antes de modelos complejos.
- **Hiperparámetros:** validación cruzada por motor (`GroupKFold`, 5 grupos).
- **Explicabilidad:** SHAP sobre Random Forest. Sensores más influyentes:
  s11, s9, s4, s12 y s7.

## Lo que no funcionó

- Ajustar profundidad y tasa de aprendizaje de XGBoost: RMSE entre 18,38 y 18,86
  en validación cruzada, diferencias dentro del ruido (±1,6).
- Promedios móviles de 5, 10, 20 y 30 ciclos: sin mejora clara (18,14 a 18,44
  contra 18,38 sin ventana).
- SHAP no funcionó con XGBoost 3.2 + SHAP 0.49 (error de versiones), por eso
  se explicó Random Forest, que rinde parecido.

## Análisis de costo (ilustrativo)

Supuestos **inventados** para ilustrar: falla = 100, intervención = 10,
horizonte de falla = 30 ciclos. Regla: intervenir si la RUL predicha es menor
que un umbral.

- Nunca intervenir: 2.500. Intervenir siempre: 1.000.
- Con umbral de 80 ciclos el costo baja a 450.
- El umbral se miró sobre el test, así que es un análisis de sensibilidad,
  no un umbral validado. En el test, 25 de 100 motores estaban cerca de la falla,
  más que en una flota real.

## Limitaciones

- Datos simulados y un solo subconjunto (FD001).
- Una sola partición de validación y un único test de 100 motores.


## Cómo reproducirlo

1. `pip install -r requirements.txt`
2. Descargar C-MAPSS (NASA Prognostics Center of Excellence) y dejar los archivos en `data/`.
3. Ejecutar `notebooks/01_eda.ipynb` y luego `notebooks/02_modelos.ipynb`.


## API y Docker

Entrenar el modelo (genera `models/xgb_rul.json`):

    python -m src.train

Construir y ejecutar la API en contenedor:

    docker build -t rul-api .
    docker run -p 8000:8000 rul-api

Documentación interactiva en `http://127.0.0.1:8000/docs`. Rutas: `GET /health`
y `POST /predict` (17 variables de entrada, devuelve la RUL estimada en ciclos).
La API rechaza con error 422 entradas incompletas o con tipos incorrectos.

Verificación de ejemplo: motor 34 del test (RUL real 7), estimada 6,6. Es un
caso extremo elegido para comprobar el servicio; las métricas del proyecto son
las de la tabla de resultados.

## Próximos pasos

Despliegue en la nube y pruebas automáticas.