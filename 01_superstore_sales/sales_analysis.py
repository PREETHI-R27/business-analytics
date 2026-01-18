"""
Superstore Sales Analysis
=========================
Analyze sales performance, profitability, and customer segments
for a fictional retail superstore.

Author: PREETHI R
Project: Business Analytics Portfolio

Dataset: Available from Kaggle - "Superstore Sales" or Maven Analytics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 7)


def load_superstore_data(file_path='train.csv'):
    """Load and perform initial exploration"""
    try:
        print("Loading Superstore dataset...")
        df = pd.read_csv(file_path)
        print(f"✓ Loaded {len(df)} records")
        print(f"\nDataset shape: {df.shape}")
        print(f"\nColumns: {list(df.columns)}")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File not found at {file_path}")
        print("\nTo run this analysis:")
        print("1. Download 'Superstore Sales' dataset from Kaggle")
        print("2. Place the CSV file in the project directory")
        print("3. Run this script again")
        return None


def clean_and_prepare_data(df):
    """Clean and prepare data for analysis"""
    if df is None:
        return None
    
    print("\nCleaning and preparing data...")
    
    # Convert Order Date to datetime
    if 'Order Date' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'])
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Create Profit Margin
    if 'Profit' in df.columns and 'Sales' in df.columns:
        df['Profit Margin'] = df['Profit'] / df['Sales']
    
    # Extract time features
    if 'Order Date' in df.columns:
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.month
        df['Quarter'] = df['Order Date'].dt.quarter
    
    print(f"✓ Data cleaning complete")
    print(f"  Records after cleaning: {len(df)}")
    
    return df


def plot_monthly_sales_trends(df):
    """Plot monthly sales trends"""
    if df is None or 'Year' not in df.columns:
        return
    
    print("\nGenerating monthly sales trends...")
    
    monthly_sales = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
    
    plt.figure(figsize=(14, 7))
    for year in monthly_sales['Year'].unique():
        year_data = monthly_sales[monthly_sales['Year'] == year]
        plt.plot(year_data['Month'], year_data['Sales'], 
                marker='o', linewidth=2, label=f'{year}')
    
    plt.title('Monthly Sales Trends by Year', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Sales ($)', fontsize=12)
    plt.xticks(range(1, 13))
    plt.legend(title='Year', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('monthly_sales_trends.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Monthly sales trends saved as 'monthly_sales_trends.png'")


def plot_profit_heatmap(df):
    """Create heatmap of profit by category and sub-category"""
    if df is None:
        return
    
    if 'Category' not in df.columns or 'Sub-Category' not in df.columns:
        print("⚠️ Category/Sub-Category columns not found")
        return
    
    print("\nGenerating profit heatmap...")
    
    profit_heatmap_data = df.groupby(['Category', 'Sub-Category'])['Profit'].sum().unstack()
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(profit_heatmap_data, annot=True, fmt='.0f', cmap='RdYlGn', 
                center=0, linewidths=1, cbar_kws={'label': 'Profit ($)'})
    plt.title('Profit by Category and Sub-Category', fontsize=16, fontweight='bold')
    plt.xlabel('Sub-Category', fontsize=12)
    plt.ylabel('Category', fontsize=12)
    plt.tight_layout()
    plt.savefig('profit_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Profit heatmap saved as 'profit_heatmap.png'")


def plot_top_states_by_sales(df, top_n=15):
    """Plot top states by sales"""
    if df is None or 'State' not in df.columns:
        return
    
    print(f"\nGenerating top {top_n} states by sales...")
    
    state_sales = df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(top_n)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(y=state_sales.index, x=state_sales.values, palette='viridis')
    plt.title(f'Top {top_n} States by Sales', fontsize=16, fontweight='bold')
    plt.xlabel('Total Sales ($)', fontsize=12)
    plt.ylabel('State', fontsize=12)
    
    # Add values on bars
    for i, v in enumerate(state_sales.values):
        plt.text(v, i, f' ${v:,.0f}', va='center')
    
    plt.tight_layout()
    plt.savefig('top_states_sales.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f"✓ Top states chart saved as 'top_states_sales.png'")


def analyze_category_performance(df):
    """Analyze performance by category"""
    if df is None or 'Category' not in df.columns:
        return
    
    print("\nAnalyzing category performance...")
    
    category_metrics = df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'count'
    }).round(2)
    
    category_metrics.columns = ['Total Sales', 'Total Profit', 'Order Count']
    category_metrics['Profit Margin %'] = (
        (category_metrics['Total Profit'] / category_metrics['Total Sales']) * 100
    ).round(2)
    
    print("\n" + "="*80)
    print("CATEGORY PERFORMANCE METRICS")
    print("="*80)
    print(category_metrics)
    print("="*80 + "\n")
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Sales by category
    category_metrics['Total Sales'].plot(kind='bar', ax=axes[0, 0], color='skyblue')
    axes[0, 0].set_title('Sales by Category', fontweight='bold')
    axes[0, 0].set_ylabel('Sales ($)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Profit by category
    category_metrics['Total Profit'].plot(kind='bar', ax=axes[0, 1], color='lightgreen')
    axes[0, 1].set_title('Profit by Category', fontweight='bold')
    axes[0, 1].set_ylabel('Profit ($)')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Profit margin by category
    category_metrics['Profit Margin %'].plot(kind='bar', ax=axes[1, 0], color='coral')
    axes[1, 0].set_title('Profit Margin by Category', fontweight='bold')
    axes[1, 0].set_ylabel('Profit Margin (%)')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Order count by category
    category_metrics['Order Count'].plot(kind='bar', ax=axes[1, 1], color='gold')
    axes[1, 1].set_title('Order Count by Category', fontweight='bold')
    axes[1, 1].set_ylabel('Number of Orders')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('category_performance.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Category performance chart saved as 'category_performance.png'")
    
    return category_metrics


def calculate_key_metrics(df):
    """Calculate and display key business metrics"""
    if df is None:
        return
    
    print("\n" + "="*80)
    print("KEY BUSINESS METRICS")
    print("="*80)
    
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order ID'].nunique() if 'Order ID' in df.columns else len(df)
    avg_order_value = total_sales / total_orders
    overall_profit_margin = (total_profit / total_sales) * 100
    
    print(f"Total Sales:           ${total_sales:,.2f}")
    print(f"Total Profit:          ${total_profit:,.2f}")
    print(f"Total Orders:          {total_orders:,}")
    print(f"Average Order Value:   ${avg_order_value:,.2f}")
    print(f"Overall Profit Margin: {overall_profit_margin:.2f}%")
    
    if 'Customer ID' in df.columns:
        unique_customers = df['Customer ID'].nunique()
        print(f"Unique Customers:      {unique_customers:,}")
    
    print("="*80 + "\n")


def generate_business_insights(df):
    """Generate business insights and recommendations"""
    if df is None:
        return
    
    print("\n" + "="*80)
    print("BUSINESS INSIGHTS & RECOMMENDATIONS")
    print("="*80 + "\n")
    
    insights = []
    
    # Sales Trends
    if 'Month' in df.columns:
        monthly_avg = df.groupby('Month')['Sales'].mean()
        peak_month = monthly_avg.idxmax()
        insights.append(f"📊 SALES TRENDS:\n   Peak sales occur in month {peak_month}. "
                       "Consider increasing inventory and marketing during Q4.")
    
    # Profitability
    if 'Sub-Category' in df.columns and 'Profit' in df.columns:
        subcat_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values()
        loss_makers = subcat_profit[subcat_profit < 0]
        if len(loss_makers) > 0:
            insights.append(f"\n💰 PROFITABILITY:\n   Loss-making sub-categories identified: "
                           f"{', '.join(loss_makers.index.tolist())}.\n   "
                           "Recommendation: Review pricing strategy or consider discontinuation.")
    
    # Geographic Performance
    if 'State' in df.columns:
        top_state = df.groupby('State')['Sales'].sum().idxmax()
        insights.append(f"\n🗺️  GEOGRAPHIC PERFORMANCE:\n   Top performing state: {top_state}.\n   "
                       "Recommendation: Focus marketing efforts on high-performing regions.")
    
    for insight in insights:
        print(insight)
    
    print("\n" + "="*80 + "\n")


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("SUPERSTORE SALES ANALYSIS")
    print("="*80 + "\n")
    
    # Step 1: Load data
    df = load_superstore_data()
    
    if df is None:
        return
    
    # Step 2: Clean and prepare
    df = clean_and_prepare_data(df)
    
    # Step 3: Calculate key metrics
    calculate_key_metrics(df)
    
    # Step 4: Visualizations
    plot_monthly_sales_trends(df)
    plot_profit_heatmap(df)
    plot_top_states_by_sales(df)
    category_metrics = analyze_category_performance(df)
    
    # Step 5: Generate insights
    generate_business_insights(df)
    
    print("="*80)
    print("ANALYSIS COMPLETE")
    print("="*80 + "\n")
    
    print("📊 Generated Files:")
    print("  - monthly_sales_trends.png")
    print("  - profit_heatmap.png")
    print("  - top_states_sales.png")
    print("  - category_performance.png")
    print("\n✅ Superstore sales analysis completed successfully!")


if __name__ == "__main__":
    main()
