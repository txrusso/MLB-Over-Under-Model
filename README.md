# 📊 MLB Over/Under Prediction Using Machine Learning

## Overview

This project explores whether machine learning models can predict total runs in Major League Baseball (MLB) games and generate a profitable betting strategy against sportsbook over/under lines.

Using publicly available MLB data and historical betting lines, multiple models are developed and evaluated. The project focuses not only on predictive accuracy but also on **real-world profitability**, measured through simulated betting returns.

---

## Objectives

- Predict the Vegas over/under line (`total_line`) for MLB games  
- Compare model predictions to sportsbook lines  
- Evaluate whether predictions can produce a **positive return on investment (ROI)**  
- Analyze the relationship between prediction accuracy and betting profitability  

---

## Project Structure

```
├── data_creation.ipynb      # Data collection, cleaning, and feature engineering
├── models.ipynb             # Modeling, evaluation, and betting strategy
├── ROI.py                   # Functions for bet simulation and ROI calculation
├── model_data.csv                # Final dataset used for modeling
└── README.md                # Project documentation
```

---

## Methodology

### Data Collection

Data is constructed by combining:
- MLB game, team, and player data (via MLB Stats API)
- Historical sportsbook over/under lines

The dataset spans:
- **2021–2024** → training data  
- **2025** → test data  

Each observation represents a single game.

---

### Feature Engineering

Features include:
- Team hitting metrics (AVG, SLG, OPS, HR rates)
- Pitching metrics (ERA, WHIP, strikeout rates)
- Rolling statistics (last 5 and 10 games)
- Ballpark effects (`park_factor`)

Care is taken to avoid data leakage by only using **past information**.

---

### Models Implemented

1. **Linear Regression**  
   - Baseline model for comparison  

2. **Random Forest**  
   - Captures nonlinear relationships  
   - Tuned using `RandomizedSearchCV`  

3. **XGBoost (No Feature Selection)**  
   - Primary model  
   - Tuned using time-series cross-validation  

4. **XGBoost (With Feature Selection)**  
   - Includes `SelectFromModel`  
   - Tests whether reducing feature space improves performance  

---

### Evaluation Metrics

Models are evaluated using:

**Prediction Metrics**
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)

**Betting Metrics**
- Return on Investment (ROI)
- Win rate
- Total profit/loss (units)

---

## Betting Strategy

A simple betting strategy is used:

- Bet **Over** if predicted total > Vegas line + threshold  
- Bet **Under** if predicted total < Vegas line − threshold  

---

### Threshold Optimization

To simulate a realistic betting approach, the threshold is optimized:

- Tested across a range of values (0.1 → 2.0)
- Best threshold ≈ **1.71**
- Result:
  - ROI: **-0.51%**
  - Win Rate: **53.97%**
  - Number of Bets: **63**

---

## Key Results

| Model | MAE | ROI | Win Rate |
|------|-----|-----|----------|
| Linear Regression | 0.6570 | -9.46% | 48.41% |
| Random Forest | 0.6329 | -7.84% | 49.22% |
| XGBoost | 0.6162 | -7.35% | 49.45% |
| XGBoost + FS | 0.6152 | -7.39% | 49.45% |
| XGBoost (Optimized Threshold) | — | **-0.51%** | **53.97%** |

---

## Key Insights

- More complex models improve prediction accuracy, but **do not produce profitable betting strategies**
- Even with a **53.97% win rate**, ROI remains negative due to sportsbook margins
- Threshold optimization reduces losses significantly, but **does not create a positive edge**
- Feature selection provides **minimal benefit** for XGBoost
- Sportsbook lines are highly efficient and difficult to outperform

---

## Important Takeaway

> Improving prediction accuracy does **not** guarantee betting profitability.

Even advanced models with careful tuning and feature engineering were unable to consistently beat the market.


PLEASE DO NOT USE THIS MODEL TO BET. IF YOU HAVE A GAMBLING PROBLEM, PLEASE SEEK HELP.

---

## Technologies Used

- Python  
- pandas, numpy  
- scikit-learn  
- XGBoost  
- matplotlib  

---

## Future Improvements

- Incorporate additional data (weather, line movement, injuries)
- Explore probabilistic models instead of point predictions
- Test alternative betting strategies (e.g., Kelly Criterion with calibrated probabilities)
- Use closing line value (CLV) as an additional evaluation metric  

---

## 📬 Author

Tyler Russo  
M.S. Data Science, Loyola University Maryland  
