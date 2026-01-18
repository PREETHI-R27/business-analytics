#!/usr/bin/env python
# coding: utf-8

# # Superstore Sales Analysis

# ## 1. Data Download & Import

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import zipfile

get_ipython().run_line_magic('matplotlib', 'inline')

# Download the dataset from Kaggle
if not os.path.exists('train.csv'):
    os.system('kaggle datasets download -d rohitsahoo/sales-forecasting -p . --unzip')

df = pd.read_csv('train.csv')


# In[ ]:


df.head()


# ## 2. Data Cleaning & Preparation

# In[ ]:


df['Order Date'] = pd.to_datetime(df['Order Date'])
df.drop_duplicates(inplace=True)
# Create Profit Margin calculated field
df['Profit Margin'] = df['Profit'] / df['Sales']


# ## 3. Exploratory Data Analysis (EDA) & Visualizations

# In[ ]:


df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
monthly_sales = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()

plt.figure(figsize=(14, 7))
sns.lineplot(x='Month', y='Sales', hue='Year', data=monthly_sales, marker='o')
plt.title('Monthly Sales Trends')
plt.grid(True)
plt.show()


# In[ ]:


# Heatmap of Profit by Category and Sub-Category
profit_heatmap_data = df.groupby(['Category', 'Sub-Category'])['Profit'].sum().unstack()

plt.figure(figsize=(12, 8))
sns.heatmap(profit_heatmap_data, annot=True, fmt='.0f', cmap='viridis')
plt.title('Profit by Category and Sub-Category')
plt.show()


# In[ ]:


# Bar chart for sales by State (as a substitute for a geographic map)
state_sales = df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(15) # Top 15 states

plt.figure(figsize=(12, 8))
sns.barplot(y=state_sales.index, x=state_sales.values, palette='plasma')
plt.title('Top 15 States by Sales')
plt.xlabel('Total Sales')
plt.ylabel('State')
plt.show()


# ## 4. Business Insights & Recommendations

# - **Sales Trends**: Sales consistently peak in the last quarter of the year. November and December are the strongest months, indicating a strong holiday season impact.
# - **Profitability**: The profit heatmap reveals that while 'Technology' is a high-profit category, certain sub-categories like 'Tables' and 'Bookcases' in the 'Furniture' category are significant loss-makers. Copiers, on the other hand, are extremely profitable.
# - **Geographic Performance**: Sales are heavily concentrated in a few states, with California and New York leading by a large margin. Focusing on these key markets is crucial.
# 
# **Recommendations:**
# - **Discontinue Loss-Making Products**: Investigate the reasons for losses in the 'Tables' and 'Bookcases' sub-categories. If profitability cannot be improved, consider discontinuing these product lines.
# - **Focus on High-Value Regions**: Double down on marketing and sales efforts in top-performing states like California and New York. For underperforming states, consider targeted campaigns to increase market penetration.
# - **Seasonal Promotions**: Capitalize on the end-of-year sales peak with targeted holiday promotions and marketing campaigns, starting as early as October.
