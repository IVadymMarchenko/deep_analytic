aggregation_functions = ['sum','max','min','count','average','unique']





def aggregation_method(df,x_column,y_columns,aggregation_function):
    aggregation_methods = {
            "sum": lambda group: group[y_columns].sum(),
            "count": lambda group: group[y_columns].count(),
            "max": lambda group: group[y_columns].max(),
            "min": lambda group: group[y_columns].min(),
            "average": lambda group: group[y_columns].mean(),
            "unique": lambda group: group[y_columns].nunique(),
        }
    aggregated_data = df.groupby(x_column).apply(aggregation_methods[aggregation_function]).reset_index()
    return aggregated_data