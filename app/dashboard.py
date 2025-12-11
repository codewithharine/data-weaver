from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from .data_fetch import get_bitcoin_prices, get_earthquakes
from .transformations import merge_crypto_and_quakes, compute_correlations


def run_dashboard():
    st.set_page_config(
        page_title="Quakes & Coins: The Data Weaver",
        layout="wide"
    )

    st.title("🌍💰 Quakes & Coins: The Data Weaver")
    st.caption("Bitcoin prices vs global earthquakes – a totally unnecessary but fun mashup 😄")

    # Sidebar controls
    with st.sidebar:
        st.header("Filters")
        days = st.slider("Number of days (past)", 7, 90, 30)
        min_mag = st.slider("Minimum magnitude", 2.5, 7.0, 3.0, 0.5)

        st.markdown("---")
        st.write("Data source:")
        st.write("- Bitcoin: CoinGecko API")
        st.write("- Earthquakes: USGS Earthquake Catalog API")

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)

    st.subheader("Selected Range")
    st.write(f"From **{start_date}** to **{end_date}**, min magnitude **{min_mag}**")

    # Fetch data
    with st.spinner("Fetching Bitcoin prices..."):
        btc_df = get_bitcoin_prices(days=days)

    with st.spinner("Fetching earthquake data..."):
        eq_df = get_earthquakes(
            start_date=datetime.combine(start_date, datetime.min.time()),
            end_date=datetime.combine(end_date, datetime.min.time()),
            min_magnitude=min_mag,
        )

    merged_df = merge_crypto_and_quakes(btc_df, eq_df)

    corr_price_count, corr_price_mag = compute_correlations(merged_df)

    # Top metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Last BTC Price (USD)",
            f"${merged_df['price_usd'].iloc[-1]:,.0f}"
        )
    with col2:
        total_quakes = int(merged_df["eq_count"].sum())
        st.metric("Total Earthquakes", f"{total_quakes}")
    with col3:
        st.metric(
            "Average Magnitude",
            f"{merged_df['avg_mag'].replace(0, pd.NA).mean():.2f}"
            if (merged_df["avg_mag"] != 0).any()
            else "N/A"
        )

    st.markdown("---")

    # Charts
    tab1, tab2, tab3 = st.tabs(
        ["📈 Bitcoin Price", "🌋 Earthquakes", "🔗 Combined View"]
    )

    with tab1:
        fig_price = px.line(
            merged_df,
            x="date",
            y="price_usd",
            labels={"date": "Date", "price_usd": "BTC Price (USD)"},
            title="Bitcoin Price Over Time",
        )
        st.plotly_chart(fig_price, use_container_width=True)

    with tab2:
        if not merged_df["eq_count"].sum():
            st.info("No earthquakes found for this range and magnitude filter.")
        else:
            fig_quakes = px.bar(
                merged_df,
                x="date",
                y="eq_count",
                labels={"date": "Date", "eq_count": "Earthquake Count"},
                title="Earthquake Count Per Day",
            )
            st.plotly_chart(fig_quakes, use_container_width=True)

            fig_mag = px.line(
                merged_df,
                x="date",
                y="avg_mag",
                labels={"date": "Date", "avg_mag": "Average Magnitude"},
                title="Average Magnitude Per Day",
            )
            st.plotly_chart(fig_mag, use_container_width=True)

    with tab3:
        if len(merged_df) > 1:
            fig_combo = px.scatter(
                merged_df,
                x="eq_count",
                y="price_usd",
                size="avg_mag",
                hover_name="date",
                labels={
                    "eq_count": "Earthquake Count",
                    "price_usd": "BTC Price (USD)",
                    "avg_mag": "Average Magnitude",
                },
                title="BTC Price vs Earthquake Count (bubble size = avg magnitude)",
            )
            st.plotly_chart(fig_combo, use_container_width=True)

            st.subheader("Correlation Snapshot")
            st.write(
                f"- BTC price vs **quake count**: `{corr_price_count:.3f}`"
                if corr_price_count is not None
                else "- Not enough data for correlation."
            )
            st.write(
                f"- BTC price vs **average magnitude**: `{corr_price_mag:.3f}`"
                if corr_price_mag is not None
                else "- Not enough data for correlation."
            )
        else:
            st.info("Not enough data points for combined analysis.")
