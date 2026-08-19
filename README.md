# CODSOFT Data Analytics Internship

This repository contains the tasks completed during the CodSoft Data Analytics Internship. 
All project phases and tasks are organized within this single repository for easy access and review.

## Project Overviews

### Task 1: Data Cleaning & Preprocessing (Completed)
- **Objective:** Import, inspect, clean, and validate the "Sample Superstore" retail sales dataset.
- **Summary of actions:** 
  - Imported the raw dataset using Pandas with `cp1252` encoding.
  - Standardized column names to `snake_case` for easier querying.
  - Imputed missing values (e.g., postal code) and removed duplicate rows.
  - Standardized categorical text (casing, whitespaces) and converted date strings into actual `datetime64` objects.
  - Created a derived `shipping_days` column.
  - Saved the cleaned dataset to `data/processed/superstore_cleaned.csv`.
- **Location:** `task1_data_cleaning/data_cleaning.ipynb`

### Task 3: Visualization (In Progress)
- *(Folder structure initialized, pending completion)*

### Task 4: Customer Analysis (In Progress)
- *(Folder structure initialized, pending completion)*

---
**Note:** The original raw dataset is `data/raw/superstore_raw.csv`, and the cleaned dataset used for subsequent tasks is `data/processed/superstore_cleaned.csv`.
