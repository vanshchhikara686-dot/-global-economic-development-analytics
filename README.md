# Global Economic & Development Analytics

**End-to-end real-world data analytics project using World Bank indicators | 2000–2024**

An integrated analysis of economic performance, population change, agriculture, healthcare expenditure and life expectancy across economies worldwide. The project turns World Bank data into analytical outputs and a four-page Power BI report using Python, SQL Server, Excel and Power BI.

> **Project type:** Real-world public-data analytics  
> **Coverage:** 217 economies · 10 indicators · 2000–2024  
> **Analytical dataset:** 54,250 country-indicator-year records

---

## 1. Business Problem

Economic and development indicators are published across different measures and country-year observations. Looking at GDP, population, agriculture and healthcare separately makes it difficult to understand long-term development patterns or compare economies consistently.

This project brings these indicators into one analytical workflow to answer questions such as:

- How did nominal GDP and economic growth change between 2000 and 2024?
- Which economies had the largest nominal GDP and GDP per capita in 2024?
- How did population change over the 25-year period, and which economies had the largest populations?
- Did agriculture's share of GDP and employment change over time?
- How do agricultural GDP contribution and agricultural employment vary across countries?
- How do healthcare expenditure and life expectancy vary across reporting economies?
- What data-coverage limitations should analysts consider before interpreting country comparisons?

### Business objective

Create a reproducible, evidence-based view of global development indicators that can support exploratory economic research, country comparisons and data-informed discussion. This is descriptive analytics; it does not claim to establish causation or make policy recommendations.

---

## 2. Project Scope & Dataset

| Attribute | Details |
|---|---|
| Primary source | World Bank indicators |
| Period | 2000–2024 |
| Economies represented | 217 |
| Indicators | 10 |
| Records in cleaned analytical dataset | 54,250 |
| Grain | Economy × indicator × year |
| Format | CSV |
| Data type | Real-world public data |

### Indicator themes

- **Economy:** GDP (current US$), GDP growth, GDP per capita.
- **Population:** Total population.
- **Agriculture:** Agriculture value added, employment in agriculture, cereal yield.
- **Healthcare and development:** Health expenditure, life expectancy and poverty-related indicator(s).

The exact indicator names and codes are documented in the data dictionary and source files.

---

## 3. Tools, Skills & Competencies

| Technology | Skills demonstrated |
|---|---|
| **Python** | World Bank API/data acquisition, Pandas, NumPy, data inspection, cleaning, missing-value profiling, validation, exploratory data analysis, visualization and reusable scripts |
| **SQL Server** | Database and table preparation, data loading, SELECT queries, filtering, grouping, aggregations, joins and analytical querying |
| **Microsoft Excel** | Data review, formulas, PivotTables, summary analysis, charts and dashboard-style reporting |
| **Power BI** | Data modeling, KPI cards, DAX measures, interactive visuals, slicers, country/year filtering, report layout and business intelligence storytelling |
| **AI-assisted analytics** | AI-assisted Python and SQL drafting, debugging, formula/query explanations, analytical brainstorming, documentation and communicating findings; outputs checked against the underlying data |

### End-to-end analyst workflow

Data acquisition → data inspection → cleaning and validation → exploratory analysis → SQL analysis → Excel analysis → Power BI reporting → interpretation and documentation.

AI tools were used as productivity support, not as a substitute for data validation or analytical judgment.

---

## 4. Key Findings

The findings below are based on the project dataset and dashboard. Values are rounded as displayed; aggregate definitions and reporting coverage matter when interpreting them.

### 4.1 Global economic overview

| Metric | Dashboard result | Interpretation |
|---|---:|---|
| Nominal GDP, 2024 | **$110.62T** | Sum of reported country-level nominal GDP values in the dataset |
| Average GDP growth KPI | **3.14** | Dashboard KPI; see aggregation caveat below |
| Population, 2024 | **8.12B** | Sum of reported country populations |
| Economies represented | **217** | Economies covered by the project dataset |
| Largest nominal GDP, 2024 | **United States — $29.3T** | Highest economy shown in the dashboard |
| Second-largest nominal GDP, 2024 | **China — $18.7T** | Second-highest economy shown |

**Interpretation:** The dashboard shows the scale and distribution of nominal economic output across economies, alongside a long-term GDP trend and country rankings.

### 4.2 Population and agriculture

| Metric | 2000 | 2024 |
|---|---:|---:|
| Population | **6.14B** | **8.12B** |
| Average agriculture contribution to GDP | **13.4%** | **10.0%** |
| Average agricultural employment | **30.2%** | **~22%** |

**Interpretation:** The dataset's reporting-economy averages show a decline in agriculture's share of GDP and employment over the period, while total population increased. These are descriptive averages, not population-weighted global estimates.

### 4.3 Healthcare and life expectancy

| Metric | Dashboard result |
|---|---:|
| Average life expectancy, 2000 | **67.6 years** |
| Average life expectancy, 2024 | **74.0 years** |
| Healthcare expenditure, 2024 | **9.47% of GDP** |
| Economies reporting healthcare expenditure in 2024 | **22** |

**Interpretation:** Average life expectancy increased across the period. The 2024 healthcare expenditure figure is based on only 22 reporting economies, so it must not be treated as representative of all 217 economies.

The dashboard also includes a comparable 22-economy healthcare expenditure trend to make the change in reporting coverage visible.

### 4.4 Agricultural performance

| Analysis | Dashboard observation |
|---|---|
| Agriculture contribution to GDP | Long-term decline in the displayed average, from 13.4% in 2000 to 10.0% in 2024 |
| Agricultural employment | Long-term decline in the displayed average, from 30.2% to approximately 22% |
| Cereal yield | Large cross-country variation; the displayed top values include Oman, the United Arab Emirates and Qatar |
| Agriculture GDP vs. employment | Country-level scatter analysis used to explore how the two measures vary together |

**Interpretation:** Agriculture's economic and employment shares have declined in the reporting-economy averages, while cereal-yield values vary substantially across countries. Unusually high observations should be investigated before drawing conclusions.

---

## 5. Power BI Dashboard

The Power BI report contains four pages:

| Page | Main contents |
|---|---|
| **Global Economic Overview** | Nominal GDP, average GDP growth KPI, GDP trend, top economies by GDP and GDP per capita |
| **Population & Agriculture** | Population trend, most populous economies and agriculture's GDP contribution |
| **Healthcare & Life Expectancy** | Life expectancy, healthcare expenditure, reporting-economy coverage and country comparisons |
| **Agricultural Performance** | Agriculture's GDP contribution, agricultural employment, cereal yield and cross-country comparison |

### Dashboard screenshots

Add the four dashboard images to the `screenshots/` folder using these exact filenames. The Markdown below will then render them on GitHub.

#### Global Economic Overview
![Global Economic Overview](screenshots/global_economic_overview.png)

#### Population & Agriculture
![Population & Agriculture](screenshots/population_agriculture.png)

#### Healthcare & Life Expectancy
![Healthcare & Life Expectancy](screenshots/healthcare_life_expectancy.png)

#### Agricultural Performance
![Agricultural Performance](screenshots/agricultural_performance.png)

### Power BI report file

The Power BI `.pbix` file may be provided through a Google Drive link if its size exceeds GitHub's standard file-upload limit.

**Power BI report:** Add the shareable Google Drive link in [powerbi/README.md](powerbi/README.md) after confirming that link access is enabled.

---

## 6. Repository Structure

```text
global-economic-development-analytics/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── processed/
├── scripts/
├── notebooks/
├── sql/
├── excel/
├── powerbi/
├── outputs/
│   └── charts/
└── screenshots/
```

See the README files inside individual folders for their contents and usage notes.

---

## 7. Data Quality & Interpretation Limitations

- The dataset contains missing country-indicator-year observations. Missing values were retained rather than automatically converted to zero.
- Indicator coverage varies by country and year. Always check the number of reporting economies before comparing annual averages.
- The 2024 healthcare expenditure result shown in the dashboard covers 22 reporting economies, not all 217.
- GDP per capita is in current US dollars; it is not a purchasing-power-parity measure.
- The GDP growth KPI is an average based on the project's available observations and should not be described as an official, GDP-weighted global growth rate.
- Agriculture and employment averages are descriptive averages across reporting economies, not necessarily weighted by population or economic size.
- Poverty data has substantially lower coverage than several other indicators and requires particular caution.
- Extreme cereal-yield values should be checked for units, source metadata and country-year context before interpretation.
- Relationships shown in charts are descriptive and do not establish causation.

---

## 8. Project Deliverables

- Raw and cleaned World Bank datasets.
- Python scripts and notebooks for data acquisition, cleaning, validation and analysis.
- SQL Server analytical queries.
- Excel analysis workbook.
- Four-page Power BI report.
- Dashboard screenshots, charts and supporting documentation.

---

## 9. What This Project Demonstrates

This project demonstrates the ability to take a real-world public dataset from acquisition through cleaning, validation, analysis and business intelligence reporting. It brings together Python, SQL Server, Excel and Power BI, with AI-assisted development and documentation practices, to answer practical questions about economic and human development.

**Author:** Vansh  
**Data source:** World Bank  
