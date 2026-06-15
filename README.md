# StockVision — Stock Market Volatility Intelligence

An end-to-end data analytics project analysing 15 years of real stock market
data across **80 stocks** from Indian (NIFTY 50) and US (S&P 500) markets to
identify highly volatile stocks and surface actionable insights for traders
and trading companies.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data collection | Python · yfinance |
| Storage | MySQL 8.0 · SQLAlchemy |
| Analysis | pandas · NumPy · SciPy |
| Visualisation | Plotly · Seaborn |
| Dashboard | Streamlit |
| IDE | VS Code |

---

## Key Features

- **Real data** — 15 years of daily OHLCV data (2010–2024), ~290K rows
- **Dual market** — India (NSE) and US (NYSE/NASDAQ) in one pipeline
- **3 volatility metrics** — Annualised volatility, ATR-14, Max Drawdown
- **Risk-return analysis** — CAGR, Sharpe Ratio, Calmar Ratio per stock
- **9 SQL business queries** — returns, rankings, seasonality, trend signals
- **Interactive dashboard** — 4-tab Streamlit app with live filters

---

## Key Insights

| Insight | Finding |
|---|---|
| Best performer | NVDA — 32,332% total return (2010–2024) |
| Best Indian stock | BAJFINANCE.NS — 22,508% total return |
| Most volatile sector | US Communication — 40.16% annualised volatility |
| Best risk-adjusted | US stocks — Sharpe 0.74 vs India 0.67 |
| Worst month (both) | September — negative avg returns every year |
| Strongest month (US) | November — +0.207% avg daily return |
| Bull signals (latest) | DIVISLAB.NS — 24.37% above 200-day MA |

---

## Project Structure

```
StockVision/
├── data/
│   ├── raw/india/          # NIFTY 50 CSVs (gitignored)
│   ├── raw/us/             # S&P 500 CSVs (gitignored)
│   └── processed/          # Cleaned data + correlation matrices
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_load_to_mysql.ipynb
│   ├── 03_cleaning_features.ipynb
│   ├── 04_sql_insights.ipynb
│   ├── 05_volatility_analysis.ipynb
│   ├── 06_risk_return.ipynb
│   └── 07_visualizations.ipynb
├── sql/
│   ├── schema.sql
│   └── queries/
│       ├── 01_return_analysis.sql
│       ├── 02_top_performers.sql
│       ├── 03_market_comparison.sql
│       └── 04_trend_volume.sql
├── dashboard/
│   └── app.py              # Streamlit dashboard
├── visuals/                # Saved HTML charts
├── config_template.py      # Credential template
├── requirements.txt
└── README.md
```

---

## Setup & Installation

**1. Clone the repo**
```bash
git clone https://github.com/Ankit-Singh-k/StockVision.git
cd StockVision
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure credentials**
```bash
cp config_template.py config.py
# Edit config.py and add your MySQL password
```

**4. Create the MySQL database**
```sql
CREATE DATABASE stockvision CHARACTER SET utf8mb4;
```

**5. Run the notebooks in order**
```
01 → 02 → 03 → 04 → 05 → 06 → 07
```

**6. Launch the dashboard**
```bash
streamlit run dashboard/app.py
```

---

## MySQL Schema

| Table | Rows | Description |
|---|---|---|
| `stocks` | 80 | Master table — ticker, company, market, sector |
| `daily_prices` | ~290K | Raw OHLCV data per stock per day |
| `stock_features` | ~290K | Engineered — daily return, log return, MA50, MA200 |
| `stock_volatility` | 79 | Volatility metrics + ranking per stock |
| `stock_risk_return` | 79 | CAGR, Sharpe Ratio, Calmar Ratio per stock |

---

## Author

**Ankit Singh** · B.Tech AI/ML · Rai University, Ahmedabad  
[GitHub](https://github.com/ankit_singh09)