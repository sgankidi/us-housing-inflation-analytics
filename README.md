# US Housing Prices vs Inflation (Power BI)

This project analyzes **US housing price trends** and **inflation** over time using real public data:
- **Zillow ZHVI** (state-level home value index)
- **BLS CPI-U** (Consumer Price Index)

## Goals
- Compare housing price growth vs inflation (YoY, long-term trend)
- Highlight which states saw the strongest housing appreciation
- Provide an “inflation-adjusted” view of housing growth

## Tools
- Power BI (data modeling, visuals)
- Power Query (data cleaning and reshaping)
- DAX (time intelligence: YoY, YTD where applicable)

## Repository Structure
- `data/` – source datasets (Zillow + CPI)
- `powerbi/` – Power BI dashboard (.pbix)
- `dax/` – documented measures
- `docs/` – data model and notes
- `screenshots/` – exported dashboard visuals

## Status
Repo scaffolding complete. Data ingestion and dashboard build in progress.
