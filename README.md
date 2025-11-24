# Interactive Automated Data Cleaner

This project is an enhanced **interactive data cleaning application** built using **Streamlit**, designed to make data preprocessing simpler, more visual, and user‑friendly for analysts, students, and data scientists.

The app supports:

* Configurable cleaning operations
* Visual previews (before/after)
* Interactive charts using Plotly
* Real‑time user controls
* Downloadable cleaned dataset output

---

## 📌 Features / About the Project

### 🔹 **1. Interactive Sidebar Controls**

Users can select which cleaning operations to apply:

* Handle missing values (with methods: mean, median, mode, constant)
* Detect/remove outliers (adjustable thresholds)
* Remove duplicates
* Standardize column names
* Convert date columns
* Encoding categorical variables
* Normalization/standardization

Each step is user‑configurable.

### 🔹 **2. Automated Data Quality Assessment**

The app evaluates dataset quality and shows:

* Missing value statistics
* Duplicate counts
* Data type distribution
* Column‑wise summary

### 🔹 **3. Dynamic Visualizations (Plotly)**

Interactive charts include:

* Missing value bar chart
* Numeric column distributions
* Before/after comparison charts

Charts allow zoom, hover, drag, and more.

### 🔹 **4. Data Preview (Before/After)**

* Displays top 10 rows before cleaning
* Displays top 10 rows after cleaning
* Highlighted differences

### 🔹 **5. Download Cleaned Data**

Download final output as **CSV**.

---

## 🚀 How to Use the App

### **Step 1: Run the application**

```bash
streamlit run data_cleaner.py
```

### **Step 2: Upload a dataset**

Supported formats:

* CSV
* XLSX
* TXT

### **Step 3: Configure cleaning operations**

Available in the sidebar:

* Select missing value handling method
* Enable/disable outlier removal
* Choose encoding technique
* Toggle visualizations

### **Step 4: Assess Quality**

The app automatically displays:

* Missing values
* Data types
* Duplicates
* Summary statistics

### **Step 5: Apply Cleaning**

Click the **“Clean Data”** button.
The cleaned dataset appears with visual comparisons.

### **Step 6: Download the cleaned file**

A download button lets you export your final dataset.

---

## ✅ Advantages

### 1. **Highly Interactive**

Users choose what operations to apply instead of everything running automatically.

### 2. **Clear Visual Feedback**

Charts help users understand distributions, missing values, and improvements.

### 3. **Beginner Friendly**

No coding knowledge required—ideal for students and analysts.

### 4. **Customizable Workflow**

The user controls every step and can disable operations they don’t want.

### 5. **Fast and Lightweight**

Streamlit makes the UI responsive and easy to run even on low‑end machines.

### 6. **Real‑time Preview**

Instant before/after comparison increases clarity.

---

## ⚠️ Limitations

### 1. **Not suitable for large datasets (1M+ rows)**

Streamlit and pandas can get slow with very large files.

### 2. **Basic Outlier Detection**

Uses IQR/Z‑Score; advanced ML‑based detection not included (though can be added).

### 3. **Limited Data Types**

Special formats (JSON, SQL tables) are not supported directly.

### 4. **Memory‑Dependent**

Entire dataset loads into RAM, which can be limiting.

### 5. **No Auto‑Save**

Users must manually download cleaned results.

---

## 📁 File Structure (Recommended)

```
project/
│── data_cleaner.py     # Main Streamlit application
│── requirements.txt    # Dependencies
│── README.md           # Documentation
│── assets/             # Images (optional)
```

---

## 📦 Requirements

Install dependencies:

```bash
pip install streamlit openpyxl pandas plotly numpy
```

---

## ✨ Future Enhancements (Optional)

* Add ML‑based anomaly detection
* Add correlation heatmaps
* Add feature engineering options
* Add auto‑EDA report generation (like Pandas Profiling)
* Support exporting to Excel with style formatting.

If you want, I can also **add screenshots**, **project logo**, **GitHub‑ready formatting**, or **expand documentation**!
