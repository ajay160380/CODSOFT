<div align="center">
  <h1>🚀 CodSoft Data Analytics Internship</h1>
  <p><i>A complete Data Engineering and Visualization Portfolio</i></p>

  ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
  ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
  ![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
</div>

<br>

Welcome to my Data Analytics internship repository! This repository showcases my ability to build end-to-end data pipelines, from raw messy data to highly interactive, production-ready web dashboards.

---

## 🧹 Task 1: Universal Data Cleaning Pipeline

The first task focuses on ingesting messy datasets, automatically identifying anomalies, and cleaning them using a dynamic Streamlit engine. 

### ⚙️ Pipeline Architecture

```mermaid
graph TD
    A[(Raw Data<br>CSV Upload)] -->|Streamlit Engine| B{Anomaly Detection}
    B -->|Finds Nulls| C[Missing Value Imputation]
    B -->|Finds Duplicates| D[Duplicate Removal]
    B -->|Schema Check| E[Standardize Columns]
    C & D & E --> F[(Cleaned Dataset)]
    F --> G[Interactive Data Profiling UI]
```

### ✨ Key Features
* **Universal Upload:** Users can upload any CSV, and the engine automatically adapts to clean generic missing values and duplicates.
* **Superstore Specifics:** If no file is uploaded, it defaults to the Superstore dataset, performing advanced feature engineering (e.g., calculating `shipping_days` from Dates).
* **Interactive UI:** Built with premium glassmorphism CSS, offering a 4-tab workflow: Raw Inspection ➡️ Issues Found ➡️ Transformations ➡️ Final Output.


---
<div align="center">
  <b>Developed by Ajay Vishwakarma</b>
</div>
