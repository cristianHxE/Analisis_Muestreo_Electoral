# Análisis de Muestreo Electoral — Ciudad de México 2024

**Inferencia estadística, muestreo probabilístico y simulaciones Monte Carlo con Python**

[English](README.md) | **Español**

## Descripción del proyecto

Este proyecto desarrolla e implementa métodos de muestreo estadístico utilizando datos de la elección para la Jefatura de Gobierno de la Ciudad de México de 2024.

El objetivo principal es estimar totales y proporciones de votos mediante muestras probabilísticas de casillas electorales, así como evaluar el comportamiento de los estimadores a través de simulaciones Monte Carlo.

El proyecto surge de un trabajo académico desarrollado originalmente en R y se está migrando progresivamente a Python, se esta poniendo especial atención a:

- Fundamentos matemáticos de los estimadores.
- Organización modular del código.
- Validación e integridad de los datos.
- Reproducibilidad de los experimentos.
- Evaluación estadística de los resultados.
- Implementación de pruebas automatizadas.

## Metodología estadística

### 1. Preparación e integración de datos

Se integran dos fuentes de información:

- Resultados electorales por casilla de la Ciudad de México.
- Identificación del distrito federal correspondiente a cada casilla.

La base electoral contiene **13,503 registros**. El archivo de identificación de distritos contiene información para 13,431 casillas.

Las 72 casillas restantes se clasifican mediante las siguientes reglas:

| Tipo de casilla | Cantidad | Criterio de asignación |
|---|---:|---|
| Voto en el extranjero | 12 | Distrito federal 0 |
| Voto anticipado | 54 | Distrito federal correspondiente a su sección |
| Personas en prisión preventiva | 6 | Distrito federal correspondiente a su sección |

Durante la integración se realizan comprobaciones para detectar llaves duplicadas, correspondencias ambiguas entre secciones y distritos, y registros sin identificación.

Posteriormente se construyen variables que representan los votos obtenidos por las candidaturas, considerando las combinaciones de partidos y coaliciones correspondientes.

### 2. Muestreo aleatorio simple sin reemplazo (MAS)

Se implementa un diseño de muestreo aleatorio simple sin reemplazo, donde la unidad de muestreo es la casilla electoral.

Para el análisis actual se excluyen las 12 casillas de voto en el extranjero, obteniendo una población de estudio de:

$$
N=13\,491.
$$

Cada muestra de tamaño $n$ se selecciona con igual probabilidad entre los subconjuntos posibles de la población.

La probabilidad de inclusión de una casilla es:

$$
\pi_i=\frac{n}{N}.
$$

### 3. Estimación de totales

Para estimar el total poblacional de votos de una candidatura se utiliza:

$$
\widehat T_y=N\overline y_s,
$$

donde $\overline y_s$ es la media muestral de votos por casilla.

La varianza se estima mediante:

$$
\widehat{\operatorname{Var}}(\widehat T_y)
=N^2\left(1-\frac{n}{N}\right)\frac{s_y^2}{n}.
$$

La expresión incorpora la corrección por población finita.

### 4. Estimación de proporciones mediante razones

Para estimar la proporción de votos obtenidos por una candidatura se utiliza el estimador de razón:

$$
\widehat R=\frac{\sum_{i\in s}y_i}{\sum_{i\in s}x_i},
$$

donde:

- $y_i$: votos obtenidos por la candidatura en la casilla $i$.
- $x_i$: total de votos registrados en la casilla $i$.

La varianza aproximada se calcula mediante linealización de Taylor, utilizando los residuos:

$$
e_i=y_i-\widehat R x_i.
$$

De esta forma:

$$
\widehat{\operatorname{Var}}(\widehat R)
=\left(1-\frac{n}{N}\right)\frac{s_e^2}{n\overline x_s^2}.
$$

Se construyen intervalos de confianza aproximados mediante cuantiles de la distribución normal.

### 5. Simulaciones Monte Carlo

Se realizan simulaciones repetidas de muestreo aleatorio simple para estudiar el comportamiento de los estimadores.

Los experimentos incluyen:

- Sesgo empírico.
- Varianza empírica.
- Error cuadrático medio (MSE).
- Raíz del error cuadrático medio (RMSE).
- Comparación entre varianza empírica y varianza linealizada promedio.
- Cobertura empírica de intervalos de confianza.

Se consideran los tamaños de muestra:

$$
n\in\{50,100,200,500,1000\},
$$

con 500 repeticiones para cada tamaño.

El objetivo es estudiar la relación entre el tamaño de muestra, la precisión de los estimadores y el comportamiento de los intervalos de confianza.

## Tecnologías utilizadas

- **Python:** implementación de los procedimientos estadísticos.
- **Pandas:** manipulación, integración y validación de datos.
- **NumPy:** operaciones numéricas y cálculos estadísticos.
- **Matplotlib:** visualización de resultados.
- **Pytest:** pruebas automatizadas de los estimadores.
- **Git y GitHub:** control de versiones y documentación del proyecto.

## Estructura del repositorio

```text
Analisis_Muestreo_Electoral/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── data_processed.py
│   ├── electoral_variables.py
│   ├── simple_random_sampling.py
│   └── estimadores.py
├── experiments/
│   ├── ratio_simulation.py
│   └── mas_precision.py
├── tests/
│   └── test_estimators.py
├── reports/
│   └── figures/
├── run_preparation.py
├── run_sampling.py
├── requirements.txt
├── README.md
├── README.es.md
└── .gitignore
```

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/cristianHxE/Analisis_Muestreo_Electoral.git
cd Analisis_Muestreo_Electoral
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo en Linux o macOS:

```bash
source .venv/bin/activate
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Datos

Los archivos originales no se incluyen en esta primera versión del repositorio.

Para reproducir el análisis es necesario disponer de:

- `2024_SEE_GOB_CDMX_CAS.csv`
- `DIS_FED_09.csv`

Los archivos deben colocarse en el directorio `data/raw/`.

La primera fuente corresponde a los resultados electorales por casilla. La segunda contiene la identificación de distritos federales utilizada en el proyecto académico.

La procedencia y las condiciones de redistribución de estos archivos deberán documentarse antes de incorporarlos al repositorio.

## Ejecución

### Preparación de los datos

Desde la raíz del proyecto:

```bash
python run_preparation.py
```

El programa integra los archivos originales, identifica los distritos federales y construye las variables electorales.

La base resultante se guarda en:

`data/processed/votos_cdmx_limpio.csv`

### Estimación mediante MAS

```bash
python run_sampling.py
```

Este script selecciona una muestra de casillas, calcula estimaciones de totales y proporciones, y compara los resultados con los parámetros poblacionales conocidos.

### Experimentos de simulación

Para ejecutar la simulación básica del estimador de razón:

```bash
python -m experiments.ratio_simulation
```

Para comparar distintos tamaños de muestra:

```bash
python -m experiments.mas_precision
```

El segundo experimento genera gráficas de varianza y cobertura en `reports/figures/`.

### Pruebas automatizadas

```bash
python -m pytest -v
```

Las pruebas permiten comprobar resultados numéricos conocidos y verificar el comportamiento de las funciones ante determinadas entradas inválidas.

## Estado del proyecto

**En desarrollo — versión inicial del portafolio.**

### Implementado

- Integración y validación de bases electorales.
- Asignación de distritos federales.
- Construcción de variables por candidatura.
- Muestreo aleatorio simple sin reemplazo.
- Estimación de totales y razones.
- Estimación de varianzas y errores estándar.
- Intervalos de confianza aproximados.
- Simulaciones Monte Carlo.
- Pruebas unitarias iniciales.

### Próximas implementaciones

- Validación adicional de los estimadores.
- Determinación de tamaños de muestra según precisión objetivo.
- Muestreo aleatorio estratificado.
- Asignación igualitaria, proporcional y de Neyman.
- Comparación de precisión entre diseños muestrales.
- Ampliación de pruebas automatizadas y documentación.

## Consideraciones metodológicas

Este proyecto analiza retrospectivamente una elección ya realizada. No tiene como objetivo pronosticar resultados electorales futuros.

La disponibilidad de la población completa permite conocer los parámetros de referencia y evaluar el desempeño de los estimadores mediante simulación.

Los resultados dependen del marco muestral, las variables utilizadas, el diseño probabilístico y las aproximaciones empleadas para estimar la incertidumbre.

## Autor

Cristian Eduardo Huerta Estrada, estudiante de la Licenciatura en Matemáticas de la Facultad de Ciencias, Universidad Nacional Autónoma de México (UNAM).

Áreas de interés: probabilidad, estadística, inferencia estadística, aprendizaje automático y ciencia de datos.
