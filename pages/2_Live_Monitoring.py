from datetime import timedelta
import pandas as pd
import plotly.express as px
import streamlit as st
from utils.common import PROFILES, gauge, setup
from utils.sensor_sim import history, reading, status


def main():
    setup("Live Monitoring", "🌡️")
    st.title("🌡️ Live monitoring")
    produce = st.selectbox("Monitored batch", list(PROFILES))
    lo, hi, dry, wet, _ = PROFILES[produce]
    st.caption(f"Demo targets · {lo}–{hi} °C · {dry}–{wet}% room humidity")
    streams = st.session_state.setdefault("streams", {})
    if produce not in streams:
        streams[produce] = history(produce)
    rows = streams[produce]
    scenario = st.selectbox("Next reading scenario", ["Normal", "Door opened", "Cooling failure"])
    if st.button("Refresh readings", type="primary"):
        stamp = rows[-1]["Time"] + timedelta(minutes=1)
        rows.append(reading(produce, stamp, scenario))
        del rows[:-24]
    current = rows[-1]
    temp, humidity = current["Temperature (°C)"], current["Humidity (%)"]
    state = status(produce, temp, humidity)
    colors = {"Safe": "#168440", "Warning": "#C88410", "Critical": "#C63E39"}
    st.badge(state, color={"Safe": "green", "Warning": "orange", "Critical": "red"}[state])
    if state != "Safe":
        st.error(f"📩 Demo SMS · {state}: {produce} room at {temp} °C and {humidity}% RH. "
                 "Check the door seal and cooling unit.")
    a, b = st.columns(2)
    with a:
        gauge("Temperature", temp, [-5, 25], " °C", colors[state])
    with b:
        gauge("Room humidity", humidity, [0, 100], "%", colors[state])
    st.subheader("Last 24 readings")
    st.caption("Each refresh advances the simulation by one minute.")
    frame = pd.DataFrame(rows)
    for tab, label in zip(st.tabs(["Temperature", "Humidity"]), frame.columns[1:]):
        with tab:
            st.plotly_chart(px.line(frame, x="Time", y=label, markers=True,
                            color_discrete_sequence=["#168440"]), use_container_width=True)


if __name__ == "__main__":
    main()
