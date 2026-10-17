import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


NUMERIC_FEATURES = [
    "scheduled_shipping_days",
    "item_count",
    "total_quantity",
    "total_sales",
    "distinct_categories",
    "distinct_departments",
    "order_year",
    "order_month",
    "order_day_of_week",
]

CATEGORICAL_FEATURES = [
    "shipping_mode",
    "payment_type",
    "market",
    "order_region",
    "customer_segment",
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

TARGET = "late_delivery_risk"

MODEL_THRESHOLD = 0.40


def create_model():
    """
    Create the Random Forest prediction pipeline.
    """

    preprocessor = ColumnTransformer([
        (
            "numeric",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
            ]),
            NUMERIC_FEATURES,
        ),
        (
            "categorical",
            Pipeline([
                (
                    "imputer",
                    SimpleImputer(strategy="most_frequent")
                ),
                (
                    "onehot",
                    OneHotEncoder(
                        handle_unknown="ignore"
                    )
                ),
            ]),
            CATEGORICAL_FEATURES,
        ),
    ])

    model = Pipeline([
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=200,
                max_depth=12,
                min_samples_leaf=5,
                random_state=42,
                n_jobs=-1
            )
        ),
    ])

    return model


def prepare_features(data):
    """
    Prepare input data for prediction.
    """

    data = data.copy()

    if "order_date" in data.columns:

        order_date = pd.to_datetime(
            data["order_date"]
        )

        data["order_year"] = order_date.dt.year
        data["order_month"] = order_date.dt.month
        data["order_day_of_week"] = (
            order_date.dt.dayofweek
        )

    return data[FEATURES]


def train_model(training_data):
    """
    Train the prediction model using historical
    order-level data.
    """

    training_data = training_data.copy()

    X = prepare_features(training_data)
    y = training_data[TARGET]

    model = create_model()

    model.fit(X, y)

    return model


def predict_delay_risk(model, order_data):
    """
    Predict late-delivery risk for one or more orders.

    Returns:
        DataFrame containing:
        - predicted_risk
        - predicted_probability
    """

    X = prepare_features(order_data)

    probabilities = model.predict_proba(X)[:, 1]

    predictions = (
        probabilities >= MODEL_THRESHOLD
    ).astype(int)

    return pd.DataFrame({
        "predicted_risk": predictions,
        "predicted_probability": probabilities,
    })