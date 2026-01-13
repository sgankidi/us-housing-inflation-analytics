# 🚀 Step-by-Step Implementation Guide: US Housing vs. Inflation

This document provides the exact technical steps to build the Power BI dashboard from the processed datasets in this repository.

---

## 🏗️ Phase 1: Data Ingestion
1.  **Open Power BI Desktop**.
2.  Click **Get Data** > **Text/CSV**.
3.  Select `processed_data/housing_processed.csv` and click **Load**.
4.  Repeat for `processed_data/inflation_processed.csv`.
5.  (Optional) Click **Transform Data** to ensure the `Date` columns are detected as Date types.

---

## 📅 Phase 2: Create a Calendar Table (Best Practice)
To sync the Housing data with the Inflation data, you MUST have a shared Calendar table.
1.  Go to the **Table View** (left sidebar).
2.  Click **New Table** and paste this DAX:
    ```dax
    Calendar = 
    CALENDARAUTO()
    ```
3.  Add a **Year** column to this table:
    ```dax
    Year = YEAR('Calendar'[Date])
    ```
4.  Add a **Month** column:
    ```dax
    Month = FORMAT('Calendar'[Date], "MMM")
    ```

---

## 🔗 Phase 3: Data Modeling (Star Schema)
1.  Go to the **Model View** (left sidebar).
2.  Create the following relationships (Drag and Drop):
    *   `Calendar[Date]`  ➡️  `housing_processed[Date]` (One-to-Many)
    *   `Calendar[Date]`  ➡️  `inflation_processed[Date]` (One-to-Many)
3.  Ensure the cross-filter direction is **Single** (Calendar filters the fact tables).

---

## 🧪 Phase 4: Implementing DAX Measures
Go to the **Report View**, click **New Measure**, and add the formulas from `dax/key_measures.dax`. 

### Key Measures to Create:
*   **Housing Growth % (YoY)**: Compares current state home values to the same month last year.
*   **Inflation Rate % (YoY)**: Compares current CPI to the same month last year.
*   **Divergence Index**: Subtracts Inflation from Housing Growth to see the "Real" appreciation.

---

## 🎨 Phase 5: Building the Dashboard (The "Wow" Factor)

### 1. Global Theme
*   **Canvas Background**: Set to Dark Navy (`#111827`) with 0% transparency.
*   **Visual Border/Cards**: Use a slightly lighter grey (`#1F2937`) with **Rounded Corners (10px)**.

### 2. The Main Chart (The Divergence)
*   **Visual type**: Line and Stacked Column Chart.
*   **Shared Axis**: `Calendar[Date]` (Year/Month).
*   **Column Values**: `[Divergence Index]`.
*   **Line Values**: `[Housing Growth %]` and `[Inflation Rate %]`.
*   **Colors**: Housing = Electric Blue (`#3B82F6`), Inflation = Amber (`#F59E0B`).

### 3. The State Heatmap
*   **Visual type**: Filled Map (US).
*   **Location**: `housing_processed[State]`.
*   **Tooltip**: `[Housing Growth %]`.
*   **Conditional Formatting**: Set Gradient from Light Blue (low growth) to Dark Blue (high growth).

### 4. Executive KPIs (Cards)
*   Use the **New Card Visual** to show:
    *   Average Home Value (Currency).
    *   Average Inflation Rate (Percentage).
    *   State with Highest Growth (Top N filter).

---

## 🚀 Phase 6: Polishing for the Portfolio
1.  **Slicers**: Add a Slicer for `State` and a Slicer for `Date` (Range).
2.  **Tooltips**: Create a custom Tooltip page that shows a breakdown of CPI categories (Energy vs Food) when hovering over the line chart.
3.  **Final Polish**: Ensure all fonts are **Inter** or **Segoe UI**. Remove unnecessary gridlines for a "Premium" look.

---
**Done!** Save your file as `powerbi/us_housing_inflation.pbix` and take high-res screenshots for the `screenshots/` folder.
