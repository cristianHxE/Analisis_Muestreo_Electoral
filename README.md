# Electoral Sampling Analysis — Mexico City 2024

**Statistical inference, probability sampling, and Monte Carlo simulations with Python**

**English** | [Español](README.es.md)

## Project Description

This project develops and implements statistical sampling methods using data from the 2024 election for Head of Government of Mexico City.

The main objective is to estimate vote totals and vote shares using probability samples of polling stations, and to evaluate estimator behavior through Monte Carlo simulations.

The project originated as an academic assignment initially developed in R and is being progressively migrated to Python, with particular emphasis on:

- Mathematical foundations of the estimators.
- Modular code organization.
- Data validation and integrity.
- Reproducibility of experiments.
- Statistical evaluation of results.
- Implementation of automated tests.

## Statistical Methodology

### 1. Data Preparation and Integration

Two sources of information are integrated:

- Mexico City electoral results by polling station.
- Identification of the federal electoral district corresponding to each polling station.

The electoral dataset contains **13,503 records**. The district identification file provides information for 13,431 polling stations.

The remaining 72 polling stations are classified according to the following rules:

| Polling station type | Count | Assignment criterion |
|---|---:|---|
| Overseas voting | 12 | Federal district 0 |
| Early voting | 54 | Federal district corresponding to its electoral section |
| People in pretrial detention | 6 | Federal district corresponding to its electoral section |

During integration, checks are performed to detect duplicate keys, ambiguous mappings between sections and districts, and records without an identification.

Variables representing the votes obtained by each candidate are then constructed, taking into account the relevant party and coalition combinations.

### 2. Simple Random Sampling Without Replacement (SRSWOR)

A simple random sampling without replacement design is implemented, with the polling station as the sampling unit.

For the current analysis, the 12 overseas voting polling stations are excluded, yielding a study population of:

$$
N=13\,491.
$$

Each sample of size $n$ is selected with equal probability among all possible subsets of that size from the population.

The inclusion probability of a polling station is:

$$
\pi_i=\frac{n}{N}.
$$

### 3. Estimation of Totals

To estimate the population total of votes for a candidate, the following estimator is used:

$$
\widehat T_y=N\overline y_s,
$$

where $\overline y_s$ is the sample mean of votes per polling station.

The variance is estimated by:

$$
\widehat{\operatorname{Var}}(\widehat T_y)
=N^2\left(1-\frac{n}{N}\right)\frac{s_y^2}{n}.
$$

This expression incorporates the finite population correction.

### 4. Estimation of Vote Shares Using Ratios

To estimate the proportion of votes obtained by a candidate, the ratio estimator is used:

$$
\widehat R=\frac{\sum_{i\in s}y_i}{\sum_{i\in s}x_i},
$$

where:

- $y_i$: votes obtained by the candidate at polling station $i$.
- $x_i$: total votes recorded at polling station $i$.

The approximate variance is calculated using Taylor linearization, with residuals:

$$
e_i=y_i-\widehat R x_i.
$$

Thus:

$$
\widehat{\operatorname{Var}}(\widehat R)
=\left(1-\frac{n}{N}\right)\frac{s_e^2}{n\overline x_s^2}.
$$

Approximate confidence intervals are constructed using quantiles of the normal distribution.

### 5. Monte Carlo Simulations

Repeated simple random sampling simulations are performed to study the behavior of the estimators.

The experiments include:

- Empirical bias.
- Empirical variance.
- Mean squared error (MSE).
- Root mean squared error (RMSE).
- Comparison between empirical variance and mean estimated linearized variance.
- Empirical coverage of confidence intervals.

The sample sizes considered are:

$$
n\in\{50,100,200,500,1000\},
$$

with 500 replications for each size.

The goal is to study the relationship between sample size, estimator precision, and confidence interval behavior.

## Technologies Used

- **Python:** implementation of statistical procedures.
- **Pandas:** data manipulation, integration, and validation.
- **NumPy:** numerical operations and statistical calculations.
- **Matplotlib:** visualization of results.
- **Pytest:** automated testing of estimators.
- **Git and GitHub:** version control and project documentation.

## Repository Structure

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

## Installation

Clone the repository:

```bash
git clone https://github.com/cristianHxE/Analisis_Muestreo_Electoral.git
cd Analisis_Muestreo_Electoral
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Data

The original files are not included in this initial version of the repository.

To reproduce the analysis, the following files are required:

- `2024_SEE_GOB_CDMX_CAS.csv`
- `DIS_FED_09.csv`

The files must be placed in the `data/raw/` directory.

The first source contains electoral results by polling station. The second contains the federal district identification used in the academic project.

The provenance and redistribution conditions of these files must be documented before adding them to the repository.

## Execution

### Data Preparation

From the project root:

```bash
python run_preparation.py
```

The program integrates the original files, identifies the federal districts, and constructs the electoral variables.

The resulting dataset is saved to:

`data/processed/votos_cdmx_limpio.csv`

### Estimation Using SRSWOR

```bash
python run_sampling.py
```

This script selects a sample of polling stations, calculates estimates of totals and vote shares, and compares the results with known population parameters.

### Simulation Experiments

To run the basic ratio estimator simulation:

```bash
python -m experiments.ratio_simulation
```

To compare different sample sizes:

```bash
python -m experiments.mas_precision
```

The second experiment generates variance and coverage plots in `reports/figures/`.

### Automated Tests

```bash
python -m pytest -v
```

The tests check known numerical results and verify the behavior of functions for certain invalid inputs.

## Project Status

**Under development — initial portfolio version.**

### Implemented

- Electoral data integration and validation.
- Federal district assignment.
- Construction of candidate-level variables.
- Simple random sampling without replacement.
- Estimation of totals and ratios.
- Estimation of variances and standard errors.
- Approximate confidence intervals.
- Monte Carlo simulations.
- Initial unit tests.

### Planned Implementations

- Additional validation of the estimators.
- Sample size determination based on target precision.
- Stratified random sampling.
- Equal, proportional, and Neyman allocation.
- Comparison of precision across sampling designs.
- Expansion of automated tests and documentation.

## Methodological Considerations

This project retrospectively analyzes an election that has already taken place. It is not intended to forecast future election results.

The availability of the complete population makes it possible to know reference parameters and evaluate estimator performance through simulation.

Results depend on the sampling frame, variables used, probability sampling design, and approximations employed to estimate uncertainty.

## Author

Cristian Eduardo Huerta Estrada, undergraduate Mathematics student at the Faculty of Sciences, National Autonomous University of Mexico (UNAM).

Areas of interest: probability, statistics, statistical inference, machine learning, and data science.
