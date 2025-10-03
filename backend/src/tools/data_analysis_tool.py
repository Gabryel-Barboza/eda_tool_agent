import io
import uuid

import pandas as pd
import plotly.express as px
from langchain.tools import tool
from plotly.basedatatypes import BaseFigure
from sklearn.cluster import KMeans

from src.services.data_processing import get_dataframe
from src.services.db_services import insert_graphs_db


def _save_graph_to_db(fig: BaseFigure) -> str:
    """
    Saves the graph's JSON to a 'database' and returns a unique ID.
    In a real application, this would interact with a database.
    """
    graph_id = str(uuid.uuid4())
    graph_json = fig.to_json()

    insert_graphs_db(graph_id, graph_json)

    return graph_id


@tool('get_data_summary')
def get_data_summary() -> str:
    """
    Returns a string with a summary of the DataFrame, including dtypes,
    non-null counts, and descriptive statistics. Use this to get a general
    overview of the dataset.
    """
    df = get_dataframe()

    if df is None or df.empty:
        return 'DataFrame empty, no data to analyse.'

    info_buffer = io.StringIO()
    df.info(buf=info_buffer)
    info_str = info_buffer.getvalue()

    desc_str = df.describe(include='all').to_string()

    return f'Data Summary:\n\n{info_str}\n\nDescriptive Statistics:\n{desc_str}'


@tool('get_data_rows')
def get_data_rows(n_rows: int = 10, sample_method: str = 'head') -> str:
    """
    Returns a sample of N rows from the DataFrame.
    Use this to get a quick sample of the data and see its structure.

    Args:
        n_rows (int): The number of rows to return. Defaults to 10.
        sample_method (str): The method for sampling. Can be 'head' (first N rows),
                             'tail' (last N rows), or 'random' (N random rows).
                             Defaults to 'head'.
    """
    df = get_dataframe()

    if df is None or df.empty:
        return 'DataFrame empty, no data to analyse.'

    if not isinstance(n_rows, int) or n_rows <= 0:
        return 'Error: Number of rows (n_rows) must be a positive integer.'

    if sample_method == 'head':
        return df.head(n_rows).to_string()
    if sample_method == 'tail':
        return df.tail(n_rows).to_string()
    if sample_method == 'random':
        return df.sample(n=min(n_rows, len(df))).to_string()

    return "Error: Invalid sample_method. Choose from 'head', 'tail', or 'random'."


@tool('get_correlation_matrix')
def get_correlation_matrix() -> str:
    """
    Returns the correlation matrix for the numeric columns of the DataFrame.
    Use this to understand the linear relationships between numeric variables.
    """
    df = get_dataframe()

    if df is None or df.empty:
        return 'DataFrame empty, no data to analyse.'

    numeric_df = df.select_dtypes(include='number')
    if numeric_df.empty:
        return 'No numeric columns found to calculate correlation.'

    return numeric_df.corr().to_string()


@tool('detect_outliers_iqr')
def detect_outliers_iqr(column: str) -> str:
    """
    Detects outliers in a numeric column using the IQR method.
    Use this to identify unusual data points in a specific column.
    """
    df = get_dataframe()

    if df is None or df.empty:
        return 'DataFrame empty, no data to analyse.'

    if column not in df.columns:
        return f'Error: Column "{column}" not found in the dataset.'
    if not pd.api.types.is_numeric_dtype(df[column]):
        return f'Error: Column "{column}" is not numeric.'

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

    if outliers.empty:
        return f'No outliers detected in column "{column}".'

    return f'Detected {len(outliers)} outliers in column "{column}":\n{outliers.to_string()}'


@tool('create_histogram')
def create_histogram(column: str) -> dict:
    """
    Generates a histogram for a given column, saves it, and returns its unique ID.
    Use this to visualize the distribution of a single numeric variable.
    """
    df = get_dataframe()

    if df is None or df.empty:
        return 'DataFrame empty, no data to analyse.'

    if column not in df.columns:
        return f'Error: Column "{column}" not found in the dataset.'
    if not pd.api.types.is_numeric_dtype(df[column]):
        return f'Error: Column "{column}" is not numeric. Use create_bar_chart for categorical columns.'

    fig = px.histogram(df, x=column)
    graph_id = _save_graph_to_db(fig)
    return {
        'response': f'Histogram for "{column}" created successfully.',
        'graph_id': graph_id,
    }


@tool('create_scatter_plot')
def create_scatter_plot(x_column: str, y_column: str) -> dict:
    """
    Generates a scatter plot for two columns, saves it, and returns its unique ID.
    Use this to visualize the relationship between two numeric variables.
    """
    df = get_dataframe()

    if df is None or df.empty:
        return 'DataFrame empty, no data to analyse.'

    if x_column not in df.columns or y_column not in df.columns:
        return 'Error: One or both columns not found in the dataset.'
    fig = px.scatter(df, x=x_column, y=y_column)
    graph_id = _save_graph_to_db(fig)
    return {
        'response': f'Scatter plot for "{x_column}" vs "{y_column}" created successfully.',
        'graph_id': graph_id,
    }


@tool('create_bar_chart')
def create_bar_chart(column: str) -> dict:
    """
    Generates a bar chart for a given categorical column, saves it, and returns its unique ID.
    Use this to visualize the frequency distribution of a categorical variable.
    """
    df = get_dataframe()

    if df is None or df.empty:
        return 'DataFrame empty, no data to analyse.'

    if column not in df.columns:
        return f'Error: Column "{column}" not found in the dataset.'
    if pd.api.types.is_numeric_dtype(df[column]):
        return f'Error: Column "{column}" is numeric. Use create_histogram for numeric columns.'

    counts = df[column].value_counts().reset_index()
    counts.columns = [column, 'count']
    fig = px.bar(counts, x=column, y='count', title=f'Distribution of {column}')
    graph_id = _save_graph_to_db(fig)
    return {
        'response': f'Bar chart for "{column}" created successfully.',
        'graph_id': graph_id,
    }


@tool('create_line_plot')
def create_line_plot(x_column: str, y_column: str) -> dict:
    """
    Generates a line plot, saves it, and returns its unique ID.
    Use this to visualize trends over time. 'x_column' should ideally be a datetime column.
    """
    df = get_dataframe()

    if df is None or df.empty:
        return 'DataFrame empty, no data to analyse.'

    if x_column not in df.columns or y_column not in df.columns:
        return 'Error: One or both columns not found in the dataset.'

    fig = px.line(
        df, x=x_column, y=y_column, title=f'Trend of {y_column} over {x_column}'
    )
    graph_id = _save_graph_to_db(fig)
    return {
        'response': f'Line plot for "{y_column}" over "{x_column}" created successfully.',
        'graph_id': graph_id,
    }


@tool('create_box_plot')
def create_box_plot(y_column: str, x_column: str = None) -> dict:
    """
    Generates a box plot, saves it, and returns its unique ID.
    Use this to visualize the distribution of a numeric variable (y_column),
    optionally grouped by a categorical variable (x_column).
    """
    df = get_dataframe()

    if df is None or df.empty:
        return 'DataFrame empty, no data to analyse.'

    if y_column not in df.columns:
        return f'Error: Column "{y_column}" not found in the dataset.'
    if not pd.api.types.is_numeric_dtype(df[y_column]):
        return f'Error: Column "{y_column}" must be numeric for a box plot.'

    title = f'Box Plot for {y_column}'
    if x_column:
        if x_column not in df.columns:
            return f'Error: Grouping column "{x_column}" not found in the dataset.'
        title += f' grouped by {x_column}'

    fig = px.box(df, y=y_column, x=x_column, title=title)
    graph_id = _save_graph_to_db(fig)
    return {
        'response': f'Box plot for "{y_column}" created successfully.',
        'graph_id': graph_id,
    }


@tool('create_correlation_heatmap')
def create_correlation_heatmap() -> dict:
    """
    Generates a correlation heatmap for numeric columns, saves it, and returns its ID.
    Use this for a visual overview of the linear relationships between variables.
    """
    df = get_dataframe()

    if df is None or df.empty:
        return 'DataFrame empty, no data to analyse.'

    numeric_df = df.select_dtypes(include='number')

    if numeric_df.shape[1] < 2:
        return 'Error: At least two numeric columns are required to create a correlation heatmap.'

    corr_matrix = numeric_df.corr()
    fig = px.imshow(corr_matrix, text_auto=True, title='Correlation Heatmap')
    graph_id = _save_graph_to_db(fig)
    return {
        'response': 'Correlation heatmap created successfully.',
        'graph_id': graph_id,
    }


@tool('find_clusters_and_plot')
def find_clusters_and_plot(x_column: str, y_column: str, n_clusters: int) -> dict:
    """
    Performs K-Means clustering and generates a scatter plot, saves it, and returns its unique ID.
    Use this to identify and visualize groupings in your data.
    """
    df = get_dataframe()

    if df is None or df.empty:
        return 'DataFrame empty, no data to analyse.'

    if x_column not in df.columns or y_column not in df.columns:
        return 'Error: One or both columns not found in the dataset.'

    if not pd.api.types.is_numeric_dtype(
        df[x_column]
    ) or not pd.api.types.is_numeric_dtype(df[y_column]):
        return f'Error: Columns "{x_column}" and "{y_column}" must be numeric for clustering.'

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_data = df[[x_column, y_column]].dropna()
    cluster_data['cluster'] = kmeans.fit_predict(cluster_data)
    cluster_data['cluster'] = cluster_data['cluster'].astype(
        str
    )  # For discrete colors in plotly

    fig = px.scatter(
        cluster_data,
        x=x_column,
        y=y_column,
        color='cluster',
        title=f'Clusters in {x_column} vs {y_column}',
    )
    graph_id = _save_graph_to_db(fig)
    return {
        'response': f'Cluster plot for "{x_column}" vs "{y_column}" with {n_clusters} clusters created successfully. 📊',
        'graph_id': graph_id,
    }


# @tool('remove_outliers_iqr')
# def remove_outliers_iqr(, column: str) -> tuple[pd.DataFrame, str]:
#     """
#     Removes outliers from a numeric column using the IQR method and returns the updated dataframe.
#     Use this to clean the data before further analysis.

#     Returns a tuple with the new dataframe and a message.
#     """
#     if not df:
#         return 'DataFrame empty, no data to analyse.'

#     if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
#         return df, f'Error: Column "{column}" is not a valid numeric column.'

#     initial_rows = len(df)
#     q1 = df[column].quantile(0.25)
#     q3 = df[column].quantile(0.75)
#     iqr = q3 - q1
#     lower_bound = q1 - 1.5 * iqr
#     upper_bound = q3 + 1.5 * iqr

#     df_cleaned = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
#     rows_removed = initial_rows - len(df_cleaned)

#     return (
#         df_cleaned,
#         f'{rows_removed} outliers removed from column "{column}". The dataframe has been updated.',
#     )
