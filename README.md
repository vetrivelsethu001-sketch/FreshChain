# 🌱 FreshChain

**From farm to market. Zero spoilage.**  
Smart Cold-Chain & Agricultural Produce Preservation Network  
**Team 15, 16 - Clue 2 Crew 2**

## Problem and solution

A farmer preparing to send produce to market needs to know where space is available, whether a batch is warming up, and which truck can carry it. FreshChain connects those decisions in a single Streamlit demo using fictional facilities around Chennai.

## Features

- **Home** — English, Hindi and Telugu home labels, navigation cards and catalogue counts.
- **Find** — compare compatible rooms within 60 km by available space, price and temperature. Reserve kg of produce or litres of milk. One facility row represents one dedicated room or tank.
- **Monitor** — 24 timestamped readings per produce type, gauges, trend charts and on-screen SMS-style alerts. Choose a scenario and refresh to add a minute. Warning starts outside the demo band. Critical starts 3 °C or 10 humidity percentage points beyond a boundary.
- **Move** — compare refrigerated trucks, book a pickup day and advance a simulated shipment using its tracking ID. Each truck accepts one trip per date.
- **Predict** — a small regression model learns synthetic deterioration from exposure time, temperature deviation and room humidity deviation. It estimates the fraction of a demo shelf life consumed and hours remaining at constant conditions.
- **Impact** — inspect eight simulated weeks of avoided produce waste, estimated farmer savings and mean storage utilization by hub.

The demo uses local CSVs, simulated telemetry and in-memory session state. Reloading the browser or starting a new session can reset bookings and reservations. Other users have independent inventories. SMS messages appear in the app. Map tiles use OpenStreetMap over the internet. Comparisons and booking work without a basemap. No credentials are required.

Temperature bands and shelf-life estimates are illustrative. Actual storage requirements depend on the commodity, handling and packaging. Use the predictor for demonstrations only.

## Tech stack

Python 3.10–3.12, Streamlit, pandas, NumPy, Plotly, scikit-learn, Folium, streamlit-folium and PyArrow. Python 3.12 is the tested version.

## Project layout

```text
FreshChain/
├── app.py
├── pages/
│   ├── 1_Find_Storage.py
│   ├── 2_Live_Monitoring.py
│   ├── 3_Book_Transport.py
│   ├── 4_Spoilage_Predictor.py
│   └── 5_Impact_Dashboard.py
├── data/
│   ├── storages.csv
│   └── transport.csv
├── utils/
│   ├── common.py
│   ├── sensor_sim.py
│   └── predictor.py
├── .streamlit/config.toml
├── .gitignore
├── requirements.txt
└── README.md
```

## Run locally

Extract the ZIP, open a terminal inside the folder containing app.py, and use a virtual environment. On Windows PowerShell, these commands work without activating scripts or changing execution policy.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

On macOS or Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501. For a quick demo, reserve 100 kg of fruit near Koyambedu, trigger a cooling failure in Live Monitoring, then book Mango Express to Tambaram and advance its tracking status.

## Screenshots

_Placeholders for the home screen, storage comparison, critical sensor alert and shipment tracker._

## Push to a new GitHub repository

Run these commands inside FreshChain with Git and GitHub CLI installed. The last command creates a public repository under the signed-in GitHub account, sets origin and pushes main. Use --private for a private repository.

```bash
gh auth login
git init -b main
git add .
git commit -m "Build FreshChain cold-chain demo"
gh repo create FreshChain --public --source=. --remote=origin --push
```

## Deploy on Streamlit Community Cloud

1. Push the project with app.py and requirements.txt in the repository root.
2. Sign in at https://share.streamlit.io and connect GitHub.
3. Choose **Create app**, then **Yup, I have an app**.
4. Select the FreshChain repository, branch **main**, and entrypoint **app.py**.
5. In **Advanced settings**, choose Python **3.12**. Click **Deploy**.

[Streamlit deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
