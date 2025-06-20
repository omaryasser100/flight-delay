import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import seaborn as sns
import matplotlib.pyplot as plt


class UnivariateAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # 📊 Histogram for continuous features
    def plot_yearly_arrivals(self):
        df = self.df.copy()
        df['year'] = pd.to_datetime(df['year_month']).dt.year
        df_grouped = df.groupby('year')['arr_flights'].sum().reset_index()

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.lineplot(data=df_grouped, x='year', y='arr_flights', marker="o", ax=ax)
        ax.set_title("Yearly Flight Arrivals")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Flights")
        ax.grid(True, linestyle="--", alpha=0.5)
        fig.tight_layout()
        return fig




    # 📦 Boxplot for numeric outlier detection
    def plot_boxplot(self, col: str):
        fig, ax = plt.subplots(figsize=(4, 4))
        sns.boxplot(y=self.df[col], ax=ax, color='coral')
        ax.set_title(f"Boxplot of {col}")
        fig.tight_layout()
        return fig

    # 📊 Countplot for categorical values
    def plot_bar_count(self, col: str, top_n: int = None):
        counts = self.df[col].value_counts()
        if top_n:
            counts = counts.head(top_n)
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(x=counts.index, y=counts.values, ax=ax, palette="pastel")
        ax.set_title(f"Frequency of {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        ax.bar_label(ax.containers[0])
        plt.xticks(rotation=45)
        fig.tight_layout()
        return fig

    # 🥧 Pie chart for proportions
    def plot_pie(self, col: str, top_n: int = 10):
        counts = self.df[col].value_counts()
        top_counts = counts.head(top_n)
        other_total = counts[top_n:].sum()

        combined = top_counts.copy()
        combined["Other"] = other_total

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(combined.values, labels=combined.index, autopct='%1.1f%%', startangle=90)
        ax.set_title(f"Proportion of {col}")
        ax.axis('equal')
        return fig



import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class FlightDataAnalysis:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.delay_cols = ['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay']

    def summary_statistics(self):
        return self.df.describe()

    def missing_values_report(self):
        missing = self.df.isnull().sum()
        percent = 100 * missing / len(self.df)
        return pd.DataFrame({'missing_count': missing, 'missing_percent': percent}).query('missing_count > 0')

    def correlation_matrix(self):
        corr = self.df.select_dtypes(include='number').corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt=".2f", ax=ax)
        ax.set_title('Correlation Matrix Heatmap')
        return fig

    # 2. Time Trends
    def plot_flights_vs_delays_yearly(self):
        df = self.df.copy()
        df['year'] = pd.to_datetime(df['year_month']).dt.year
        yearly = df.groupby('year')[['arr_flights', 'arr_del15']].sum().reset_index()

        fig, ax = plt.subplots(figsize=(10, 4))
        yearly.plot(x='year', y=['arr_flights', 'arr_del15'], ax=ax, marker='o')
        ax.set_title("Yearly Trends: Total Flights vs Delayed Flights (15+ mins)")
        ax.set_xlabel("Year")
        ax.set_ylabel("Flights")
        fig.tight_layout()
        return fig


    def plot_delay_ratio_yearly(self):
        df = self.df.copy()
        df['year'] = pd.to_datetime(df['year_month']).dt.year
        df_grouped = df.groupby('year').agg({
            'arr_del15': 'sum',
            'arr_flights': 'sum'
        }).reset_index()
        df_grouped['delay_ratio'] = df_grouped['arr_del15'] / df_grouped['arr_flights']

        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=df_grouped, x='year', y='delay_ratio', marker="o", ax=ax)
        ax.set_title("Yearly Delay Ratio")
        ax.set_ylabel("Delay Ratio")
        ax.set_xlabel("Year")
        fig.tight_layout()
        return fig


    def plot_cancellation_rate_yearly(self):
        df = self.df.copy()
        df['year'] = pd.to_datetime(df['year_month']).dt.year
        yearly = df.groupby('year')[['arr_cancelled', 'arr_flights']].sum().reset_index()
        yearly['cancellation_rate'] = yearly['arr_cancelled'] / yearly['arr_flights']

        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=yearly, x='year', y='cancellation_rate', marker="o", ax=ax)
        ax.set_title("Yearly Cancellation Rate")
        fig.tight_layout()
        return fig


    def plot_diversion_rate_yearly(self):
        df = self.df.copy()
        df['year'] = pd.to_datetime(df['year_month']).dt.year
        yearly = df.groupby('year')[['arr_diverted', 'arr_flights']].sum().reset_index()
        yearly['diversion_rate'] = yearly['arr_diverted'] / yearly['arr_flights']

        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=yearly, x='year', y='diversion_rate', marker="o", ax=ax)
        ax.set_title("Yearly Diversion Rate")
        fig.tight_layout()
        return fig


    # 3. Delay Cause Breakdown
    def plot_delay_causes_proportion_peak(self):
        import matplotlib.patches as mpatches

        peak = self.df[self.df['month'].isin([6, 7, 8, 12])]
        cause_sum = peak[self.delay_cols].sum().sort_values(ascending=True)

        fig, ax = plt.subplots(figsize=(7, 6))

        # Use custom colors for clarity (optional)
        colors = sns.color_palette("pastel", len(cause_sum))

        # Plot pie with only percentages shown inside
        wedges, texts, autotexts = ax.pie(
            cause_sum.values,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 9, 'color': 'black'},
            colors=colors,
            pctdistance=0.75
        )

        # External legend
        labels = [label.replace("_", " ").title() for label in cause_sum.index]
        handles = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(len(labels))]
        ax.legend(
            handles=handles,
            loc='center left',
            bbox_to_anchor=(1, 0.5),
            fontsize=9,
            title="Delay Cause"
        )

        ax.set_title("Delay Causes Proportion (Peak Months)", fontsize=12)
        ax.axis("equal")
        fig.tight_layout()
        return fig

    def plot_avg_delay_pct_by_cause(self):
        # Calculate and sort average delay percentages by cause
        avg_pct = self.df[[f"{col}_pct" for col in self.delay_cols]].mean()
        avg_pct = avg_pct.sort_values(ascending=True)

        # Plot sorted values
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(x=avg_pct.index, y=avg_pct.values, ax=ax, palette="muted")

        ax.set_title("Average Delay Percentage by Cause")
        ax.set_ylabel("Average % of Total Delay")
        ax.set_xlabel("Delay Cause")
        plt.xticks(rotation=45)
        fig.tight_layout()
        return fig


    def plot_dominant_delay_causes_count(self):
        count = self.df['dominant_delay_cause'].value_counts().sort_values().reset_index()
        count.columns = ['Cause', 'Count']
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(data=count, x='Cause', y='Count', ax=ax, palette="pastel")
        ax.set_title("Dominant Delay Cause per Flight")
        ax.bar_label(ax.containers[0])
        plt.xticks(rotation=45)
        fig.tight_layout()
        return fig

    # 4. Seasonal Patterns
    def plot_avg_delay_per_flight_seasonal(self):
        df = self.df.groupby('season')['mean_delay_per_flight'].mean().reset_index()
        df = df.sort_values(by='mean_delay_per_flight')  # ✅ sort ascending

        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(data=df, x='season', y='mean_delay_per_flight', ax=ax, palette='coolwarm')
        ax.set_title("Average Delay per Flight by Season")
        ax.set_ylabel("Avg Delay (mins)")
        ax.set_xlabel("Season")
        fig.tight_layout()
        return fig


    def plot_flights_per_season(self):
        df = self.df.groupby('season')['arr_flights'].sum().reset_index()
        df = df.sort_values(by='arr_flights')  # ✅ sort ascending

        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(data=df, x='season', y='arr_flights', ax=ax, palette='viridis')
        ax.set_title("Total Flights per Season")
        ax.set_ylabel("Total Flights")
        ax.set_xlabel("Season")
        fig.tight_layout()
        return fig


    def plot_delay_causes_seasonal_distribution(self):
        df = self.df.groupby('season')[self.delay_cols].sum().reset_index()
        df['total'] = df[self.delay_cols].sum(axis=1)
        df = df.sort_values(by='total')  # ✅ sort seasons by total delay

        melted = df.drop(columns='total').melt(id_vars='season', var_name='Cause', value_name='Total Delay')

        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(data=melted, x='season', y='Total Delay', hue='Cause', ax=ax)
        ax.set_title("Delay Cause Distribution by Season")
        ax.set_ylabel("Total Delay Minutes")
        fig.tight_layout()
        return fig


    def plot_disruption_rate_by_season(self):
        df = self.df.groupby('season')['disrupted'].mean().reset_index()
        df = df.sort_values(by='disrupted')  # ✅ sort ascending

        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(data=df, x='season', y='disrupted', ax=ax, palette='mako')
        ax.set_title("Disruption Rate by Season")
        ax.set_ylabel("Disruption Rate")
        ax.set_xlabel("Season")
        fig.tight_layout()
        return fig


    # 5. Carrier Behavior
    
    def avg_delay_ratio_per_carrier(self):
        # Group and sort ascending by delay ratio
        df = self.df.groupby('carrier_name')['delay_ratio'].mean().reset_index()
        df = df.sort_values(by='delay_ratio', ascending=True)

        # ✅ Ensure carrier_name is string and categorical in sorted order
        df['carrier_name'] = df['carrier_name'].astype(str)
        df['carrier_name'] = pd.Categorical(df['carrier_name'], categories=df['carrier_name'], ordered=True)

        fig, ax = plt.subplots(figsize=(12, 5))

        # ✅ Explicitly tell Seaborn not to reorder
        sns.barplot(data=df, x='carrier_name', y='delay_ratio', ax=ax, order=df['carrier_name'])

        ax.set_title("Average Delay Ratio per Carrier")
        ax.set_ylabel("Delay Ratio")
        ax.set_xlabel("Carrier")
        ax.tick_params(axis='x', labelrotation=45, labelsize=8)
        fig.tight_layout()
        return fig





    def delay_cause_vs_disruption_correlation(self):
        summary = self.df.groupby('carrier_name').agg({
            'disrupted': 'mean', **{col: 'sum' for col in self.delay_cols}
        }).reset_index()

        fig, ax = plt.subplots(figsize=(8, 5))
        for col in self.delay_cols:
            sns.scatterplot(x=summary[col], y=summary['disrupted'], ax=ax, label=col.replace('_', ' ').title(), s=60)
        ax.set_title("Disruption Rate vs Delay Cause (Carrier Level)")
        ax.set_xlabel("Total Delay Minutes")
        ax.set_ylabel("Disruption Rate")
        ax.legend(title='Delay Cause', fontsize=7, title_fontsize=8, bbox_to_anchor=(1.05, 1), loc='upper left')
        fig.tight_layout()
        return fig


    # 6. Airport Insights
    def top_airports_delay_metrics(self):
        # Top 10 airports by total flights
        top = self.df.groupby('airport_name')['arr_flights'].sum().nlargest(10).index
        df_top = self.df[self.df['airport_name'].isin(top)].copy()
        df_top['airport_short'] = df_top['airport_name'].str[:10]

        # Avg delay per flight
        avg_delay = df_top.groupby('airport_short')['mean_delay_per_flight'].mean().reset_index()

        # Avg airport delay rate
        self.df['airport_delay_rate'] = pd.to_numeric(self.df['airport_delay_rate'], errors='coerce')
        delay_rate = self.df.groupby('airport_name')['airport_delay_rate'].mean().reset_index()
        delay_rate = delay_rate[delay_rate['airport_name'].isin(top)].copy()
        delay_rate['airport_short'] = delay_rate['airport_name'].str[:10]

        # Merge and sort by average delay
        merged = pd.merge(avg_delay, delay_rate[['airport_short', 'airport_delay_rate']], on='airport_short')
        merged = merged.sort_values(by='mean_delay_per_flight')  # ✅ sort by delay for intuitive visual

        # Melt for bar plot
        melted = merged.melt(id_vars='airport_short', var_name='Metric', value_name='Value')

        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(data=melted, x='airport_short', y='Value', hue='Metric', ax=ax)
        ax.set_title("Top Airports: Avg Delay vs Delay Rate")
        ax.set_ylabel("Metric Value")
        ax.set_xlabel("Airport (Short Code)")
        fig.tight_layout()
        return fig


    def delay_ratio_vs_flight_volume(self):
        df = self.df.copy()

        # Aggregate and sort by flight volume
        agg_df = df.groupby('airport_name').agg({
            'arr_flights': 'sum',
            'delay_ratio': 'mean'
        }).reset_index().sort_values(by='arr_flights')  # ✅ sorted left to right

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(
            data=agg_df,
            x='arr_flights',
            y='delay_ratio',
            alpha=0.6,
            s=60,
            ax=ax,
            color='steelblue'
        )

        ax.set_title("Airport-Level: Delay Ratio vs Flight Volume", fontsize=12)
        ax.set_xlabel("Total Flight Volume", fontsize=10)
        ax.set_ylabel("Average Delay Ratio", fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.4)
        fig.tight_layout()
        return fig





    def airport_delay_cause_heatmap(self):
        df = self.df.copy()

        delay_cols = ['carrier_ct', 'weather_ct', 'nas_ct', 'security_ct', 'late_aircraft_ct']

        # Aggregate delays
        delay_sum = df.groupby('airport_name')[delay_cols].sum()

        # Focus on top 20 busiest airports
        top_airports = df.groupby('airport_name')['arr_flights'].sum().nlargest(20).index
        delay_sum = delay_sum.loc[top_airports]

        # Normalize column names
        delay_sum.columns = [col.replace('_ct', '').replace('_', ' ').title() for col in delay_sum.columns]

        fig, ax = plt.subplots(figsize=(12, 7))
        sns.heatmap(
            delay_sum,
            cmap="YlOrRd",
            linewidths=0.3,
            linecolor='white',
            annot=True,
            fmt=".0f",
            cbar_kws={'label': 'Total Delay Count'}
        )

        ax.set_title("Top 20 Airports: Delay Cause Breakdown", fontsize=13)
        ax.set_xlabel("Delay Cause")
        ax.set_ylabel("Airport")
        ax.tick_params(axis='y', labelsize=8)
        fig.tight_layout()
        return fig




    # 7. Risk Insights
    def plot_delay_risk_level_distribution(self):
        # Count and normalize risk levels, then sort ascending
        df = self.df['delay_risk_level'].value_counts(normalize=True).sort_values().reset_index()
        df.columns = ['Risk Level', 'Proportion']

        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(data=df, x='Risk Level', y='Proportion', ax=ax, palette='Set2')

        ax.set_title("Distribution of Delay Risk Levels")
        ax.set_ylabel("Proportion of Flights")
        ax.set_xlabel("Risk Level")
        fig.tight_layout()
        return fig

