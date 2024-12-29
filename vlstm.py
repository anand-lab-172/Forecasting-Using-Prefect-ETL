from prefect import flow, task
from prefect_dask.task_runners import DaskTaskRunner
import pandas as pd
import numpy as np
import os, sys, logging
from sotam import VLSTM

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filename='pipeline.log',
    encoding='utf-8'  # Ensure UTF-8 encoding for logs
)

@task(log_prints=True)
def extract_data(file_path: str):
    logging.info("Starting data extraction...")
    df = pd.read_csv(file_path, usecols=lambda column: column != "Unnamed: 0", 
                     parse_dates=['Date'], index_col='Date', encoding='utf-8')
    logging.info("Data extraction completed.")
    return df

@task
def preprocess_data(df: pd.DataFrame):
    logging.info("Starting data preprocessing...")
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['day'] = df.index.day
    df['dayofweek'] = df.index.dayofweek
    df['weekno'] = df.index.isocalendar().week
    df['isweekend'] = df.index.weekday // 5
    df['season'] = df['month'].apply(lambda month: 1 if month in [12, 1, 2] else 
                                     2 if month in [3, 4, 5] else 
                                     3 if month in [6, 7, 8] else 4)
    df.sort_index(inplace=True)
    logging.info("Data preprocessing completed.")
    return df

@task
def select_top_features(df: pd.DataFrame):
    logging.info("Starting feature selection...")
    corr_matrix = df.corr().abs()
    target = 'Close'
    normalized_corr = (corr_matrix[f'{target}'] - corr_matrix[f'{target}'].min()) / \
                      (corr_matrix[f'{target}'].max() - corr_matrix[f'{target}'].min())
    n = 6
    top_features = normalized_corr.sort_values(ascending=False).index[:n].to_list()
    logging.info(f"Top features correlated with {target}: {top_features}")
    return top_features

@task
def vlstm_forecast(df: pd.DataFrame, top_features: list):
    logging.info("Starting VLSTM forecast...")
    vlstm = VLSTM(target='Close', epochs=10)  # Adjust VLSTM parameters as needed
    history, y_test, y_pred, train_score, test_score = vlstm.train(df, top_features)
    forecast, high_trend, low_trend = vlstm.forecast(df, top_features, 10, noise_factor=0.02)
    logging.info("VLSTM forecast completed.")
    return forecast, high_trend, low_trend

@task
def save_forecast_data(forecast, high_trend, low_trend, output_path: str):
    logging.info("Saving forecast data to CSV...")
    forecast_data = pd.DataFrame({
        'forecast': forecast,
        'high_trend': high_trend,
        'low_trend': low_trend
    })
    forecast_data.to_csv(output_path, index=False, encoding='utf-8')
    logging.info(f"Forecast data saved to {output_path}.")

@flow(name="Stock Forecasting ETL Pipeline", description="Forecasting Using VLSTM Model", log_prints=True)
def stock_forecasting_etl_pipeline(input_file: str, output_file: str):
    logging.info("Starting Stock Forecasting ETL Pipeline...")
    raw_data = extract_data(input_file)
    preprocessed_data = preprocess_data(raw_data)
    top_features = select_top_features(preprocessed_data)
    forecast_data, high_trend, low_trend = vlstm_forecast(preprocessed_data, top_features)
    save_forecast_data(forecast_data, high_trend, low_trend, output_file)
    logging.info("ETL Pipeline completed successfully.")

# Run the pipeline
if __name__ == "__main__":
    stock_forecasting_etl_pipeline(input_file, output_file)
