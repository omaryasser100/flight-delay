import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from backend.feature_engineering import FeatureEngineering
from backend.data_loader_cleaner import DataLoaderCleaner


class ClassifierPipeline:
    def __init__(self, thresholds_path="models/best_thresholds.json", default_strategy="Best Overall (Penalty Class 2 False Positives)"):
        """
        Initialize the pipeline with pre-trained model, encoder, scaler, and thresholds.
        """
        base_path = os.path.dirname(__file__)
        models_dir = os.path.join(base_path, "..", "models")

        # Load encoder and scaler
        self.encoder = joblib.load(os.path.join(models_dir, "encoder_classifier.pkl"))
        self.scaler = joblib.load(os.path.join(models_dir, "scaler_classifier.pkl"))

        # Load XGBoost model
        self.model = joblib.load(os.path.join(models_dir, "model_classifier.pkl"))
        booster = self.model.get_booster()

        # Load expected features
        if booster.feature_names is None or len(booster.feature_names) == 0:
            features_path = os.path.join(models_dir, "feature_names_classifier.json")
            with open(features_path, "r") as f:
                self.expected_features = json.load(f)
        else:
            self.expected_features = booster.feature_names

        # Load classification thresholds
        thresholds_full_path = os.path.join(base_path, "..", thresholds_path)
        with open(thresholds_full_path, "r") as f:
            thresholds_raw = json.load(f)
        self.thresholds_dict = {k: np.array(v) for k, v in thresholds_raw.items()}

        # Default strategy check
        if default_strategy not in self.thresholds_dict:
            raise ValueError(f"Threshold strategy '{default_strategy}' not found.")
        self.threshold_strategy = default_strategy

    def set_threshold_strategy(self, strategy_name):
        """
        Set a custom threshold strategy (for class probability weighting).
        """
        if strategy_name not in self.thresholds_dict:
            raise ValueError(f"Strategy '{strategy_name}' not found.")
        self.threshold_strategy = strategy_name

    def preprocess(self, df):
        """
        Clean, encode, and scale features. Aligns with training-time feature order.
        """
        df = df.copy()

        # Drop unnecessary or leakage columns
        drop_cols = [
            'carrier_name', 'airport_name', 'arr_flights', 'arr_del15',
            'carrier_ct', 'weather_ct', 'nas_ct', 'security_ct', 'late_aircraft_ct',
            'arr_cancelled', 'arr_diverted', 'arr_delay', 'carrier_delay',
            'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay',
            'total_delay', 'delay_ratio', 'high_delay_flag', 'delay_risk_level',
            'year_month', 'season_airport_combo'
        ]
        df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True, errors='ignore')

        # Ensure categories are string
        for col in df.columns:
            if df[col].dtype.name == "category":
                df[col] = df[col].astype(str)

        # Split columns by encoding and scaling
        cat_cols = [col for col in self.encoder.feature_names_in_ if col in df.columns]
        num_cols = [col for col in self.scaler.feature_names_in_ if col in df.columns]

        encoded = self.encoder.transform(df[cat_cols]) if cat_cols else np.zeros((len(df), 0))
        scaled = self.scaler.transform(df[num_cols]) if num_cols else np.zeros((len(df), 0))

        df_cat = pd.DataFrame(encoded, columns=self.encoder.get_feature_names_out(cat_cols), index=df.index)
        df_num = pd.DataFrame(scaled, columns=num_cols, index=df.index)

        final_df = pd.concat([df_num, df_cat], axis=1)
        aligned_df = final_df.reindex(columns=self.expected_features, fill_value=0)

        return aligned_df

    def predict_proba(self, X):
        """
        Return class probabilities from the model.
        """
        return self.model.predict_proba(X)

    def predict(self, X):
        """
        Apply custom threshold weighting and return class predictions.
        """
        probs = self.predict_proba(X)
        weights = self.thresholds_dict[self.threshold_strategy]
        scaled = probs * (weights / weights.sum())
        return np.argmax(scaled, axis=1)

    def run_pipeline(self, df: pd.DataFrame, mode: str = "test"):
        """
        Runs full pipeline on user-provided DataFrame:
        - Cleans and feature engineers
        - Preprocesses and aligns columns
        - Predicts using trained model

        Modes:
        - 'test'     → requires target column and returns evaluation
        - 'realtime' → no targets, returns predictions only
        """
        cleaner = DataLoaderCleaner()
        clean_df = cleaner.clean_data(df)
        engineered_df = FeatureEngineering().transform(clean_df)

        if mode == "test":
            # Expect the uploaded dataset to contain the target column
            X, y_true = cleaner.split_features_and_target(engineered_df)
            X_proc = self.preprocess(X)
            y_pred = self.predict(X_proc)

            report = classification_report(y_true, y_pred, digits=4, labels=[0, 1, 2], zero_division=0)

            return {
                "X_input": X_proc,
                "y_true": y_true,
                "y_pred": y_pred,
                "report": report
            }

        elif mode == "realtime":
            X_input, _ = cleaner.split_features_and_target(engineered_df)
            X_proc = self.preprocess(X_input)
            y_pred = self.predict(X_proc)
            return {
                "X_input": X_proc,
                "y_pred": y_pred
            }

        else:
            raise ValueError("Mode must be 'test' or 'realtime'")
