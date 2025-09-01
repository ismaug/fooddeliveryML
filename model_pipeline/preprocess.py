
# model_pipeline/preprocess.py
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATA_PATH = os.getenv('DATA_PATH', 'Food_Delivery_Times.csv')
MODEL_OUTPUT_PATH = os.getenv('MODEL_OUTPUT_PATH', 'models/')

#Load data
def load_data(path=None):
    path = path or DATA_PATH
    return pd.read_csv(path)

# Manage missing values
def clean_missing(df):
    df = df.copy()
    # Mode for categorical
    df['Weather'] = df['Weather'].fillna(df['Weather'].mode()[0])
    df['Traffic_Level'] = df['Traffic_Level'].fillna(df['Traffic_Level'].mode()[0])
    df['Time_of_Day'] = df['Time_of_Day'].fillna(df['Time_of_Day'].mode()[0])
    # Median for discrete numeric
    df['Courier_Experience_yrs'] = df['Courier_Experience_yrs'].fillna(df['Courier_Experience_yrs'].median())
    return df
# Handle outliers
def handle_outliers(df, drop=True):
    df = df.copy()
    # Only handle target variable outliers
    col = 'Delivery_Time_min'
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    floor = Q1 - 1.5 * IQR
    ceiling = Q3 + 1.5 * IQR
    
    outliers = df[(df[col] < floor) | (df[col] > ceiling)]
    print(f"Found {len(outliers)} outliers in {col}")
    
    if drop and len(outliers) > 0:
        df = df.drop(index=outliers.index)
        
    return df

def select_features(df):
    return df.drop(columns=['Order_ID'], errors='ignore')

#For non-linear models, add simple features
def add_features(df):
    df = df.copy()
    
    # Distance categories
    df['Distance_Category'] = pd.cut(df['Distance_km'], 
                                   bins=[0, 5, 15, float('inf')], 
                                   labels=['Short', 'Medium', 'Long'])
    
    # Rush hour indicator
    df['Is_Rush_Hour'] = df['Time_of_Day'].isin(['Morning', 'Evening'])
    
    return df

def get_preprocessor():
    num_features = ['Distance_km', 'Preparation_Time_min', 'Courier_Experience_yrs']
    cat_features = ['Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type', 'Distance_Category']
    bool_features = ['Is_Rush_Hour']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', num_features),
            ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_features),
            ('bool', 'passthrough', bool_features)
        ],
        verbose_feature_names_out=False # Avoid prefixing feature names prevnents warnings
    )
    return preprocessor

def data_cleaning(path=None, drop_outliers=True):
    df = load_data(path)
    df = clean_missing(df)
    df = handle_outliers(df, drop=drop_outliers)
    df = select_features(df)
    
    df = add_features(df)
    return df
