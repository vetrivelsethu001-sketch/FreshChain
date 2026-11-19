import streamlit as st
from utils.common import PROFILES, gauge, setup
from utils.predictor import predict


def main():
    setup("Spoilage Predictor", "🌿")
    st.title("🌿 Spoilage predictor")
    st.caption("Synthetic model · risk is a demo score, not a measured probability or food-safety assessment.")
    produce = st.selectbox("Produce", list(PROFILES))
    lo, hi, dry, wet, _ = PROFILES[produce]
    a, b, c = st.columns(3)
    temp = a.slider("Current temperature (°C)", -5.0, 40.0, (lo + hi) / 2, 0.5, key=f"t{produce}")
    rh = b.slider("Room humidity (%)", 20, 100, (dry + wet) // 2, key=f"h{produce}")
    hours = c.slider("Hours in storage or transit", 0, 240, 24)
    risk, life = predict(produce, temp, rh, hours)
    level, color = ("Low", "#168440") if risk < 35 else (
        ("Elevated", "#C88410") if risk < 70 else ("High", "#C63E39"))
    a, b = st.columns(2)
    with a:
        gauge(f"{level} spoilage risk", round(risk, 1), [0, 100], "%", color)
    b.metric("Estimated remaining shelf life", f"{life:.1f} hours")
    b.caption("Assumes the batch stays at the selected conditions.")
    st.subheader("Batch handling tips")
    if not lo <= temp <= hi:
        st.write(f"• Inspect the cooling controls. This demo room targets {lo}–{hi} °C.")
    if not dry <= rh <= wet:
        st.write("• Inspect the room humidity sensor and airflow.")
    st.write("• Prioritize older batches for dispatch and minimize time at the loading bay.")


if __name__ == "__main__":
    main()
