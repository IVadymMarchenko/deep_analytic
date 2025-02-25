from scipy.interpolate import make_interp_spline
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
from .func_name import aggregation_method
import matplotlib.ticker as ticker
from matplotlib import ticker
import pandas as pd

#aggregated_data = df.groupby(x_column)[y_columns].count().reset_index()
class MakeGraphs:
    """
    Class for constructing bar charts with support for various aggregation functions.
    """
    def make_bar_char(self,df, x_column, y_columns, aggregation_function, title="Bar Chart", xlabel=None, ylabel=None, figsize=(12, 6)):

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

        
        # agregation data
        aggregated_data = aggregation_method(df,x_column,y_columns,aggregation_function)

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



    def make_line_chart(self, df, x_column, y_columns, aggregation_function, title="Line Chart", xlabel=None, ylabel=None, figsize=(12, 6)):
        """Universal function to plot a line chart with smooth curves."""
        # Проверка типа данных в x_column и преобраз, если это даты
       
        if pd.api.types.is_datetime64_any_dtype(df[x_column]) or pd.api.types.is_object_dtype(df[x_column]):
            try:
                df[x_column] = pd.to_datetime(df[x_column], errors="coerce")
                if df[x_column].isna().any():
                    raise ValueError(f"Incorrect date values ​​in column '{x_column}'. Please check your data.")
            except Exception as e:
                raise ValueError(f"Error converting '{x_column}' to date: {e}")
       # Агрегация данных
        aggregated_data = aggregation_method(df,x_column,y_columns,aggregation_function)

        # Удаление дубликатов значений по оси X
        aggregated_data = aggregated_data.drop_duplicates(subset=[x_column])
        plt.figure(figsize=figsize)

        for y_column in y_columns:
        # Проверка наличия столбца y_column
            if y_column not in aggregated_data.columns:
                raise ValueError(f"Column '{y_column}' is missing from aggregated data.")

        # Получение данных для интерполяции
            x = aggregated_data[x_column]
            y = aggregated_data[y_column]

        # Проверяем, что данные не пустые
            if x.empty or y.empty:
                raise ValueError(f"No data to plot for column '{y_column}'.")

        # Преобразование для интерполяции: проверка, является ли x числовым
            if pd.api.types.is_numeric_dtype(x):
                x_smooth = np.linspace(x.min(), x.max(), 100)
                y_smooth = make_interp_spline(x, y,k=2)(x_smooth)
                plt.plot(x_smooth, y_smooth, label=y_column, linewidth=2)
            elif pd.api.types.is_datetime64_any_dtype(x):
                # Если x - даты, преобразуем их в числовой формат
                x_numeric = x.astype(np.int64) // 10**9
                x_smooth_numeric = np.linspace(x_numeric.min(), x_numeric.max(), 100)
                y_smooth = make_interp_spline(x_numeric, y)(x_smooth_numeric)
                x_smooth_dates = pd.to_datetime(x_smooth_numeric * 10**9)
                plt.plot(x_smooth_dates, y_smooth, label=y_column, linewidth=2)
            else:
                raise ValueError(f"Column '{x_column}' must be either numeric or date.")

        # Настройки графика
        plt.title(title, fontsize=14)
        plt.xlabel(xlabel if xlabel else x_column, fontsize=12)
        plt.ylabel(ylabel if ylabel else "Meaning", fontsize=12)
        plt.xticks(rotation=30, ha="right")
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.show()