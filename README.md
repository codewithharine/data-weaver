# Quakes & Coins: The Data Weaver

Week 3 challenge for **Kiro AI for Bharat – The Data Weaver**.

This dashboard mashes up:

- **Bitcoin price data** (CoinGecko API)
- **Global earthquake data** (USGS Earthquake Catalog API)

to explore a playful question:  
> Do earth-shaking events have anything to do with Bitcoin’s daily price?

## Tech Stack

- Python
- Streamlit
- pandas
- requests
- plotly
- Kiro (IDE) – using `.kiro` steering/spec files

## How to Run

```bash
# Create & activate venv if you want
pip install -r requirements.txt
streamlit run streamlit_app.py
