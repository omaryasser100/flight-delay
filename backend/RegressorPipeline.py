import os
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from backend.feature_engineering import FeatureEngineering
from backend.data_loader_cleaner import DataLoaderCleaner


class RegressorPipeline:
    def __init__(self):
        """
        Initialize the RegressorPipeline:
        - Loads pre-trained XGBoost regressor
        - Loads associated OneHotEncoder and StandardScaler
        - Extracts expected feature names from model or builds fallback
        """
        base_path = os.path.dirname(__file__)
        models_dir = os.path.join(base_path, "..", "models")

        self.encoder = joblib.load(os.path.join(models_dir, "encoder_regressor.pkl"))
        self.scaler = joblib.load(os.path.join(models_dir, "scaler_regressor.pkl"))
        self.model = joblib.load(os.path.join(models_dir, "model_regressor.pkl"))

        # Extract feature names used at training time
        booster = self.model.get_booster()
        if booster.feature_names is None or len(booster.feature_names) == 0:
            # Fallback to manually reconstruct expected feature list
            num_cols = list(self.scaler.feature_names_in_)
            cat_cols = list(self.encoder.get_feature_names_out())
            self.expected_features = num_cols + cat_cols
        else:
            self.expected_features = booster.feature_names


    def preprocess(self, df):
        """
        Apply preprocessing steps:
        - Drop irrelevant or leakage-prone columns
        - Encode categorical variables
        - Scale numeric values
        - Align feature set with training-time format
        """
        df = df.copy()

        # Drop target and leakage columns
        drop_cols = [
            'carrier_name', 'airport_name', 'arr_flights', 'arr_del15',
            'carrier_ct', 'weather_ct', 'nas_ct', 'security_ct', 'late_aircraft_ct',
            'arr_cancelled', 'arr_diverted', 'carrier_delay', 'weather_delay',
            'nas_delay', 'security_delay', 'late_aircraft_delay', 'total_delay',
            'delay_ratio', 'high_delay_flag', 'delay_risk_level', 'year_month', 'season_airport_combo'
        ]
        df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True, errors='ignore')

        # Convert categorical types to strings for encoder compatibility
        for col in df.columns:
            if df[col].dtype.name == "category":
                df[col] = df[col].astype(str)

        # Extract matching columns only
        cat_cols = [col for col in self.encoder.feature_names_in_ if col in df.columns]
        num_cols = [col for col in self.scaler.feature_names_in_ if col in df.columns]

        # Encode and scale
        encoded = self.encoder.transform(df[cat_cols]) if cat_cols else np.zeros((len(df), 0))
        scaled = self.scaler.transform(df[num_cols]) if num_cols else np.zeros((len(df), 0))

        # Rebuild as aligned DataFrame
        df_cat = pd.DataFrame(encoded, columns=self.encoder.get_feature_names_out(cat_cols), index=df.index)
        df_num = pd.DataFrame(scaled, columns=num_cols, index=df.index)

        # Combine numeric and categorical
        final_df = pd.concat([df_num, df_cat], axis=1)

        # Ensure order and completeness of features
        aligned_df = final_df.reindex(columns=self.expected_features, fill_value=0)

        return aligned_df


    def predict(self, X):
        """Run inference on aligned features and return delay predictions (in minutes)."""
        return self.model.predict(X)


    def run_pipeline(self, df: pd.DataFrame, mode: str = "test"):
        """
        Run the full pipeline:
        - Cleans and transforms input
        - Applies preprocessing
        - Runs prediction
        - Evaluates performance (only in test mode)

        Parameters:
        - df (DataFrame): user input dataset
        - mode (str): 'test' or 'realtime'

        Returns:
        - Dict with predictions, and optionally evaluation metrics (if mode='test')
        """
        cleaner = DataLoaderCleaner()
        clean_df = cleaner.clean_data(df)
        engineered_df = FeatureEngineering().transform(clean_df)

        if mode == "test":
            X, y_true = cleaner.split_features_and_target(engineered_df, target_col="arr_delay")
            X_proc = self.preprocess(X)
            y_pred = self.predict(X_proc)

            # Calculate evaluation metrics
            mae = mean_absolute_error(y_true, y_pred)
            mse = mean_squared_error(y_true, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_true, y_pred)

            return {
                "X_input": X_proc,
                "y_true": y_true,
                "y_pred": y_pred,
                "mae": mae,
                "mse": mse,
                "rmse": rmse,
                "r2": r2
            }

        elif mode == "realtime":
            X_input, _ = cleaner.split_features_and_target(engineered_df, target_col="arr_delay")
            X_proc = self.preprocess(X_input)
            y_pred = self.predict(X_proc)

            return {
                "X_input": X_proc,
                "y_pred": y_pred
            }

        else:
            raise ValueError("Mode must be 'test' or 'realtime'")
