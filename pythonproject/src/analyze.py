import pandas as pd
from sklearn.ensemble import IsolationForest

def dataanalysis(df):
    """Analyze data using Isolation Forest for anomaly detection."""
    
    df_values = df[["co2_ppm", "o2_percentage", "humidity"]].values
    
    # Train Isolation Forest
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    df['Anomaly'] = iso_forest.fit_predict(df_values)
    
    print(df)
    