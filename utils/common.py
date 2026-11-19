from pathlib import Path
from uuid import uuid4

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).resolve().parents[1] / "data"
TOWNS = {"Koyambedu": (13.069, 80.195), "Tambaram": (12.925, 80.121),
         "Chengalpattu": (12.692, 79.976), "Madhavaram": (13.148, 80.231)}
# Temperature, humidity and shelf-life assumptions for the synthetic demo.
PROFILES = {"Fruits": (4, 8, 85, 95, 168),
            "Vegetables": (2, 6, 85, 95, 120),
            "Milk": (1, 4, 45, 65, 72)}


def setup(title, icon):
    st.set_page_config(page_title=f"{title} · FreshChain", page_icon=icon, layout="wide")
    st.sidebar.markdown("**🌱 FreshChain**")
    st.sidebar.caption("Chennai region · simulated network")
    for key in ("reservations", "bookings"):
        st.session_state.setdefault(key, [])


def catalog(file, columns):
    try:
        data = pd.read_csv(DATA / file).loc[:, columns]
        if data.empty or data.isna().any().any():
            raise ValueError("Empty or incomplete catalogue")
        return data
    except (OSError, ValueError, KeyError) as exc:
        st.error(f"Could not load {file}. Check the bundled CSV. {exc}")
        st.stop()


def distance(origin, lat, lon):
    a, b = np.radians(origin)
    c, d = np.radians(lat), np.radians(lon)
    h = np.sin((c-a)/2)**2 + np.cos(a)*np.cos(c)*np.sin((d-b)/2)**2
    return 12742 * np.arcsin(np.sqrt(np.clip(h, 0, 1)))


def identifier(prefix):
    return f"{prefix}-{uuid4().hex[:8].upper()}"


def unit(produce):
    return "L" if produce == "Milk" else "kg"


def gauge(label, value, limits, suffix, color):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=value,
        title={"text": label}, number={"suffix": suffix},
        gauge={"axis": {"range": limits}, "bar": {"color": color}}))
    fig.update_layout(height=220, margin=dict(l=35, r=35, t=55, b=15))
    st.plotly_chart(fig, use_container_width=True)
