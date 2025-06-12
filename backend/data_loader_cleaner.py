import pandas as pd

class DataLoaderCleaner:
    def __init__(self):
        self.raw_df = None
        self.clean_df = None
        self.categorical_backup = None

    def load_data(self, file_path):
        """Load the CSV file and store raw DataFrame."""
        self.raw_df = pd.read_csv(file_path)
        return self.raw_df

    def clean_data(self, df):
        """Clean the raw DataFrame and return cleaned version."""
        df = df.copy()

        # Drop missing values
        df.dropna(inplace=True)

        # Convert to appropriate dtypes
        cat_cols = ['carrier', 'carrier_name', 'airport', 'airport_name']
        for col in cat_cols:
            if col in df.columns:
                df[col] = df[col].astype('category')

        # Backup categorical columns
        self.categorical_backup = df[cat_cols].copy()

        # Convert specific numeric columns
        df['arr_flights'] = df['arr_flights'].astype(int)
        df['arr_del15'] = df['arr_del15'].astype(int)

        self.clean_df = df
        return df

    def summarize_missing(self, df):
        """Return summary of missing values per column."""
        missing = df.isna().sum()
        return missing[missing > 0].sort_values(ascending=False)

    def summarize_duplicates(self, df):
        """Return number of duplicate rows."""
        return df.duplicated().sum()

    def summarize_overview(self, df):
        summary = {
            'shape': df.shape,
            'rows': df.shape[0],
            'columns': df.shape[1],
            'dtypes': df.dtypes,
            'describe': df.describe(),
            'head': df.head()
        }

        if 'year' in df.columns:
            years = pd.to_numeric(df['year'], errors='coerce')
            years = years.dropna()
            if not years.empty:
                summary['year_range'] = (int(years.min()), int(years.max()))
                summary['time_span'] = int(years.max() - years.min())
            else:
                summary['year_range'] = None
                summary['time_span'] = None
        else:
            summary['year_range'] = None
            summary['time_span'] = None

        return summary



    def compare_raw_clean(self):
        """Return basic comparison between raw and cleaned DataFrames."""
        if self.raw_df is None or self.clean_df is None:
            return None

        return {
            'raw_shape': self.raw_df.shape,
            'clean_shape': self.clean_df.shape,
            'missing_before': self.raw_df.isna().sum().sum(),
            'missing_after': self.clean_df.isna().sum().sum(),
            'dropped_rows': self.raw_df.shape[0] - self.clean_df.shape[0],
        }

    def get_categorical_backup(self):
        """Return the backup of categorical columns."""
        return self.categorical_backup


    def split_features_and_target(self, df, target_col="delay_risk_level"):
        """
        Splits DataFrame into features and target label.

        Parameters:
        - df: DataFrame to split
        - target_col: name of the target column (default is 'delay_risk_level')

        Returns:
        - X: DataFrame without target column
        - y: Series of target labels (if present), else None
        """
        if target_col in df.columns:
            y = df[target_col]
            X = df.drop(columns=[target_col])
            return X, y
        else:
            return df, None

