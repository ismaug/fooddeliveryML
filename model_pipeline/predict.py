# model_pipeline/predict.py
import joblib
import pandas as pd
from preprocess import MODEL_OUTPUT_PATH
import os

class DeliveryPredictor:
    
    def __init__(self, model_path=None):
        model_path = model_path or os.path.join(MODEL_OUTPUT_PATH, 'best_model.joblib')
        self.model = joblib.load(model_path)
        print(f"Model loaded from: {model_path}")
    
    def predict_single(self, distance_km, weather, traffic_level, time_of_day, 
                      vehicle_type, preparation_time_min, courier_experience_yrs):
        # This predicts delivery time for a single order
        
        # Most likely distance is in km so we can categorize it for our engineered feature
        if distance_km <= 5:
            distance_category = 'Small'
        elif distance_km <= 15:
            distance_category = 'Medium'
        else:
            distance_category = 'Large'
            
        # Rush hour logic
        is_rush_hour = time_of_day in ['Morning', 'Evening']
        
        # Create DataFrame with single row
        data = pd.DataFrame({
            'Distance_km': [distance_km],
            'Weather': [weather],
            'Traffic_Level': [traffic_level],
            'Time_of_Day': [time_of_day],
            'Vehicle_Type': [vehicle_type],
            'Preparation_Time_min': [preparation_time_min],
            'Courier_Experience_yrs': [courier_experience_yrs],
            'Distance_Category': [distance_category],
            'Is_Rush_Hour': [is_rush_hour]
        })
        
        # Predict
        prediction = self.model.predict(data)[0]
        return round(prediction, 1)
    
    def predict_batch(self, df):
        # For batch predictions we expand the DataFrame
        predictions = self.model.predict(df)
        return predictions

# Test
if __name__ == "__main__":
    # Test the predictor
    predictor = DeliveryPredictor()
    
    # Example prediction
    predicted_time = predictor.predict_single(
        distance_km=10.5,
        weather='Rainy',
        traffic_level='High',
        time_of_day='Evening',
        vehicle_type='Bike',
        preparation_time_min=15,
        courier_experience_yrs=2.5
    )
    
    print(f"Predicted delivery time: {predicted_time} minutes")