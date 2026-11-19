import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from utils.common import PROFILES, TOWNS, catalog, distance, identifier, setup, unit


def show_map(origin, sites):
    chart = folium.Map(location=origin, zoom_start=10)
    folium.Marker(origin, tooltip="Your location", icon=folium.Icon(color="blue")).add_to(chart)
    points = [origin]
    for row in sites.itertuples():
        point = (row.lat, row.lon)
        points.append(point)
        folium.Marker(point, tooltip=row.name, icon=folium.Icon(color="green")).add_to(chart)
    chart.fit_bounds(points, max_zoom=13)
    st_folium(chart, use_container_width=True, height=330, returned_objects=[])


def main():
    setup("Find Storage", "📍")
    st.title("📍 Find storage")
    st.caption("Demo facilities within 60 km · straight-line distances")
    a, b, c = st.columns(3)
    produce = a.selectbox("Produce", PROFILES.keys())
    town = b.selectbox("Farmer location", TOWNS.keys())
    u = unit(produce)
    qty = c.number_input(f"Quantity ({u})", 1, 100000, 100)
    maximum = st.slider(f"Maximum daily rate (₹/{u})", 0.0, 3.0, 3.0, 0.1)
    sites = catalog("storages.csv", ["name", "produce", "lat", "lon", "capacity", "rate", "tmin", "tmax"])
    reserved = st.session_state.reservations
    used = {}
    for r in reserved:
        used[r["Site"]] = used.get(r["Site"], 0) + r["Quantity"]
    sites["available"] = (sites.capacity - sites.name.map(used).fillna(0)).astype(int)
    sites["km"] = distance(TOWNS[town], sites.lat, sites.lon)
    sites = sites[(sites.produce == produce) & (sites.rate <= maximum) &
                  (sites.available >= qty) & (sites.km <= 60)].sort_values("km")
    if message := st.session_state.pop("space_message", None):
        st.success(message)
    if sites.empty:
        st.info("No storage matches. Try a smaller quantity, another town or a higher price.")
    else:
        table, map_tab = st.tabs(["Compare facilities", "Map"])
        with table:
            st.dataframe(pd.DataFrame({"Facility": sites.name, "Distance (km)": sites.km.round(1),
                f"Available ({u})": sites.available, f"₹/{u}/day": sites.rate,
                "Your cost (₹/day)": (sites.rate * qty).round(2),
                "Room (°C)": sites.tmin.astype(str) + "–" + sites.tmax.astype(str)}),
                hide_index=True, use_container_width=True)
        with map_tab:
            st.caption("Map tiles need internet. Facility comparison works offline.")
            show_map(TOWNS[town], sites)
        site = st.selectbox("Reserve at", sites.name)
        if st.button("Reserve Space", type="primary"):
            ref = identifier("RS")
            reserved.append({"ID": ref, "Site": site, "Produce": produce, "Quantity": qty, "Unit": u})
            st.session_state.space_message = f"Reserved {qty} {u} at {site}. Reference {ref}."
            st.rerun()
    if reserved:
        st.subheader("Your reservations")
        st.dataframe(pd.DataFrame(reserved), hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()
