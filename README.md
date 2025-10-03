# South African Unemployment Analysis (2008–2024)

## Overview
This project analyzes the **unemployment trends in South Africa** from 2008 to Q1 2024 using official unemployment data by province and metropolitan areas. It focuses on understanding how unemployment evolved over time, highlighting **provincial differences** and the impact of major events like **COVID-19**.

The analysis includes:
- Data cleaning and reshaping from Excel files
- Handling missing values and separating provinces from metro areas
- Visualizations comparing provinces with the national average
- Yearly and quarterly trends for better insights

---

## Key Questions Answered
1. **How does Gauteng’s unemployment compare to the national average?**
2. **Which provinces have consistently high or low unemployment rates?**
3. **How did unemployment trends change during COVID-19?**
4. **Quarterly vs yearly trends across all provinces**

---

## Dataset
- Source: Excel file [`Unemployment_rate_by_province_and_metro_2008_-_2024Q1.xlsx`](https://wcg-opendataportal-westerncapegov.hub.arcgis.com/documents/12cb36b98c3a458f89e343585676cd49/about)
- Columns include:
  - `Province` – The South African province
  - `Metro` – Metropolitan area (if applicable)
  - `Quarter` – Quarterly period (e.g., Jan-Mar 2008)
  - `Unemployment_Rate` – Percentage unemployment
  - `Level` – Province or Metro level

---

## Analysis & Visualizations
### Gauteng vs South Africa
![Gauteng vs National](https://github.com/DenzilKachidza/SA-Unemployment-Analysis/blob/b5090fadfa58db5e8ea816d979c6e14f59fb90bc/Gauteng%20vs%20National.png)
- The chart shows **Gauteng’s unemployment** compared to the **national average** from 2008–2024.
- Key spikes during **COVID-19 (2020–2021)** are highlighted.

---

### Provincial Averages
![Provincial Unemployment](https://github.com/DenzilKachidza/SA-Unemployment-Analysis/blob/b5090fadfa58db5e8ea816d979c6e14f59fb90bc/Provincial%20Averages.png)
- Highlights **which provinces have higher or lower unemployment** on average.
- Useful for comparing regional disparities.
---
### Yearly Trends
![Yearly Trends](https://github.com/DenzilKachidza/SA-Unemployment-Analysis/blob/f2e12f917e71032cfc284e5c9bc5c6f80d6d9cec/Yearly%20Trends.png)
- Aggregated by year to smooth quarterly fluctuations and identify long-term trends.
- Provides context for policy evaluation and economic planning.
---
### Metro vs Province Differences
![Metro vs Province Differences](https://github.com/DenzilKachidza/SA-Unemployment-Analysis/blob/0f7f4c0a0e5b06b481a466ec3a594c684cf0f0bd/metro%20vs%20provincial.png)
- Highlights how metro areas perform relative to their province. Positive values indicate higher unemployment in the metro than the provincial average.
---

## Insights
- **Gauteng** generally follows national trends but shows sharper fluctuations during economic shocks.
- Provinces like **KwaZulu-Natal** and **Eastern Cape** often have higher unemployment compared to others.
- COVID-19 caused **significant temporary spikes**, visible across all provinces.
- Metropolitan areas often have lower unemployment than their surrounding non-metro regions.
---
### Tools 
- *Python*

