from functools import lru_cache
import numpy as np
from sklearn.linear_model import LinearRegression
from utils.common import PROFILES


def features(produce, temp, humidity, hours):
    lo, hi, dry, wet, life = PROFILES[produce]
    # Stress and time are normalized to one synthetic batch lifetime.
    heat = np.maximum(np.maximum(temp - hi, lo - temp), 0)
    damp = np.maximum(np.maximum(humidity - wet, dry - humidity), 0)
    age = hours / life
    return np.column_stack((age, age * heat, age * damp))


@lru_cache(maxsize=1)
def train():
    rng = np.random.default_rng(15)
    samples, targets = [], []
    for produce in PROFILES:
        x = features(produce, rng.uniform(-5, 40, 1200), rng.uniform(20, 100, 1200),
                     rng.uniform(0, 240, 1200))
        # Synthetic deterioration targets with small measurement noise.
        y = x @ [1.0, 0.14, 0.025] + rng.normal(0, 0.015, len(x))
        samples.append(x)
        targets.append(y)
    return LinearRegression(fit_intercept=False, positive=True).fit(
        np.vstack(samples), np.concatenate(targets))


def predict(produce, temp, humidity, hours):
    rate = train().predict(features(produce, temp, humidity, 1))[0]
    fraction = rate * hours
    return float(np.clip(100 * fraction, 0, 100)), max(0.0, 1 / rate - hours)
