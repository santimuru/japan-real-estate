# Japan Real Estate Intelligence

Interactive Streamlit app for exploring Japan's property market using government transaction data from the Ministry of Land, Infrastructure, Transport and Tourism (MLIT).

**Live demo:** https://japan-real-estate-santimuru.streamlit.app
**Portfolio:** https://santimuru.github.io

---

## What it covers

- **Japan Overview** · Choropleth of all 47 prefectures ranked by median ¥/m², population change vs price appreciation scatter, and the akiya (vacant home) crisis mapped and trended across 2013/2018/2023.
- **City Comparison** · Select 2–5 cities and compare transaction-level MLIT data: quarterly price trends, median ¥/m², YoY change, and property type mix.
- **Tokyo Deep Dive** · Ward-level analytics for Tokyo's 23 Special Wards: choropleth map, ranking table, price trends, ward-year heatmap, k-NN price estimator (P10/P50/P90), and an investment value score combining momentum and relative affordability.
- **About** · Full data source documentation, methodology notes, and known limitations.

---

## Data

| Source                         | Coverage                                           | Used in                          |
| ------------------------------ | -------------------------------------------------- | -------------------------------- |
| MLIT XIT001 API                | Transaction-level, all prefectures, ~2-quarter lag | City Comparison, Tokyo Deep Dive |
| MLIT aggregate reports / REINS | Prefecture price estimates 2015–2024               | Japan Overview price map         |
| Japan Housing and Land Survey  | Akiya rates 2013 / 2018 / 2023                     | Akiya section                    |
| Statistics Bureau of Japan     | Prefectural population 2010 / 2020                 | Demographics scatter             |
| dataofjapan/land (GitHub)      | Prefecture GeoJSON boundaries                      | All choropleths                  |

The Japan Overview choropleth uses curated prefecture-level aggregates, not raw API output. For transaction-level live data, use City Comparison or Tokyo Deep Dive.

**Backends:** the app checks for a cached parquet file first, then the live MLIT API (`DATA_SOURCE=mlit_api`), then falls back to a synthetic dataset (~50K transactions) modeled after MLIT public aggregates.

---

## Tech stack

| Layer          | Tools                                                  |
| -------------- | ------------------------------------------------------ |
| Language       | Python 3.11                                            |
| App framework  | Streamlit                                              |
| Visualisation  | Plotly Express, Plotly Graph Objects                   |
| Data wrangling | Pandas, NumPy                                          |
| Geospatial     | Plotly choropleth mapbox + dataofjapan/land GeoJSON    |
| API            | MLIT Real Estate Information Library · XIT001 endpoint |
| Hosting        | Streamlit Community Cloud                              |

---

## Run locally

```bash
git clone https://github.com/santimuru/japan-real-estate.git
cd japan-real-estate
pip install -r requirements.txt
streamlit run app.py
```

To use the live MLIT API (free key at reinfolib.mlit.go.jp):

```bash
export DATA_SOURCE=mlit_api
export MLIT_API_KEY=your_subscription_key_here
streamlit run app.py
```

---

## Project structure

```
japan-real-estate/
├── app.py                        # Landing page / hero
├── pages/
│   ├── 0_Japan_Overview.py       # 47-prefecture choropleth + akiya crisis
│   ├── 1_City_Comparison.py      # Multi-city MLIT comparison
│   ├── 2_Tokyo_Deep_Dive.py      # 23-ward analytics + estimator
│   └── 3_About.py                # Methodology and data sources
├── utils/
│   ├── data_loader.py            # Parquet / MLIT API / synthetic backends
│   ├── ward_data.py              # Ward metadata (coords, base prices, stations)
│   ├── prefecture_data.py        # Prefecture metadata and akiya rates
│   └── analytics.py             # Aggregations + k-NN price estimator
├── data/
│   ├── prefecture_aggregates.parquet
│   ├── prefecture_aggregates_by_type.parquet
│   ├── ward_transactions.parquet
│   └── tokyo23_wards.geojson
├── .streamlit/config.toml        # Dark theme config
└── requirements.txt
```

---

## Author

**Santiago Martinez** · data analyst

- Portfolio: https://santimuru.github.io
- GitHub: https://github.com/santimuru

---

## License

MIT
