from datetime import date
from math import ceil
import streamlit as st
from utils.common import PROFILES, TOWNS, catalog, distance, identifier, setup

STAGES = ["Confirmed", "Collected", "In transit", "Delivered"]


def tracking(bookings):
    st.subheader("Your shipments")
    if not bookings:
        st.info("Book a truck to start tracking.")
        return
    ref = st.selectbox("Tracking ID", [b["id"] for b in reversed(bookings)])
    shipment = next(b for b in bookings if b["id"] == ref)
    stage = shipment["stage"]
    st.write(f"{shipment['truck']} · {shipment['produce']} · {shipment['route']}")
    st.caption(f"Pickup {shipment['date']} · ₹{shipment['cost']:,} · estimated {shipment['eta']} min")
    st.progress((stage + 1) / len(STAGES), text=STAGES[stage])
    if stage < len(STAGES) - 1 and st.button("Advance demo shipment"):
        shipment["stage"] += 1
        st.rerun()


def main():
    setup("Book Transport", "🚚")
    st.title("🚚 Book transport")
    a, b = st.columns(2)
    produce = a.selectbox("Produce", list(PROFILES))
    day = b.date_input("Pickup date", min_value=date.today())
    pickup = a.selectbox("Pickup", list(TOWNS))
    dest = b.selectbox("Destination", [t for t in TOWNS if t != pickup])
    trucks = catalog("transport.csv", ["truck", "produce", "cooling", "rating", "base", "per_km"])
    bookings = st.session_state.bookings
    busy = {r["truck"] for r in bookings if r["date"] == day}
    trucks = trucks[(trucks.produce == produce) & ~trucks.truck.isin(busy)].copy()
    km = 1.25 * distance(TOWNS[pickup], *TOWNS[dest])
    eta = 15 + ceil(km / 35 * 60)
    trucks["Fare (₹)"] = (trucks.base + km * trucks.per_km).round().astype(int)
    trucks["ETA (min)"] = eta
    if msg := st.session_state.pop("truck_message", None):
        st.success(msg)
    st.caption(f"Demo route estimate · {km:.1f} km · ETA includes loading")
    if trucks.empty:
        st.info("No compatible truck available. Try another pickup date.")
    else:
        st.dataframe(trucks[["truck", "rating", "cooling", "Fare (₹)", "ETA (min)"]],
                     use_container_width=True, hide_index=True)
        truck = st.selectbox("Available truck", trucks.truck)
        if st.button("Book truck", type="primary"):
            ref = identifier("FC")
            cost = int(trucks.loc[trucks.truck == truck, "Fare (₹)"].iloc[0])
            bookings.append(dict(id=ref, truck=truck, produce=produce, date=day,
                                 route=f"{pickup} → {dest}", cost=cost, eta=eta, stage=0))
            st.session_state.truck_message = f"Booking confirmed. Tracking ID {ref}."
            st.rerun()
    tracking(bookings)


if __name__ == "__main__":
    main()
