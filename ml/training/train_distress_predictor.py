"""
Distress Score Prediction Model Training
Uses historical data to train XGBoost/LightGBM for predicting future distress scores
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import lightgbm as lgb
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DistressScorePredictionModel:
    """Model for predicting future distress scores"""
    
    def __init__(self, model_type='xgboost'):
        """
        Initialize prediction model
        
        Args:
            model_type: 'xgboost' or 'lightgbm'
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
    
    def prepare_features(self, df):
        """
        Prepare features from historical data
        
        Expected columns:
        - distress_score: current score
        - sentiment_score, voice_stress, behavior_score, threat_score, history_score
        - interaction_count, missed_interactions, avg_response_time
        - days_since_registration, case_type_encoded, district_encoded
        """
        
        # Feature engineering
        features = df[[
            'sentiment_score', 'voice_stress', 'behavior_score',
            'threat_score', 'history_score', 'interaction_count',
            'missed_interactions', 'avg_response_time',
            'days_since_registration'
        ]].copy()
        
        # Add lag features (previous scores)
        for lag in [1, 2, 3, 7]:
            features[f'distress_score_lag_{lag}'] = df['distress_score'].shift(lag)
        
        # Add rolling statistics
        features['distress_score_rolling_mean_7'] = df['distress_score'].rolling(7).mean()
        features['distress_score_rolling_std_7'] = df['distress_score'].rolling(7).std()
        
        # Fill NaN values
        features = features.fillna(0)
        
        self.feature_names = features.columns.tolist()
        
        return features
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """Train the prediction model"""
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        if self.model_type == 'xgboost':
            self.model = xgb.XGBRegressor(
                objective='reg:squarederror',
                max_depth=6,
                learning_rate=0.1,
                n_estimators=100,
                random_state=42
            )
            
            if X_val is not None:
                X_val_scaled = self.scaler.transform(X_val)
                self.model.fit(
                    X_train_scaled, y_train,
                    eval_set=[(X_val_scaled, y_val)],
                    early_stopping_rounds=10,
                    verbose=10
                )
            else:
                self.model.fit(X_train_scaled, y_train)
        
        elif self.model_type == 'lightgbm':
            self.model = lgb.LGBMRegressor(
                objective='regression',
                max_depth=6,
                learning_rate=0.1,
                n_estimators=100,
                random_state=42
            )
            
            if X_val is not None:
                X_val_scaled = self.scaler.transform(X_val)
                self.model.fit(
                    X_train_scaled, y_train,
                    eval_set=[(X_val_scaled, y_val)],
                    early_stopping_rounds=10
                )
            else:
                self.model.fit(X_train_scaled, y_train)
        
        logger.info(f"Model trained using {self.model_type}")
    
    def predict(self, X):
        """Predict distress scores"""
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        y_pred = self.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        metrics = {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2': r2
        }
        
        logger.info(f"Model Evaluation Metrics: {metrics}")
        return metrics
    
    def save_model(self, filepath):
        """Save trained model"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'model_type': self.model_type
        }, filepath)
        logger.info(f"Model saved to {filepath}")
    
    @staticmethod
    def load_model(filepath):
        """Load trained model"""
        data = joblib.load(filepath)
        
        model = DistressScorePredictionModel(model_type=data['model_type'])
        model.model = data['model']
        model.scaler = data['scaler']
        model.feature_names = data['feature_names']
        
        logger.info(f"Model loaded from {filepath}")
        return model


def train_pipeline():
    """
    Complete training pipeline
    
    This would load data from database and train the model
    """
    
    # Placeholder: In production, load from database
    # data = load_training_data_from_db()
    
    # For demonstration:
    logger.info("Training distress score prediction model...")
    
    # Create sample data
    np.random.seed(42)
    n_samples = 1000
    
    data = pd.DataFrame({
        'sentiment_score': np.random.uniform(0, 100, n_samples),
        'voice_stress': np.random.uniform(0, 1, n_samples),
        'behavior_score': np.random.uniform(0, 100, n_samples),
        'threat_score': np.random.uniform(0, 100, n_samples),
        'history_score': np.random.uniform(0, 100, n_samples),
        'interaction_count': np.random.randint(0, 50, n_samples),
        'missed_interactions': np.random.randint(0, 20, n_samples),
        'avg_response_time': np.random.uniform(0, 48, n_samples),
        'days_since_registration': np.random.randint(1, 365, n_samples),
        'distress_score': np.random.uniform(0, 100, n_samples)
    })
    
    # Prepare features
    model = DistressScorePredictionModel(model_type='xgboost')
    X = model.prepare_features(data)
    y = data['distress_score'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42
    )
    
    # Train model
    model.train(X_train, y_train, X_val, y_val)
    
    # Evaluate
    metrics = model.evaluate(X_test, y_test)
    
    # Save model
    model.save_model('./models/distress_score_predictor.pkl')
    
    logger.info("Training pipeline completed successfully!")


if __name__ == "__main__":
    train_pipeline()
