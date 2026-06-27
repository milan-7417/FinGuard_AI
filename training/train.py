import os
import json
import joblib
import numpy as np

from pathlib import Path

import tensorflow as tf

from sklearn.utils.class_weight import compute_class_weight

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import (
    Input,
    Conv1D,
    BatchNormalization,
    MaxPooling1D,
    Bidirectional,
    LSTM,
    Dense,
    Dropout
)

from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint,
    CSVLogger
)

from app.services.preprocess import prepare_data

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_DIR = BASE_DIR / "app" / "model"

ARTIFACT_DIR = BASE_DIR / "training" / "artifacts"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# Load Dataset
# =====================================================

print("=" * 60)
print("Preparing Dataset...")
print("=" * 60)

(
    X_train,
    X_val,
    X_test,
    y_train,
    y_val,
    y_test
) = prepare_data()

print("\nDataset Loaded Successfully!")

print("\nTraining Shape :", X_train.shape)
print("Validation Shape :", X_val.shape)
print("Testing Shape :", X_test.shape)

# =====================================================
# Compute Class Weights
# =====================================================

class_weights = compute_class_weight(

    class_weight="balanced",

    classes=np.unique(y_train),

    y=y_train

)

class_weights = {

    int(i): float(weight)

    for i, weight in enumerate(class_weights)

}

print("\nClass Weights")

print(class_weights)

# =====================================================
# Build CNN + BiLSTM Model
# =====================================================

print("\n")
print("=" * 60)
print("Building CNN + BiLSTM Model...")
print("=" * 60)

model = Sequential(

    [

        # =================================================
        # Input Layer
        # =================================================

        Input(shape=(X_train.shape[1], 1)),

        # =================================================
        # CNN Block - 1
        # =================================================

        Conv1D(
            filters=64,
            kernel_size=3,
            padding="same",
            activation="relu"
        ),

        BatchNormalization(),

        MaxPooling1D(pool_size=2),

        Dropout(0.25),

        # =================================================
        # CNN Block - 2
        # =================================================

        Conv1D(
            filters=128,
            kernel_size=3,
            padding="same",
            activation="relu"
        ),

        BatchNormalization(),

        MaxPooling1D(pool_size=1),

        Dropout(0.30),

        # =================================================
        # BiLSTM
        # =================================================

        Bidirectional(

            LSTM(

                64,

                return_sequences=False

            )

        ),

        # =================================================
        # Dense Block
        # =================================================

        Dense(
            64,
            activation="relu"
        ),

        Dropout(0.30),

        Dense(
            32,
            activation="relu"
        ),

        Dense(
            1,
            activation="sigmoid"
        )

    ],

    name="CNN_BiLSTM_Fraud_Detector"

)

# =====================================================
# Compile Model
# =====================================================

print("\nCompiling Model...")

model.compile(

    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),

    loss="binary_crossentropy",

    metrics=[

        "accuracy",

        tf.keras.metrics.Precision(
            name="precision"
        ),

        tf.keras.metrics.Recall(
            name="recall"
        ),

        tf.keras.metrics.AUC(
            name="auc"
        )

    ]

)

# =====================================================
# Model Summary
# =====================================================

print("\n")
print("=" * 60)
print("Model Summary")
print("=" * 60)

model.summary()

# =====================================================
# Callbacks
# =====================================================

early_stop = EarlyStopping(

    monitor="val_loss",

    patience=5,

    restore_best_weights=True,

    verbose=1

)

reduce_lr = ReduceLROnPlateau(

    monitor="val_loss",

    factor=0.5,

    patience=3,

    min_lr=1e-6,

    verbose=1

)

checkpoint = ModelCheckpoint(

    filepath=MODEL_DIR / "cnn_bilstm.keras",

    monitor="val_loss",

    save_best_only=True,

    verbose=1

)

csv_logger = CSVLogger(

    MODEL_DIR / "training_history.csv"

)

# =====================================================
# Train Model
# =====================================================

print("\n")
print("=" * 60)
print("Training Started...")
print("=" * 60)

history = model.fit(

    X_train,

    y_train,

    validation_data=(

        X_val,

        y_val

    ),

    epochs=30,

    batch_size=256,

    class_weight=class_weights,

    callbacks=[

        early_stop,

        reduce_lr,

        checkpoint,

        csv_logger

    ],

    verbose=1

)

# =====================================================
# Load Best Model
# =====================================================

print("\nLoading Best Model...\n")

model = tf.keras.models.load_model(
    MODEL_DIR / "cnn_bilstm.keras"
)

# =====================================================
# Evaluate Model
# =====================================================

results = model.evaluate(

    X_test,

    y_test,

    verbose=1

)

# =====================================================
# Save Test Dataset
# =====================================================

np.save(

    ARTIFACT_DIR / "X_test.npy",

    X_test

)

np.save(

    ARTIFACT_DIR / "y_test.npy",

    y_test

)

print("Test dataset saved.")

# =====================================================
# Save Training History
# =====================================================

joblib.dump(

    history.history,

    ARTIFACT_DIR / "history.pkl"

)

print("Training history saved.")

# =====================================================
# Save Model Information
# =====================================================

model_info = {

    "model_name": "CNN + BiLSTM",

    "epochs": len(history.history["loss"]),

    "batch_size": 256,

    "optimizer": "Adam",

    "learning_rate": 0.001,

    "input_shape": list(X_train.shape),

    "loss": float(results[0]),

    "accuracy": float(results[1]),

    "precision": float(results[2]),

    "recall": float(results[3]),

    "auc": float(results[4])

}

with open(

    ARTIFACT_DIR / "model_info.json",

    "w"

) as file:

    json.dump(

        model_info,

        file,

        indent=4

    )

print("Model information saved.")

# =====================================================
# Test Metrics
# =====================================================

print("\n")

print("=" * 60)

print("Final Test Performance")

print("=" * 60)

print(f"Loss       : {results[0]:.4f}")

print(f"Accuracy   : {results[1]:.4f}")

print(f"Precision  : {results[2]:.4f}")

print(f"Recall     : {results[3]:.4f}")

print(f"AUC        : {results[4]:.4f}")

print("=" * 60)
