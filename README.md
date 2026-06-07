# Data Cleaning & Visualization Project

> A complete Python data pipeline that cleans raw retail sales data and generates an interactive visual dashboard with key business insights.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-11557c)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13-4c72b0)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Project Overview

This project demonstrates a full **data science workflow** — from raw, messy data to clean, analyzed, and beautifully visualized insights. Using a simulated retail sales dataset (2024), it covers every stage of data preprocessing and storytelling with data.

---

## Features

| Feature | Description |
|---|---|
|  **Missing Values** | Fills gaps using median imputation for ratings, zero-fill for discounts |
|  **Duplicate Removal** | Detects and drops duplicate order records |
|  **Outlier Detection** | Removes extreme sales values using the 97th percentile method |
|  **Feature Engineering** | Derives `month`, `profit`, and other columns from raw data |
|  **Dashboard** | 5-panel visual report saved as a high-resolution PNG |

---

##  Project Structure

```
data-cleaning-visualization/
│
├── data_cleaning_visualization.py   # Main script: cleaning + visualization
├── retail_sales_raw.csv             # Raw dataset (520 rows, with issues)
├── retail_sales_clean.csv           # Cleaned dataset (485 rows, with derived columns)
├── retail_sales_dashboard.png       # Output dashboard (auto-generated)
└── README.md                        # Project documentation
```

---

##  Getting Started

### Prerequisites

Make sure you have Python 3.8+ installed.

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/data-cleaning-visualization.git
cd data-cleaning-visualization

# Install dependencies
pip install pandas numpy matplotlib seaborn
```

### Run the Project

```bash
python data_cleaning_visualization.py
```

The script will:
1. Generate a sample retail sales dataset (500 rows with injected issues)
2. Print a cleaning report to the console
3. Save `retail_sales_dashboard.png` to the current directory

>  The raw and cleaned datasets are also available directly as CSV files — no need to run the script to access the data.

---

##  Dashboard Preview

The output dashboard includes:

- **Cleaning Summary Panel** — metrics before and after cleaning
- **Monthly Sales vs Profit** — grouped bar chart across 12 months
- **Sales by Category** — donut chart (Electronics, Clothing, Food & Beverage, etc.)
- **Sales by Region** — horizontal bar chart (North, South, East, West, Central)
- **Customer Rating Distribution** — bar chart for ratings 1–5

---

## Dataset

Two CSV files are included for direct use or further exploration:

### `retail_sales_raw.csv` — 520 rows
The original unprocessed dataset with intentionally injected data quality issues:

| Column | Type | Description |
|---|---|---|
| `order_id` | int | Unique order identifier |
| `date` | date | Order date (2024) |
| `category` | str | Product category |
| `region` | str | Sales region |
| `sales` | float | Revenue amount |
| `quantity` | int | Units ordered |
| `discount` | float | Discount rate (0–0.2), **has missing values** |
| `customer_rating` | float | Rating 1–5, **has missing values** |

>  Contains 20 duplicate rows, 45 missing values, and 5 outliers in `sales`.

---

### `retail_sales_clean.csv` — 485 rows
The fully cleaned and enriched dataset, ready for analysis:

| Column | Type | Description |
|---|---|---|
| `order_id` | int | Unique order identifier |
| `date` | date | Order date (2024) |
| `category` | str | Product category |
| `region` | str | Sales region |
| `sales` | float | Revenue amount (outliers removed) |
| `quantity` | int | Units ordered |
| `discount` | float | Discount rate (no missing values) |
| `customer_rating` | float | Rating 1–5 (no missing values) |
| `month` | str | Derived month label (e.g. Jan, Feb) |
| `profit` | float | Derived: `sales × (1 - discount)` |

---

## 🔬 Data Cleaning Pipeline

```
Raw Dataset (520 rows)
        │
        ▼
Remove Duplicates (–20 rows)
        │
        ▼
Fill Missing Values (45 cells fixed)
        │
        ▼
Remove Outliers (–5 rows, 97th percentile)
        │
        ▼
Feature Engineering (month, profit columns)
        │
        ▼
Clean Dataset (485 rows) 
```

---

## 🛠️ Technologies Used

- **Python 3.8+** — Core language
- **Pandas** — Data manipulation and cleaning
- **NumPy** — Numerical operations and random data generation
- **Matplotlib** — Custom dashboard layout (GridSpec)
- **Seaborn** — Theming and styling

---

## 📈 Key Insights (Sample Data)

-  **Total Sales**: ~$88,600 across 485 clean orders
-  **Top Category**: Electronics (~26% of sales)
-  **Top Region**: South
-  **Average Rating**: 3.82 / 5.00
-  **Peak Month**: May

---

##  Concepts Demonstrated

- Data preprocessing with Pandas
- Handling real-world data quality issues
- IQR / quantile-based outlier detection
- Median imputation for missing values
- Multi-panel dashboard design with Matplotlib GridSpec
- Data storytelling and visual communication

---

##  License

This project is licensed under the [MIT License](LICENSE).

---

##  Acknowledgements

Built as part of a Data Science project focusing on data preprocessing, visualization, and storytelling with Python.
