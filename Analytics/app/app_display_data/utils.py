import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from .func_name import aggregation_functions
from matplotlib import ticker


#aggregated_data = df.groupby(x_column)[y_columns].count().reset_index()
class MakeGraphBar:
    """
    Class for constructing bar charts with support for various aggregation functions.
    """
    def make_bar_char(self,df, x_column, y_columns, aggregation_function, title="Диаграмма продаж", xlabel=None, ylabel=None, figsize=(12, 6)):

        """Plot a column chart.
        :param df: DataFrame with data.
        :param x_column: Column name for the X-axis.
        :param y_columns: List of columns for the Y-axis.
        :param aggregation_function: Aggregation function ('sum', 'count', 'max', 'min', 'average', 'unique').
        :param title: Chart title.
        :param xlabel: X-axis title.
        :param ylabel: Y-axis title.
        :param figsize: Figure size.
        :raises ValueError: If an unsupported aggregation function is passed."""

        aggregation_methods = {
            "sum": lambda group: group[y_columns].sum(),
            "count": lambda group: group[y_columns].count(),
            "max": lambda group: group[y_columns].max(),
            "min": lambda group: group[y_columns].min(),
            "average": lambda group: group[y_columns].mean(),
            "unique": lambda group: group[y_columns].nunique(),
        }
        # agregation data
        aggregated_data = df.groupby(x_column).apply(aggregation_methods[aggregation_function]).reset_index()

        plt.figure(figsize=figsize)
        for y_column in y_columns:
            plt.bar(aggregated_data[x_column], aggregated_data[y_column], alpha=0.7, label=y_column)
        #Formatting numbers on the Y axis
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: x))
        plt.title(title, fontsize=14)
        plt.xlabel(xlabel if xlabel else x_column, fontsize=12)
        plt.ylabel(str(*y_columns))
        plt.xticks(rotation=30, ha='right')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.show()



