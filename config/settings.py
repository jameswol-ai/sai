import os

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "models/trading_model.pkl"
)

DEFAULT_RISK = float(
    os.getenv(
        "DEFAULT_RISK",
        0.02
    )
)