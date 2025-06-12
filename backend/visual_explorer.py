import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class VisualExplorer:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def view_columns(self, columns, num_rows):
        return self.df[columns].head(num_rows)

    def view_row_by_index(self, index):
        if 0 <= index < len(self.df):
            return self.df.iloc[[index]]
        else:
            return pd.DataFrame({"Error": ["Index out of bounds"]})

    def univariate_plot(self, column, kind="hist"):
        plt.figure(figsize=(8, 4))
        if kind == "hist":
            sns.histplot(self.df[column], kde=True, bins=30)
        elif kind == "box":
            sns.boxplot(x=self.df[column])
        elif kind == "violin":
            sns.violinplot(x=self.df[column])
        plt.title(f"{kind.capitalize()} Plot of {column}")
        plt.tight_layout()
        return plt.gcf()

    def bivariate_plot(self, x_col, y_col, kind="scatter"):
        plt.figure(figsize=(8, 4))
        if kind == "scatter":
            sns.scatterplot(x=self.df[x_col], y=self.df[y_col])
        elif kind == "line":
            sns.lineplot(x=self.df[x_col], y=self.df[y_col])
        elif kind == "box":
            sns.boxplot(x=self.df[x_col], y=self.df[y_col])
        elif kind == "bar":
            sns.barplot(x=self.df[x_col], y=self.df[y_col])
        plt.title(f"{kind.capitalize()} Plot of {x_col} vs {y_col}")
        plt.tight_layout()
        return plt.gcf()

    def correlation_heatmap(self, columns):
        plt.figure(figsize=(10, 6))
        if not columns or len(columns) < 2:
            plt.text(0.5, 0.5, "Select at least two numeric columns", ha='center', va='center', fontsize=12)
        else:
            corr = self.df[columns].corr()
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        return plt.gcf()
