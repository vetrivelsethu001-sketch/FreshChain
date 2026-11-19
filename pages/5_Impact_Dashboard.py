import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from utils.common import setup


def demo_data():
    rng = np.random.default_rng(16)
    rows = []
    for week in range(1, 9):
        for hub in ("Koyambedu", "Tambaram", "Chengalpattu"):
            volume = int(rng.integers(5000, 8500))
            avoided = round(volume * rng.uniform(0.035, 0.085))
            rows.append((week, hub, avoided, avoided * int(rng.integers(18, 36)),
                         int(rng.integers(55, 94))))
    return pd.DataFrame(rows, columns=["Week", "Hub", "Waste avoided (kg)",
                        "Farmer savings (₹)", "Utilization (%)"])


def main():
    setup("Impact Dashboard", "📊")
    st.title("📊 Impact dashboard")
    st.info("Simulated eight-week scenario for fruit and vegetable rooms. All figures are demo data.")
    df = demo_data()
    hubs = st.multiselect("Storage hubs", df.Hub.unique(), default=df.Hub.unique())
    df = df[df.Hub.isin(hubs)]
    if df.empty:
        st.info("Select a hub to view its impact.")
        return
    waste, money, utilization = df.columns[2:]
    weekly = df.groupby("Week", as_index=False).agg({waste: "sum", money: "sum", utilization: "mean"})
    a, b, c = st.columns(3)
    a.metric("Estimated waste avoided", f"{df[waste].sum():,} kg")
    b.metric("Estimated farmer savings", f"₹{df[money].sum():,}")
    c.metric("Mean storage utilization", f"{df[utilization].mean():.1f}%")
    for tab, metric in zip(st.tabs(["Waste avoided", "Money saved", "Utilization"]), df.columns[2:]):
        with tab:
            fig = px.bar(weekly, x="Week", y=metric, color_discrete_sequence=["#168440"])
            if metric == utilization:
                fig.update_yaxes(range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
    st.caption("Waste avoided = volume × simulated reduction in loss. Savings = avoided kg × "
               "demo farm price. Utilization is the mean simulated occupied share across selected hubs.")


if __name__ == "__main__":
    main()
