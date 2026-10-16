import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.prediction import train_model, predict_delay_risk


DATA_PATH = "data/processed/supplyprescript_order_model_data.csv"


def main():
    data = pd.read_csv(DATA_PATH)

    print("Dataset shape:", data.shape)

    # Use a small real sample only for module testing.
    sample = data.head(10).copy()

    training_data = data.iloc[:-10].copy()

    model = train_model(training_data)

    predictions = predict_delay_risk(model, sample)

    output = pd.concat(
        [
            sample[
                ["Order Id", "order_date", "late_delivery_risk"]
            ].reset_index(drop=True),
            predictions.reset_index(drop=True),
        ],
        axis=1,
    )

    print("\nPrediction module test output:")
    print(output.to_string(index=False))

    print("\nPrediction columns:")
    print(list(predictions.columns))

    print("\nModule test completed successfully.")


if __name__ == "__main__":
    main()