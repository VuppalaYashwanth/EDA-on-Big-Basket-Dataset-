# BigBasket Sales & Pricing Analysis

A comprehensive retail analytics project analyzing sales patterns, pricing strategies, and discount effectiveness using SQL, Python, Excel, and data visualization libraries.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![SQL](https://img.shields.io/badge/SQL-MySQL-orange.svg)
![Pandas](https://img.shields.io/badge/Pandas-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📊 Project Overview

This project demonstrates end-to-end retail analytics capabilities by analyzing a dataset of 41,748 transactions across 649 products from BigBasket, covering a 6-month period (July-December 2024). The analysis provides actionable insights into category performance, discount strategies, and regional sales distribution.

### Key Highlights
- ✅ Analyzed **₹14.4M+ in revenue** across 8 product categories
- ✅ Processed 41,748 transactions with complex SQL queries
- ✅ Generated 7 professional visualizations using Matplotlib & Seaborn
- ✅ Created interactive Excel dashboard with multiple worksheets
- ✅ Delivered stakeholder-ready performance report

## 🎯 Business Questions Answered

1. Which product categories generate the highest revenue?
2. What is the impact of discounts on sales volume and revenue?
3. How do monthly sales trends inform inventory planning?
4. Which products are top performers by revenue?
5. How does sales performance vary across regions?
6. What is the optimal pricing strategy for different product categories?
7. What correlations exist between price, discounts, and sales?

## 📁 Project Structure

```
bigbasket_analysis/
│
├── generate_bigbasket_data.py    # Dataset generation script
├── products.csv                  # Product master data (649 products)
├── transactions.csv              # Transaction records (41,748 records)
│
├── sql_queries.sql               # 12 complex SQL queries
├── analysis.py                   # Python analysis script
├── create_excel_dashboard.py     # Excel dashboard generator
│
├── BigBasket_Sales_Dashboard.xlsx # Interactive Excel dashboard
├── STAKEHOLDER_REPORT.md         # Comprehensive stakeholder report
│
└── Visualizations/
    ├── category_analysis.png
    ├── monthly_trends.png
    ├── discount_impact.png
    ├── top_products.png
    ├── regional_performance.png
    ├── price_analysis.png
    └── correlation_heatmap.png
```

## 🛠️ Technologies Used

### Programming & Querying
- **Python 3.8+** - Data processing and analysis
- **SQL (MySQL/PostgreSQL)** - Data aggregation and complex joins
- **Pandas** - Data manipulation and transformation
- **NumPy** - Numerical computations

### Visualization
- **Matplotlib** - Statistical visualizations
- **Seaborn** - Advanced data visualization

### Reporting
- **Excel (OpenPyXL)** - Interactive dashboards
- **Markdown** - Documentation and reporting

## 📈 Key Findings

### 1. Category Performance
- **Cleaning & Household** leads with ₹3.42M (23.6% of revenue)
- **Beauty & Hygiene** follows with ₹3.08M (21.3% of revenue)
- **Fruits & Vegetables** has highest order volume but lower AOV

### 2. Discount Strategy Impact
| Discount Range | Revenue/Transaction | Impact |
|----------------|---------------------|--------|
| No Discount | ₹323.95 | Baseline |
| 1-10% | ₹326.05 | +0.6% |
| 11-20% | ₹363.47 | +12.2% |
| 20%+ | ₹447.82 | +38.2% |

**Insight:** Higher discounts significantly increase order value, with 20%+ discounts driving 38% higher revenue per transaction.

### 3. Monthly Trends
- Peak revenue in **August 2024** (₹2.65M)
- Stable AOV around ₹345 across all months
- Q4 shows slight decline in transaction volume

### 4. Regional Distribution
- Balanced performance across all regions (20% ±0.5%)
- Central region slightly underperforming at 19.68%
- West region leads with ₹2.91M revenue

### 5. Price Point Analysis
- **₹200-500 range** drives 53.8% of total revenue
- Products under ₹100 account for 2.37 units per transaction (impulse buys)
- Premium products (₹200+) maintain strong margins

## 🔍 SQL Analysis

The project includes 12 comprehensive SQL queries covering:

1. **Category-wise Sales Analysis** - Revenue, units sold, and discount rates by category
2. **Monthly Sales Trends** - Month-over-month performance tracking
3. **Top Products** - Best sellers by revenue with complete metrics
4. **Discount Impact** - Sales volume analysis across discount brackets
5. **Regional Performance** - Geographic revenue distribution
6. **Brand Comparison** - Brand performance benchmarking
7. **Sub-category Deep Dive** - Granular category analysis
8. **Weekly Trends** - Week-over-week performance
9. **Price Point Analysis** - Revenue by price ranges
10. **High-value Transactions** - Premium customer behavior
11. **Rating vs Sales Correlation** - Product rating impact
12. **Pareto Analysis** - 80/20 revenue contribution

### Example Query: Category-wise Sales
```sql
SELECT 
    p.category,
    COUNT(DISTINCT t.transaction_id) AS total_orders,
    SUM(t.quantity) AS units_sold,
    SUM(t.total_amount) AS total_revenue,
    ROUND(AVG(t.total_amount), 2) AS avg_order_value,
    ROUND(SUM(t.discount_amount) / SUM(t.total_amount) * 100, 2) AS avg_discount_rate
FROM transactions t
INNER JOIN products p ON t.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
```

## 📊 Visualizations

### 1. Category Analysis (4 charts)
- Revenue by category (horizontal bar chart)
- Units sold comparison
- Average discount rates
- Revenue share (pie chart)

### 2. Monthly Trends (2 charts)
- Revenue trend line with markers
- Transactions vs Average Order Value (dual-axis)

### 3. Discount Impact (2 charts)
- Units sold by discount bracket
- Revenue per transaction comparison

### 4. Top Products
- Top 15 products ranked by revenue (horizontal bar chart)

### 5. Regional Performance (2 charts)
- Revenue by region (bar chart)
- Regional revenue distribution (pie chart)

### 6. Price Analysis
- Revenue distribution across price ranges

### 7. Correlation Heatmap
- Correlation matrix showing relationships between metrics

## 📋 Excel Dashboard

The interactive Excel dashboard includes 6 worksheets:

1. **Executive Summary** - KPI dashboard with key metrics
2. **Category Analysis** - Detailed category performance
3. **Monthly Trends** - Month-by-month breakdown
4. **Discount Analysis** - Discount strategy effectiveness
5. **Top Products** - Top 20 revenue-generating products
6. **Regional Performance** - Geographic sales distribution

### Features:
- Professional formatting with color-coded headers
- Auto-sized columns for readability
- Sortable data tables
- Summary statistics
- Clean, stakeholder-ready presentation

## 🚀 How to Run

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### Step 1: Generate Dataset
```bash
python generate_bigbasket_data.py
```
**Output:** Creates `products.csv` and `transactions.csv`

### Step 2: Run Python Analysis
```bash
python analysis.py
```
**Output:** 
- Console output with statistical summaries
- 7 PNG visualization files

### Step 3: Create Excel Dashboard
```bash
python create_excel_dashboard.py
```
**Output:** `BigBasket_Sales_Dashboard.xlsx`

### Step 4: Execute SQL Queries (Optional)
1. Import `products.csv` and `transactions.csv` into your SQL database
2. Run queries from `sql_queries.sql`
3. Validate results against Python analysis

## 💡 Business Recommendations

Based on the analysis, key recommendations include:

### Immediate Actions
1. **Optimize Inventory** - Ensure 100% availability for top 50 products
2. **Promotional Strategy** - Implement 15-20% targeted discounts in Q1
3. **Regional Focus** - Launch marketing campaign in Central region

### Medium-Term
1. **Customer Segmentation** - Develop personalized discount strategies
2. **Product Expansion** - Increase premium offerings in Beauty & Hygiene
3. **Bundle Pricing** - Create bundles to increase basket size by 12-15%

### Long-Term
1. **Market Expansion** - Target 10% growth in underperforming categories
2. **Technology** - Implement predictive analytics for demand forecasting
3. **Customer Experience** - Enhance product discovery with AI recommendations

## 📖 Skills Demonstrated

### Technical Skills
- ✅ SQL (JOINs, aggregations, CTEs, window functions)
- ✅ Python (Pandas, NumPy, data manipulation)
- ✅ Data Visualization (Matplotlib, Seaborn)
- ✅ Excel (OpenPyXL, dashboard creation)
- ✅ Statistical Analysis

### Business Skills
- ✅ Retail Analytics
- ✅ Pricing Strategy Analysis
- ✅ Performance Reporting
- ✅ Stakeholder Communication
- ✅ Data-Driven Decision Making

### Soft Skills
- ✅ Problem Solving
- ✅ Critical Thinking
- ✅ Attention to Detail
- ✅ Documentation
- ✅ Presentation Skills

## 📊 Dataset Details

### Products Table (649 records)
| Column | Type | Description |
|--------|------|-------------|
| product_id | Integer | Unique product identifier |
| product_name | String | Product name |
| category | String | Main category (8 categories) |
| sub_category | String | Sub-category grouping |
| brand | String | Product brand |
| mrp | Float | Maximum retail price |
| sale_price | Float | Actual selling price |
| discount_percent | Integer | Discount percentage |
| rating | Float | Product rating (3.0-4.9) |
| stock_qty | Integer | Current stock quantity |

### Transactions Table (41,748 records)
| Column | Type | Description |
|--------|------|-------------|
| transaction_id | Integer | Unique transaction ID |
| date | Date | Transaction date |
| product_id | Integer | Product purchased |
| quantity | Integer | Units purchased |
| unit_price | Float | Price per unit |
| total_amount | Float | Total transaction value |
| discount_amount | Float | Total discount given |
| customer_id | String | Customer identifier |
| region | String | Geographic region |

## 📝 Sample Output

### Console Output from analysis.py
```
Loading datasets...
Merging datasets...

Dataset Shape: (41748, 20)
Date Range: 2024-07-01 to 2024-12-31
Total Transactions: 41,748
Total Products: 649
Total Revenue: ₹14,485,425.79

============================================================
1. CATEGORY-WISE SALES ANALYSIS
============================================================
                          Orders  Units_Sold     Revenue   Discount
category                                                            
Cleaning & Household        5141       11363  3419647.62  399701.54
Beauty & Hygiene            5729       12527  3078536.48  341443.68
Bakery, Cakes & Dairy       5361       12680  2031024.82  286396.54
...
```

## 🤝 Contributing

This is a portfolio project, but suggestions for improvements are welcome! Feel free to:
- Open an issue for bugs or questions
- Submit a pull request with enhancements
- Share your own analysis approaches

## 📧 Contact

**Vuppala Yashwanth**  
Email: yashwanthvuppala123@gmail.com  
FOR ANY ENQUIRIES GET IN TOUCH WITH ME THROUGH GMAIL.


## 🙏 Acknowledgments

- Dataset structure inspired by real-world e-commerce patterns
- Analysis techniques based on industry best practices
- Visualization design follows professional business intelligence standards

---

**⭐ If you found this project helpful, please star the repository!**

## 📚 Additional Resources

- [SQL Best Practices](https://www.sqlstyle.guide/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Retail Analytics Guide](https://www.tableau.com/learn/articles/retail-analytics)

---

*Last Updated: February 2026*
