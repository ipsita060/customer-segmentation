# Customer Segmentation using KMeans (RFM Analysis)
# This module provides the run_segmentation function for the Flask app

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def run_segmentation(file):
    """
    Perform RFM segmentation on uploaded customer data.
    
    Args:
        file: CSV file object from Flask request
        
    Returns:
        rfm_data: DataFrame with RFM scores and cluster assignments
        summary: Dictionary with cluster statistics
    """
    
    # Load dataset from uploaded file
    df = pd.read_csv(file)
    
    # Data Cleaning
    df = df.dropna()  # Remove missing values
    
    # Remove cancelled invoices
    df = df[~df['InvoiceNo'].astype(str).str.contains('C')].copy()
    
    # Remove negative quantities
    df = df[df['Quantity'] > 0]
    
    # Create TotalPrice column
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    
    # Convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # RFM Feature Engineering
    reference_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    })
    
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    rfm = rfm.reset_index()
    
    # Feature Scaling
    scaler = StandardScaler()
    
    rfm_scaled = scaler.fit_transform(
        rfm[['Recency', 'Frequency', 'Monetary']]
    )
    
    # Apply KMeans Clustering (using 4 clusters)
    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )
    
    rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)
    
    # PCA for Visualization
    pca = PCA(n_components=2)
    rfm_pca = pca.fit_transform(rfm_scaled)
    
    rfm['PCA1'] = rfm_pca[:, 0]
    rfm['PCA2'] = rfm_pca[:, 1]
    
    # Cluster Analysis
    cluster_summary = rfm.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean()
    
    # Prepare summary data
    summary = cluster_summary.to_dict(orient='index')
    
    # Convert to list of dicts for JSON serialization
    rfm_data = rfm.to_dict(orient='records')
    
    # Convert numpy types to native Python types for JSON serialization
    for record in rfm_data:
        for key, value in record.items():
            if isinstance(value, (np.int64, np.int32)):
                record[key] = int(value)
            elif isinstance(value, (np.float64, np.float32)):
                record[key] = float(value)
    
    # Convert summary values as well
    for cluster, metrics in summary.items():
        for metric, value in metrics.items():
            if isinstance(value, (np.float64, np.float32)):
                summary[cluster][metric] = round(float(value), 2)
    
    return rfm_data, summary

