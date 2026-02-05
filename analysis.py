"""
BigBasket Sales & Pricing Analysis
Python Script for Data Analysis and Visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load data
print("Loading datasets...")
products_df = pd.read_csv('products.csv')
transactions_df = pd.read_csv('transactions.csv')

# Merge datasets
print("Merging datasets...")
df = transactions_df.merge(products_df, on='product_id', how='left')
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M')
df['week'] = df['date'].dt.to_period('W')

print(f"\nDataset Shape: {df.shape}")
print(f"Date Range: {df['date'].min()} to {df['date'].max()}")
print(f"Total Transactions: {df['transaction_id'].nunique():,}")
print(f"Total Products: {df['product_id'].nunique():,}")
print(f"Total Revenue: ₹{df['total_amount'].sum():,.2f}")

# ==========================================
# 1. CATEGORY-WISE SALES ANALYSIS
# ==========================================
print("\n" + "="*60)
print("1. CATEGORY-WISE SALES ANALYSIS")
print("="*60)

category_sales = df.groupby('category').agg({
    'transaction_id': 'nunique',
    'quantity': 'sum',
    'total_amount': 'sum',
    'discount_amount': 'sum'
}).round(2)

category_sales.columns = ['Orders', 'Units_Sold', 'Revenue', 'Discount']
category_sales['Avg_Discount_%'] = (category_sales['Discount'] / (category_sales['Revenue'] + category_sales['Discount']) * 100).round(2)
category_sales = category_sales.sort_values('Revenue', ascending=False)

print(category_sales)

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Category-Wise Sales Performance', fontsize=16, fontweight='bold')

# Revenue by Category
axes[0, 0].barh(category_sales.index, category_sales['Revenue'] / 1000, color='steelblue')
axes[0, 0].set_xlabel('Revenue (₹ Thousands)', fontsize=11)
axes[0, 0].set_title('Total Revenue by Category', fontsize=12, fontweight='bold')
axes[0, 0].grid(axis='x', alpha=0.3)

# Units Sold by Category
axes[0, 1].barh(category_sales.index, category_sales['Units_Sold'], color='coral')
axes[0, 1].set_xlabel('Units Sold', fontsize=11)
axes[0, 1].set_title('Total Units Sold by Category', fontsize=12, fontweight='bold')
axes[0, 1].grid(axis='x', alpha=0.3)

# Average Discount by Category
axes[1, 0].barh(category_sales.index, category_sales['Avg_Discount_%'], color='seagreen')
axes[1, 0].set_xlabel('Average Discount (%)', fontsize=11)
axes[1, 0].set_title('Average Discount Rate by Category', fontsize=12, fontweight='bold')
axes[1, 0].grid(axis='x', alpha=0.3)

# Revenue Share Pie Chart
revenue_share = category_sales['Revenue']
colors = plt.cm.Set3(range(len(revenue_share)))
axes[1, 1].pie(revenue_share, labels=revenue_share.index, autopct='%1.1f%%', 
               colors=colors, startangle=90)
axes[1, 1].set_title('Revenue Share by Category', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('category_analysis.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved: category_analysis.png")

# ==========================================
# 2. MONTHLY SALES TREND
# ==========================================
print("\n" + "="*60)
print("2. MONTHLY SALES TREND")
print("="*60)

monthly_sales = df.groupby('month').agg({
    'transaction_id': 'nunique',
    'quantity': 'sum',
    'total_amount': 'sum',
    'discount_amount': 'sum'
}).reset_index()

monthly_sales.columns = ['Month', 'Transactions', 'Units', 'Revenue', 'Discount']
monthly_sales['Month'] = monthly_sales['Month'].astype(str)
monthly_sales['Avg_Order_Value'] = (monthly_sales['Revenue'] / monthly_sales['Transactions']).round(2)

print(monthly_sales)

# Visualization
fig, axes = plt.subplots(2, 1, figsize=(14, 10))
fig.suptitle('Monthly Sales Trends', fontsize=16, fontweight='bold')

# Revenue Trend
axes[0].plot(monthly_sales['Month'], monthly_sales['Revenue']/1000, 
             marker='o', linewidth=2.5, markersize=8, color='steelblue', label='Revenue')
axes[0].set_ylabel('Revenue (₹ Thousands)', fontsize=11)
axes[0].set_title('Monthly Revenue Trend', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)
axes[0].legend()

# Transactions and AOV
ax2 = axes[1]
ax2.bar(monthly_sales['Month'], monthly_sales['Transactions'], 
        color='lightcoral', alpha=0.7, label='Transactions')
ax2.set_ylabel('Number of Transactions', fontsize=11, color='lightcoral')
ax2.tick_params(axis='y', labelcolor='lightcoral')
ax2.set_xlabel('Month', fontsize=11)

ax3 = ax2.twinx()
ax3.plot(monthly_sales['Month'], monthly_sales['Avg_Order_Value'], 
         marker='D', linewidth=2, markersize=7, color='seagreen', label='Avg Order Value')
ax3.set_ylabel('Average Order Value (₹)', fontsize=11, color='seagreen')
ax3.tick_params(axis='y', labelcolor='seagreen')

axes[1].set_title('Transactions & Average Order Value', fontsize=12, fontweight='bold')
axes[1].legend(loc='upper left')
ax3.legend(loc='upper right')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('monthly_trends.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved: monthly_trends.png")

# ==========================================
# 3. DISCOUNT IMPACT ANALYSIS
# ==========================================
print("\n" + "="*60)
print("3. DISCOUNT IMPACT ANALYSIS")
print("="*60)

# Create discount brackets
df['discount_bracket'] = pd.cut(df['discount_percent'], 
                                 bins=[-1, 0, 10, 20, 100],
                                 labels=['No Discount', '1-10%', '11-20%', '20%+'])

discount_analysis = df.groupby('discount_bracket').agg({
    'transaction_id': 'nunique',
    'quantity': ['sum', 'mean'],
    'total_amount': 'sum'
}).round(2)

discount_analysis.columns = ['Transactions', 'Total_Units', 'Avg_Units_Per_Order', 'Revenue']
discount_analysis['Revenue_Per_Transaction'] = (discount_analysis['Revenue'] / discount_analysis['Transactions']).round(2)

print(discount_analysis)

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Discount Impact on Sales Performance', fontsize=16, fontweight='bold')

# Units Sold by Discount Bracket
axes[0].bar(discount_analysis.index, discount_analysis['Total_Units'], color='skyblue', edgecolor='black')
axes[0].set_ylabel('Total Units Sold', fontsize=11)
axes[0].set_title('Units Sold by Discount Bracket', fontsize=12, fontweight='bold')
axes[0].grid(axis='y', alpha=0.3)

# Revenue per Transaction
axes[1].bar(discount_analysis.index, discount_analysis['Revenue_Per_Transaction'], color='lightgreen', edgecolor='black')
axes[1].set_ylabel('Revenue per Transaction (₹)', fontsize=11)
axes[1].set_title('Avg Revenue per Transaction by Discount', fontsize=12, fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('discount_impact.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved: discount_impact.png")

# ==========================================
# 4. TOP PRODUCTS ANALYSIS
# ==========================================
print("\n" + "="*60)
print("4. TOP 15 PRODUCTS BY REVENUE")
print("="*60)

top_products = df.groupby(['product_name', 'category', 'brand']).agg({
    'quantity': 'sum',
    'total_amount': 'sum',
    'rating': 'first',
    'discount_percent': 'first'
}).round(2)

top_products.columns = ['Units_Sold', 'Revenue', 'Rating', 'Discount_%']
top_products = top_products.sort_values('Revenue', ascending=False).head(15)

print(top_products)

# Visualization
fig, ax = plt.subplots(figsize=(14, 8))
products_plot = top_products.reset_index()
y_pos = range(len(products_plot))

bars = ax.barh(y_pos, products_plot['Revenue']/1000, color='teal', edgecolor='black')
ax.set_yticks(y_pos)
ax.set_yticklabels([f"{row['product_name'][:30]}..." if len(row['product_name']) > 30 
                     else row['product_name'] for _, row in products_plot.iterrows()], fontsize=9)
ax.set_xlabel('Revenue (₹ Thousands)', fontsize=11)
ax.set_title('Top 15 Products by Revenue', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2, 
            f'₹{width:.1f}K', ha='left', va='center', fontsize=8)

plt.tight_layout()
plt.savefig('top_products.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved: top_products.png")

# ==========================================
# 5. REGIONAL PERFORMANCE
# ==========================================
print("\n" + "="*60)
print("5. REGIONAL PERFORMANCE ANALYSIS")
print("="*60)

regional_sales = df.groupby('region').agg({
    'transaction_id': 'nunique',
    'quantity': 'sum',
    'total_amount': 'sum',
    'discount_amount': 'sum'
}).round(2)

regional_sales.columns = ['Orders', 'Units', 'Revenue', 'Discount']
regional_sales['Avg_Order_Value'] = (regional_sales['Revenue'] / regional_sales['Orders']).round(2)
regional_sales['Revenue_Share_%'] = (regional_sales['Revenue'] / regional_sales['Revenue'].sum() * 100).round(2)
regional_sales = regional_sales.sort_values('Revenue', ascending=False)

print(regional_sales)

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Regional Sales Performance', fontsize=16, fontweight='bold')

# Revenue by Region
axes[0].bar(regional_sales.index, regional_sales['Revenue']/1000, color='indianred', edgecolor='black')
axes[0].set_ylabel('Revenue (₹ Thousands)', fontsize=11)
axes[0].set_title('Total Revenue by Region', fontsize=12, fontweight='bold')
axes[0].grid(axis='y', alpha=0.3)

# Revenue Share
colors = plt.cm.Pastel1(range(len(regional_sales)))
axes[1].pie(regional_sales['Revenue'], labels=regional_sales.index, autopct='%1.1f%%',
           colors=colors, startangle=45)
axes[1].set_title('Revenue Distribution by Region', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('regional_performance.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved: regional_performance.png")

# ==========================================
# 6. PRICE POINT ANALYSIS
# ==========================================
print("\n" + "="*60)
print("6. PRICE POINT ANALYSIS")
print("="*60)

df['price_range'] = pd.cut(df['sale_price'], 
                           bins=[0, 50, 100, 200, 500, 10000],
                           labels=['Under ₹50', '₹50-100', '₹100-200', '₹200-500', 'Above ₹500'])

price_analysis = df.groupby('price_range').agg({
    'product_id': 'nunique',
    'quantity': ['sum', 'mean'],
    'total_amount': 'sum'
}).round(2)

price_analysis.columns = ['Products', 'Total_Units', 'Avg_Qty_Per_Order', 'Revenue']
print(price_analysis)

# Visualization
fig, ax = plt.subplots(figsize=(12, 6))
x_pos = range(len(price_analysis))
bars = ax.bar(x_pos, price_analysis['Revenue']/1000, color='mediumpurple', edgecolor='black', alpha=0.7)
ax.set_xticks(x_pos)
ax.set_xticklabels(price_analysis.index, rotation=15, ha='right')
ax.set_ylabel('Revenue (₹ Thousands)', fontsize=11)
ax.set_title('Revenue Distribution by Price Range', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'₹{height:.0f}K', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('price_analysis.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved: price_analysis.png")

# ==========================================
# 7. CORRELATION HEATMAP
# ==========================================
print("\n" + "="*60)
print("7. CORRELATION ANALYSIS")
print("="*60)

# Prepare numerical features for correlation
corr_df = df[['quantity', 'sale_price', 'discount_percent', 'rating', 'total_amount']].corr()

print(corr_df)

# Visualization
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_df, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
ax.set_title('Correlation Matrix: Sales Metrics', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved: correlation_heatmap.png")

# ==========================================
# SUMMARY STATISTICS
# ==========================================
print("\n" + "="*60)
print("OVERALL SUMMARY STATISTICS")
print("="*60)

summary = {
    'Total Revenue': f"₹{df['total_amount'].sum():,.2f}",
    'Total Discount Given': f"₹{df['discount_amount'].sum():,.2f}",
    'Total Transactions': f"{df['transaction_id'].nunique():,}",
    'Total Units Sold': f"{df['quantity'].sum():,}",
    'Average Order Value': f"₹{df.groupby('transaction_id')['total_amount'].sum().mean():.2f}",
    'Average Discount Rate': f"{(df['discount_amount'].sum() / (df['total_amount'].sum() + df['discount_amount'].sum()) * 100):.2f}%",
    'Unique Products Sold': f"{df['product_id'].nunique():,}",
    'Unique Customers': f"{df['customer_id'].nunique():,}",
    'Average Product Rating': f"{products_df['rating'].mean():.2f}"
}

for key, value in summary.items():
    print(f"{key}: {value}")

print("\n" + "="*60)
print("ANALYSIS COMPLETE!")
print("="*60)
print("\nGenerated Files:")
print("- category_analysis.png")
print("- monthly_trends.png")
print("- discount_impact.png")
print("- top_products.png")
print("- regional_performance.png")
print("- price_analysis.png")
print("- correlation_heatmap.png")
