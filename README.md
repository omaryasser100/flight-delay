# Flight Delay Analysis & Prediction

This repository presents a complete data analysis, machine learning modeling, and business insights pipeline on the flight delay dataset.  
It includes exploratory data analysis (EDA), model building, evaluation, and visualization through an interactive Streamlit web application.  
The deployed app is available here: **[Flight Delay App](https://flight-delay-omar.streamlit.app/)**

---

## Project Overview

Flight delays represent a major operational and financial challenge for airlines and passengers alike.  
This project explores how machine learning can be used to predict flight delays, identify key contributing factors, and derive actionable business insights.  

The work includes:
1. Data collection and preprocessing  
2. Exploratory data analysis and visualization  
3. Feature engineering and selection  
4. Training and evaluating multiple machine learning models  
5. Extracting business insights from model outputs  
6. Deploying an interactive prediction dashboard using Streamlit  

---

## Objectives

- Understand the major causes and patterns of flight delays  
- Build predictive models to estimate delay duration or probability  
- Visualize flight trends, airport performance, and delay statistics  
- Provide an interactive web application for users to explore and test predictions  

---

## Key Features

- **Comprehensive EDA:** Analysis of delay frequency, distribution, and correlations  
- **Feature Engineering:** Creation of time-based, route-based, and weather-related features  
- **Modeling Techniques:** Comparison across multiple ML algorithms (Random Forest, XGBoost, LightGBM, CatBoost, etc.)  
- **Evaluation Metrics:** MAE, RMSE, R² for regression models  
- **Business Insights:** Data-driven recommendations to mitigate delays  
- **Deployment:** Streamlit app hosted at [https://flight-delay-omar.streamlit.app/](https://flight-delay-omar.streamlit.app/)  

---

## Data Summary

The dataset includes detailed flight information such as:
- Flight date, carrier, and route  
- Scheduled and actual departure/arrival times  
- Weather and airport conditions  
- Delay duration and reason codes  

After preprocessing, the dataset contained:
- Over **500,000 records**  
- **10+ engineered features** representing time, location, and traffic context  

---

## Methodology

1. **Data Cleaning:** Removal of duplicates, missing values, and inconsistencies  
2. **Exploratory Data Analysis:**  
   - Delay distribution visualization  
   - Route, carrier, and time-of-day analysis  
   - Correlation and feature relationships  
3. **Feature Engineering:**  
   - Encoding categorical variables  
   - Generating new time and route features  
4. **Modeling:**  
   - Tested multiple ML algorithms (Linear Regression, Decision Tree, Random Forest, XGBoost, LightGBM, CatBoost)  
   - Hyperparameter tuning with GridSearchCV  
5. **Evaluation:**  
   - Compared models using R², MAE, and RMSE  
   - Chose the top-performing model for deployment  

---

## Business Insights
 
- **Airport Bottlenecks:** Certain hubs were responsible for over 60% of total delay minutes  
- **Airline Performance:** Carriers varied in reliability due to scheduling and congestion patterns  
- **Seasonal Trends:** Delays spiked during winter months and holiday periods  

These findings can help optimize scheduling, route planning, and staffing decisions for airline operations.

---

## The Deployed Application

**Live App:** [https://flight-delay-omar.streamlit.app/](https://flight-delay-omar.streamlit.app/)

The Streamlit dashboard provides:
- **Interactive data visualization:** Explore flight and delay trends dynamically  
- **User input interface:** Enter flight details to get predicted delay outcomes  
- **Prediction output:** Displays expected delay time or delay probability  
- **Insights tab:** Shows feature importance and performance metrics  

The app integrates a trained machine learning model, real-time user input handling, and precomputed summary analytics.

---

## Technologies Used

- **Python 3.x**
- **Pandas**, **NumPy** — Data manipulation  
- **Matplotlib**, **Seaborn**, **Plotly** — Visualization  
- **Scikit-learn**, **XGBoost**,  — Machine learning  
- **Streamlit** — Web app deployment  
- **Joblib / Pickle** — Model persistence  




## Author

**Omar Yasser**  
[GitHub Profile](https://github.com/omaryasser100)  
[Live App](https://flight-delay-omar.streamlit.app/)
