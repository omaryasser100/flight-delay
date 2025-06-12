import pandas as pd
import numpy as np

class FeatureEngineering:
    @staticmethod
    def get_season(month: int) -> str:
        """Map month to season."""
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'

    def transform(self, df: pd.DataFrame, fillna: bool = True) -> pd.DataFrame:
        """
        Feature engineering pipeline for flight delay data.
        - Generates delay-related ratios
        - Adds seasonal and airport-level features
        - Avoids groupby.apply-related issues
        - Keeps dtype consistency for modeling
        """
        df = df.copy()

        # ➤ Handle arr_flights = 0 to prevent division errors
        df['arr_flights'] = df['arr_flights'].replace(0, np.nan)

        # ➤ Delay ratios and rates
        df['delay_ratio'] = df['arr_del15'] / df['arr_flights']
        df['cancellation_rate'] = df['arr_cancelled'] / df['arr_flights']
        df['diversion_rate'] = df['arr_diverted'] / df['arr_flights']
        df['disrupted'] = ((df['arr_del15'] > 0) | (df['arr_cancelled'] > 0)).astype(int)


        # ➤ Total delay and individual delay percentages
        delay_cols = ['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay']
        df['total_delay'] = df[delay_cols].sum(axis=1).replace(0, np.nan)

        for col in delay_cols:
            new_col = col.replace('_delay', '_delay_pct')
            df[new_col] = df[col] / df['total_delay']

        if fillna:
            pct_cols = [col.replace('_delay', '_delay_pct') for col in delay_cols]
            df[pct_cols] = df[pct_cols].fillna(0)

        # ➤ Time-based features
        df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
        df['season'] = df['month'].apply(self.get_season)

        # ➤ Group-level aggregated features
        # carrier_total_flights: must pre-fill NaNs to avoid errors
        df['carrier_total_flights'] = df.groupby('carrier', observed=False)['arr_flights'].transform('sum')

        airport_delay_sum = df.groupby('airport', observed=False)['arr_del15'].transform('sum')
        airport_flights_sum = df.groupby('airport', observed=False)['arr_flights'].transform('sum')
        df['airport_delay_rate'] = airport_delay_sum / airport_flights_sum

        # ➤ Label: delay_risk_level
        def classify_risk(ratio):
            if pd.isna(ratio):
                return np.nan
            elif ratio <= 0.20:
                return 0
            elif ratio <= 0.40:
                return 1
            else:
                return 2
        df['delay_risk_level'] = df['delay_ratio'].apply(classify_risk)

        # ➤ Additional features
        df['mean_delay_per_flight'] = df['total_delay'] / df['arr_flights']
        df['mean_delay_per_flight'] = df['mean_delay_per_flight'].fillna(0)

        df['dominant_delay_cause'] = df[delay_cols].idxmax(axis=1)

        # Monthly delay patterns
        month_delay_sum = df.groupby('month', observed=False)['arr_del15'].transform('sum')
        month_flights_sum = df.groupby('month', observed=False)['arr_flights'].transform('sum')
        df['month_delay_rate'] = month_delay_sum / month_flights_sum

        # Carrier vs airport pressure
        df['carrier_vs_airport_ratio'] = df['carrier_delay_pct'] / (
            df['weather_delay_pct'] + df['nas_delay_pct'] + 1e-6
        )

        # Combo feature: season + airport
        df['season_airport_combo'] = df['season'].astype(str) + '_' + df['airport'].astype(str)
        combo_del15 = df.groupby('season_airport_combo', observed=False)['arr_del15'].transform('sum')
        combo_flights = df.groupby('season_airport_combo', observed=False)['arr_flights'].transform('sum')
        df['season_airport_delay_rate'] = combo_del15 / combo_flights

        # Fill remaining NaNs in numerical columns
        if fillna:
            num_cols = df.select_dtypes(include=[np.number]).columns
            df[num_cols] = df[num_cols].fillna(0)

        return df
