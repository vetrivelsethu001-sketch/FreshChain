from datetime import datetime, timedelta
import numpy as np
from utils.common import PROFILES


def reading(produce, stamp, scenario="Normal"):
    lo, hi, dry, wet, _ = PROFILES[produce]
    rng = np.random.default_rng()
    temp = rng.normal((lo + hi) / 2, 0.55)
    humidity = rng.normal((dry + wet) / 2, 1.5)
    if scenario == "Door opened":
        temp = hi + rng.uniform(0.5, 2.5)
    elif scenario == "Cooling failure":
        temp = hi + rng.uniform(4, 8)
    return {"Time": stamp, "Temperature (°C)": round(temp, 1),
            "Humidity (%)": round(humidity, 1)}


def history(produce):
    now = datetime.now().replace(microsecond=0)
    return [reading(produce, now - timedelta(minutes=i)) for i in reversed(range(24))]


def status(produce, temp, humidity):
    lo, hi, dry, wet, _ = PROFILES[produce]
    t = max(lo - temp, temp - hi, 0)
    h = max(dry - humidity, humidity - wet, 0)
    if t >= 3 or h >= 10:
        return "Critical"
    return "Warning" if t or h else "Safe"
