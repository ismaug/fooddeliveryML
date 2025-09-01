# model_pipeline/train.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import lightgbm as lgb
from preprocess import data_cleaning, get_preprocessor, MODEL_OUTPUT_PATH
import joblib
import os

#Model evaluation metrics
def evaluate_model(y_true, y_pred, model_name):
    return {
        'model': model_name,
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'mae': mean_absolute_error(y_true, y_pred),
        'r2': r2_score(y_true, y_pred),
        'mape': np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    }

def train_multiple_models(X_train, X_test, y_train, y_test):
    
    # Get preprocessor
    preprocessor = get_preprocessor()
    
    # Diferent models to train slightly tuned to avoid overfitting
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=10.0),  # Increased regularization
        'Random Forest': RandomForestRegressor(
            n_estimators=50,      # Reduced trees
            max_depth=10,         # Limit depth
            min_samples_split=10, # Require more samples to split
            min_samples_leaf=5,   # Require more samples in leaves
            random_state=42
        ),
        'XGBoost': xgb.XGBRegressor(
            n_estimators=50,      # Reduced trees
            max_depth=6,          # Limit depth
            learning_rate=0.1,    # Slower learning
            subsample=0.8,        # Use subset of data
            colsample_bytree=0.8, # Use subset of features
            reg_alpha=1.0,        # L1 regularization
            reg_lambda=1.0,       # L2 regularization
            random_state=42
        ),
        'LightGBM': lgb.LGBMRegressor(
            n_estimators=50,      # Reduced trees
            max_depth=6,          # Limit depth
            learning_rate=0.1,    # Slower learning
            subsample=0.8,        # Use subset of data
            colsample_bytree=0.8, # Use subset of features
            reg_alpha=1.0,        # L1 regularization
            reg_lambda=1.0,       # L2 regularization
            random_state=42,
            verbose=-1
        )
    }
    
    results = []
    trained_models = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Create pipeline
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', model)
        ])
        
        # Train
        pipeline.fit(X_train, y_train)
        
        # Predict
        train_pred = pipeline.predict(X_train)
        test_pred = pipeline.predict(X_test)
        
        # Evaluate
        train_metrics = evaluate_model(y_train, train_pred, f"{name} (Train)")
        test_metrics = evaluate_model(y_test, test_pred, f"{name} (Test)")
        
        # Calculate overfitting indicator
        overfitting = train_metrics['r2'] - test_metrics['r2']
        test_metrics['overfitting'] = overfitting
        
        results.append(train_metrics)
        results.append(test_metrics)
        trained_models[name] = pipeline
        
        print(f"  Train R²: {train_metrics['r2']:.4f}, Test R²: {test_metrics['r2']:.4f}")
        print(f"  Test RMSE: {test_metrics['rmse']:.2f}, Overfitting: {overfitting:.4f}")
    
    return results, trained_models

def save_best_model(trained_models, results, output_path):
    
    # Find best model based on test R²
    test_results = [r for r in results if 'Test' in r['model']]
    best_result = max(test_results, key=lambda x: x['r2'])
    best_model_name = best_result['model'].replace(' (Test)', '')
    
    print(f"\nBest model: {best_model_name} with R² = {best_result['r2']:.4f}")
    
    # Save best model
    os.makedirs(output_path, exist_ok=True)
    model_path = os.path.join(output_path, 'best_model.joblib')
    joblib.dump(trained_models[best_model_name], model_path)
    
    print(f"Best model saved to: {model_path}")
    return trained_models[best_model_name], best_result

#Model results comparison table
def print_results_table(results):
    print(f"{'Model':<25} {'RMSE':<10} {'MAE':<10} {'R²':<10} {'MAPE':<10}")
    print("-"*70)
    
    for result in results:
        print(f"{result['model']:<25} {result['rmse']:<10.2f} {result['mae']:<10.2f} "
              f"{result['r2']:<10.4f} {result['mape']:<10.2f}")

if __name__ == "__main__":
    # Load and preprocess data
    print("Loading and preprocessing data...")
    df = data_cleaning(drop_outliers=True)
    
    # Split features and target
    X = df.drop(columns=['Delivery_Time_min'])
    y = df['Delivery_Time_min']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Train multiple models
    results, trained_models = train_multiple_models(X_train, X_test, y_train, y_test)
    
    # Print results
    print_results_table(results)
    
    # Save best model
    best_model, best_metrics = save_best_model(trained_models, results, MODEL_OUTPUT_PATH)