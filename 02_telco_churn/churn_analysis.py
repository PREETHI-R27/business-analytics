"""
Telco Customer Churn Analysis
==============================
Predict and analyze customer churn in a telecommunications company.

Author: PREETHI R
Project: Business Analytics Portfolio
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

def load_churn_data(file_path='WA_Fn-UseC_-Telco-Customer-Churn.csv'):
    """Load and explore churn dataset"""
    try:
        print("Loading Telco Churn dataset...")
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} customer records")
        return df
    except FileNotFoundError:
        print(f"File not found. Download from Kaggle: Telco Customer Churn")
        return None

def clean_data(df):
    """Clean and preprocess data"""
    if df is None:
        return None
    
    print("\nCleaning data...")
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(inplace=True)
    df['Churn'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
    print("Data cleaning complete")
    return df

def visualize_churn(df):
    """Create churn visualizations"""
    if df is None:
        return
    
    print("\nGenerating visualizations...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Churn rate
    df['Churn'].value_counts().plot(kind='bar', ax=axes[0, 0], color=['green', 'red'])
    axes[0, 0].set_title('Churn Distribution')
    axes[0, 0].set_xticklabels(['Retained', 'Churned'], rotation=0)
    
    # Tenure by churn
    df.boxplot(column='tenure', by='Churn', ax=axes[0, 1])
    axes[0, 1].set_title('Tenure by Churn Status')
    
    # Monthly charges by churn
    df.boxplot(column='MonthlyCharges', by='Churn', ax=axes[1, 0])
    axes[1, 0].set_title('Monthly Charges by Churn')
    
    # Churn by contract type
    if 'Contract' in df.columns:
        pd.crosstab(df['Contract'], df['Churn'], normalize='index').plot(
            kind='bar', stacked=True, ax=axes[1, 1], color=['green', 'red'])
        axes[1, 1].set_title('Churn Rate by Contract Type')
    
    plt.tight_layout()
    plt.savefig('churn_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Visualizations saved")

def train_churn_model(df):
    """Train logistic regression model"""
    if df is None:
        return None
    
    print("\nTraining churn prediction model...")
    
    df_encoded = pd.get_dummies(df, drop_first=True)
    if 'customerID' in df_encoded.columns:
        df_encoded = df_encoded.drop('customerID', axis=1)
    
    X = df_encoded.drop('Churn', axis=1)
    y = df_encoded['Churn']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return model, X_test, y_test, y_pred

def main():
    print("\n" + "="*80)
    print("TELCO CUSTOMER CHURN ANALYSIS")
    print("="*80 + "\n")
    
    df = load_churn_data()
    if df is None:
        return
    
    df = clean_data(df)
    visualize_churn(df)
    model, X_test, y_test, y_pred = train_churn_model(df)
    
    print("\nAnalysis completed successfully!")

if __name__ == "__main__":
    main()
