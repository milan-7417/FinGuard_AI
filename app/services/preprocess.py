import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler
)

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

MODEL_DIR = BASE_DIR / "app" / "model"

MODEL_DIR.mkdir(exist_ok=True)

# =====================================================
# Load Original Dataset
# =====================================================

def load_data():

    print("Loading PaySim Dataset...")

    file_path = DATA_DIR / "PS_20174392719_1491204439457_log.csv"

    df = pd.read_csv(file_path)

    print(f"Dataset Shape : {df.shape}")

    return df

# =====================================================
# Feature Engineering
# =====================================================

def feature_engineering(df):

    print("Performing Feature Engineering...")

    # -----------------------------
    # Drop unnecessary columns
    # -----------------------------

    df = df.drop(

        columns=[
            "nameOrig",
            "nameDest",
            "isFlaggedFraud"
        ],

        errors="ignore"

    )

    # -----------------------------
    # Create new features
    # -----------------------------

    df["originBalanceDiff"] = (

        df["oldbalanceOrg"]

        -

        df["newbalanceOrig"]

    )

    df["destBalanceDiff"] = (

        df["newbalanceDest"]

        -

        df["oldbalanceDest"]

    )

    df["balanceChanged"] = (

        df["originBalanceDiff"] != 0

    ).astype(int)

    threshold = df["amount"].quantile(0.95)

    df["largeTransaction"] = (

        df["amount"] > threshold

    ).astype(int)

    joblib.dump(
        threshold,
        MODEL_DIR / "amount_threshold.pkl"
    )

    print(f"Amount Threshold Saved: {threshold:.2f}")

    print("Feature Engineering Completed.")

    return df

# =====================================================
# Label Encoding
# =====================================================

def encode_features(df):

    print("Encoding Categorical Features...")

    encoder = LabelEncoder()

    df["type"] = encoder.fit_transform(

        df["type"]

    )

    joblib.dump(

        encoder,

        MODEL_DIR / "encoder.pkl"

    )

    print("Encoder Saved.")

    return df

# =====================================================
# Create Balanced Dataset
# =====================================================

def create_balanced_dataset(df, sample_size=100000):

    balanced_file = DATA_DIR / "paysim_balanced.parquet"

    if balanced_file.exists():

        print("Loading Existing Balanced Dataset...")

        return pd.read_parquet(balanced_file)

    print("Creating Balanced Dataset...")

    fraud_df = df[df["isFraud"] == 1]

    genuine_df = df[df["isFraud"] == 0]

    sample_size = min(sample_size, len(genuine_df))

    genuine_sample = genuine_df.sample(
        n=sample_size,
        random_state=42
    )

    balanced_df = pd.concat(
        [fraud_df, genuine_sample],
        ignore_index=True
    )

    balanced_df = balanced_df.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    balanced_df.to_parquet(
        balanced_file,
        index=False
    )

    print("Balanced Dataset Saved.")

    return balanced_df

# =====================================================
# Split Dataset
# =====================================================

def split_data(df):

    X = df.drop(columns=["isFraud"])

    y = df["isFraud"]

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.20,

        random_state=42,

        stratify=y

    )

    X_train, X_val, y_train, y_val = train_test_split(

        X_train,
        y_train,

        test_size=0.20,

        random_state=42,

        stratify=y_train

    )

    return X_train, X_val, X_test, y_train, y_val, y_test

# =====================================================
# Feature Scaling
# =====================================================
def scale_data(X_train, X_val, X_test):

    scaler = StandardScaler()

    numeric_columns = [
        "step",
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
        "originBalanceDiff",
        "destBalanceDiff"
    ]

    # Create copies
    X_train = X_train.copy()
    X_val = X_val.copy()
    X_test = X_test.copy()

    # Scale
    X_train[numeric_columns] = scaler.fit_transform(
        X_train[numeric_columns].astype("float32")
    )

    X_val[numeric_columns] = scaler.transform(
        X_val[numeric_columns].astype("float32")
    )

    X_test[numeric_columns] = scaler.transform(
        X_test[numeric_columns].astype("float32")
    )

    joblib.dump(
        scaler,
        MODEL_DIR / "scaler.pkl"
    )

    print("Scaler Saved.")

    return X_train, X_val, X_test

# =====================================================
# Reshape Data
# =====================================================

def reshape_data(X_train, X_val, X_test):

    X_train = X_train.to_numpy(dtype=np.float32)

    X_val = X_val.to_numpy(dtype=np.float32)

    X_test = X_test.to_numpy(dtype=np.float32)

    X_train = X_train.reshape(
        X_train.shape[0],
        X_train.shape[1],
        1
    )

    X_val = X_val.reshape(
        X_val.shape[0],
        X_val.shape[1],
        1
    )

    X_test = X_test.reshape(
        X_test.shape[0],
        X_test.shape[1],
        1
    )

    return X_train, X_val, X_test

# =====================================================
# Complete Preprocessing Pipeline
# =====================================================

def prepare_data():

    balanced_file = DATA_DIR / "paysim_balanced.parquet"

    # -------------------------------------------------
    # Load balanced dataset if available
    # -------------------------------------------------

    if balanced_file.exists():

        print("Loading Balanced Dataset...")

        balanced_df = pd.read_parquet(
            balanced_file
        )

    else:

        print("Balanced dataset not found.")

        print("Starting preprocessing pipeline...\n")

        # Load original dataset
        df = load_data()

        # Feature Engineering
        df = feature_engineering(df)

        # Encode categorical features
        df = encode_features(df)

        # Create balanced dataset
        balanced_df = create_balanced_dataset(df)

        print("Balanced dataset created successfully.\n")

    # -------------------------------------------------
    # Split Dataset
    # -------------------------------------------------

    print("Splitting dataset...")

    X_train, X_val, X_test, y_train, y_val, y_test = split_data(
        balanced_df
    )

    # -------------------------------------------------
    # Scale Features
    # -------------------------------------------------

    print("Scaling features...")

    X_train, X_val, X_test = scale_data(
        X_train,
        X_val,
        X_test
    )

    # -------------------------------------------------
    # Reshape
    # -------------------------------------------------

    print("Reshaping dataset...")

    X_train, X_val, X_test = reshape_data(
        X_train,
        X_val,
        X_test
    )

    # -------------------------------------------------
    # Convert dtype
    # -------------------------------------------------

    X_train = X_train.astype(np.float32)
    X_val = X_val.astype(np.float32)
    X_test = X_test.astype(np.float32)

    y_train = y_train.to_numpy(dtype=np.float32)
    y_val = y_val.to_numpy(dtype=np.float32)
    y_test = y_test.to_numpy(dtype=np.float32)

    print("\nPreprocessing Completed Successfully!")

    return (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test
    )

# =====================================================
# Test Pipeline
# =====================================================

if __name__ == "__main__":

    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test
    ) = prepare_data()

    print("=" * 50)

    print("Training Shape :", X_train.shape)

    print("Validation Shape :", X_val.shape)

    print("Testing Shape :", X_test.shape)

    print("=" * 50)

    print("Training dtype :", X_train.dtype)

    print("Target dtype :", y_train.dtype)

    print("=" * 50)