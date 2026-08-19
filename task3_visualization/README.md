<div align="center">
  <h1>⚡ Task 3: Executive Visualization Dashboard</h1>
  <p><i>Real-time interactive business intelligence and analytics.</i></p>

  ![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
  ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
  ![Data Analytics](https://img.shields.io/badge/Data_Analytics-0052CC?style=for-the-badge&logo=data&logoColor=white)
</div>

<br>

## 📈 System Architecture

This interactive dashboard pulls from the central Cleaned Dataset to render live metrics and visualizations.

```mermaid
graph LR
    A[(Cleaned Data<br>superstore_cleaned.csv)] -->|Data Binding| B{Streamlit Engine}
    
    subgraph Nexus Analytics Dashboard
    B -->|Sidebar Filters| C[Region / Category Selection]
    C -->|Dynamic Updates| D((KPI Cards))
    C -->|Dynamic Updates| E((Interactive Plotly Charts))
    end
    
    E -.-> F[Bar Chart: Top Categories]
    E -.-> G[Line Chart: Profit vs Sales]
    E -.-> H[Scatter: Profitability Matrix]
```

## 💎 Premium Features

- **Interactive Sidebar Filtering:** Filter the entire application state globally using Region and Category drop-downs.
- **Masterclass Plotly Charts:** Highly customized Plotly Express charts featuring:
  - Transparent backgrounds aligning seamlessly with the app theme.
  - Custom *Outfit* fonts and disabled gridlines for a clean UI.
  - Break-Even indicator lines (profit=0) dynamically plotted on scatter matrices.
- **Next-Gen CSS Glassmorphism:** Features a premium dark mode layout with floating, animated gradient KPI cards.

## 🚀 How to Launch the Dashboard

Launch the interactive dashboard to interact with the visual analytics:

```bash
# 1. Navigate to the Task 3 directory
cd task3_visualization

# 2. Run the Streamlit Dashboard (on port 8502 to avoid conflicts)
streamlit run app.py --server.port 8502
```

*The dashboard will automatically open in your default web browser at `http://localhost:8502/`.*

---
<div align="center">
  <b>Built for CodSoft Data Analytics Internship</b>
</div>
