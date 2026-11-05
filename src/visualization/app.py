"""
Interactive Early Warning & Forecasting Dashboard for Monsoon Flooding in Nepal
Built with Streamlit, Plotly, Folium, and Machine Learning Backends.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from pathlib import Path

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Nepal Monsoon Flood Early Warning System",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #E2E8F0;
        text-align: center;
    }
    .alert-watch {
        background-color: #FEF08A;
        color: #854D0E;
        padding: 10px;
        border-radius: 6px;
        font-weight: bold;
    }
    .alert-warning {
        background-color: #FED7AA;
        color: #9A3412;
        padding: 10px;
        border-radius: 6px;
        font-weight: bold;
    }
    .alert-evac {
        background-color: #FECACA;
        color: #991B1B;
        padding: 10px;
        border-radius: 6px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_processed_data():
    csv_path = Path("data/processed/monsoon_features_2022.csv")
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        df['date'] = pd.to_datetime(df['date'])
        return df
    return None


@st.cache_data
def load_model_metrics():
    metrics_path = Path("outputs/baseline_model_evaluation_table.csv")
    if metrics_path.exists():
        return pd.read_csv(metrics_path)
    return None


df_monsoon = load_processed_data()
df_metrics = load_model_metrics()

# --- Header Section ---
st.markdown('<div class="main-header">🌊 Nepal Monsoon Flood Early Warning System (FEWS)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Spatiotemporal Deep Learning & Antecedent Soil Moisture Hydro-Hazard Intelligence</div>', unsafe_allow_html=True)

# --- Sidebar Controls ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/9/9b/Flag_of_Nepal.svg", width=60)
st.sidebar.header("🕹️ Dashboard Controls")

view_mode = st.sidebar.radio(
    "Select View Mode:",
    ["🚨 Live Early Warning Monitor", "📈 Multi-Horizon Forecast Explorer", "🤖 AI Model Benchmark Hub", "🗺️ Transboundary Basin Cartography"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Lead Time Warning Horizon:** 24 Hours")
st.sidebar.markdown("**Basin Focus:** Koshi, Gandaki, Karnali, West Rapti")
st.sidebar.markdown("**Data Feeds:** NASA GPM, CHIRPS 0.05°, ERA5-Land Reanalysis")

# --- Tab 1: Live Early Warning Monitor ---
if view_mode == "🚨 Live Early Warning Monitor":
    st.subheader("Current Monsoon Early Warning & Runoff Potential Index (RPI)")

    if df_monsoon is not None:
        # Date selector slider
        date_list = df_monsoon['date'].dt.strftime('%Y-%m-%d').tolist()
        selected_date_str = st.select_slider(
            "Select Monsoon Observation Date (June - September):",
            options=date_list,
            value=date_list[-15]
        )
        row = df_monsoon[df_monsoon['date'] == selected_date_str].iloc[0]

        # Top summary metric cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Daily Mean Precipitation", value=f"{row['precip_mean_mm']:.1f} mm/day", delta=f"{row['precip_mean_mm'] - row['precip_lag_1d']:.1f} mm vs yesterday")
        with col2:
            st.metric(label="Top-Layer Soil Moisture (L1)", value=f"{row['soil_moisture_l1']:.3f} m³/m³", delta="Saturation Index")
        with col3:
            st.metric(label="Runoff Potential Index (RPI)", value=f"{row['RPI']:.2f}")
        with col4:
            alert_level = int(row['flood_alert_level'])
            if alert_level == 0:
                st.markdown('<div class="metric-card" style="background-color: #DCFCE7; color: #166534; font-weight: bold;">🟢 NORMAL STATUS<br>No Imminent Hazard</div>', unsafe_allow_html=True)
            elif alert_level == 1:
                st.markdown('<div class="metric-card alert-watch">🟡 WATCH LEVEL (RPI ≥ 0.50)<br>Heightened Soil Wetness</div>', unsafe_allow_html=True)
            elif alert_level == 2:
                st.markdown('<div class="metric-card alert-warning">🟠 WARNING LEVEL (RPI ≥ 0.75)<br>Severe Runoff Threat</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-card alert-evac">🔴 EVACUATION ALERT (RPI ≥ 1.00)<br>Flash Flood Critical Notice</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Interactive Timeline Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_monsoon['date'], y=df_monsoon['precip_mean_mm'],
            mode='lines', name='Daily Rainfall (mm)',
            line=dict(color='#1E40AF', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df_monsoon['date'], y=df_monsoon['RPI'] * 20,
            mode='lines', name='RPI Scaled (x20)',
            line=dict(color='#DC2626', width=2.5, dash='dot')
        ))
        fig.add_vline(x=pd.to_datetime(selected_date_str), line_width=2, line_dash="dash", line_color="black")
        fig.update_layout(
            title="Monsoon Timeline: Dynamic Coupling of Precipitation with Runoff Potential",
            xaxis_title="Date",
            yaxis_title="Intensity / Index",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Processed features not loaded. Run `python -m src.features.build_features` first.")

# --- Tab 2: Multi-Horizon Forecast Explorer ---
elif view_mode == "📈 Multi-Horizon Forecast Explorer":
    st.subheader("Multi-Horizon Lead Time Forecaster (24-Hour Evaluation)")
    
    if df_monsoon is not None:
        colA, colB = st.columns([2, 1])
        with colA:
            # 24h Actual vs Target Comparison
            fig_pred = px.line(
                df_monsoon, x="date", y=["precip_mean_mm", "target_precip_lead_1d"],
                labels={"value": "Rainfall (mm)", "date": "Date", "variable": "Stream"},
                title="Observed vs 24-Hour Forward Lead-Time Target"
            )
            fig_pred.update_layout(legend_title_text='Series')
            st.plotly_chart(fig_pred, use_container_width=True)
        with colB:
            st.markdown("### 💡 Early Warning Value")
            st.info(
                """
                **Why 24h Predictive Warning Matters:**
                - **Traditional Point Stage Gauges:** Give downstream Terai plains only **2 to 4 hours** notice before bank overflow.
                - **Coupled ML Nowcasting:** Extends evacuation lead times to **12–24 hours** by anticipating orographic lifting and cloudbursts before runoff enters river channels.
                """
            )
            st.image("figures/monsoon_rpi_leadtime_evaluation.png", caption="Model Dynamic Alert Matrix", use_container_width=True)

# --- Tab 3: AI Model Benchmark Hub ---
elif view_mode == "🤖 AI Model Benchmark Hub":
    st.subheader("Empirical Model Performance & Benchmark Comparison")
    st.markdown("Evaluated on held-out monsoon test sequences across standard hydrological and machine learning metrics:")

    if df_metrics is not None:
        st.dataframe(df_metrics, use_container_width=True)

        fig_bar = px.bar(
            df_metrics, x="Model", y="RMSE (mm)",
            color="Model", text_auto=True,
            title="Model Comparison by Root Mean Squared Error (RMSE) - Lower is Better"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Benchmark metrics table not found in `outputs/`.")

# --- Tab 4: Transboundary Basin Cartography ---
elif view_mode == "🗺️ Transboundary Basin Cartography":
    st.subheader("Interactive Nepal River Basin Risk Map")

    # Center map on Central Nepal
    m = folium.Map(location=[28.3949, 84.1240], zoom_start=7, tiles="CartoDB positron")

    # Critical Gauge Stations (from config.yaml)
    gauges = [
        {"name": "Chatara (Koshi Basin)", "lat": 26.8667, "lon": 87.1500, "status": "Warning"},
        {"name": "Devghat (Gandaki Basin)", "lat": 27.7000, "lon": 84.4167, "status": "Watch"},
        {"name": "Chisapani (Karnali Basin)", "lat": 28.6500, "lon": 81.2833, "status": "Normal"},
        {"name": "Kusum (West Rapti Basin)", "lat": 27.9833, "lon": 82.1167, "status": "Evacuation"}
    ]

    for g in gauges:
        color = "red" if g["status"] == "Evacuation" else ("orange" if g["status"] == "Warning" else ("yellow" if g["status"] == "Watch" else "green"))
        folium.CircleMarker(
            location=[g["lat"], g["lon"]],
            radius=9,
            popup=f"<b>{g['name']}</b><br>Status: {g['status']}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8
        ).add_to(m)

    st_folium(m, width=1100, height=520)

st.markdown("---")
st.caption("Developed for MSc Data Science & AI Research | Softwarica College of IT & E-Commerce | softwarica.edu.np")

