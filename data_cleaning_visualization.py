"""
Data Cleaning & Visualization Project
======================================
Retail Sales Dataset — 2024
- Handles missing values, outliers, and duplicates
- Uses Pandas, Matplotlib, Seaborn
- Generates visual reports of key findings
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
# STEP 1: Generate Sample Dataset
# ─────────────────────────────────────────
print("=" * 55)
print("  DATA CLEANING & VISUALIZATION PROJECT")
print("=" * 55)

np.random.seed(42)
n = 500

categories = ['Electronics', 'Clothing', 'Food & Beverage', 'Home & Garden', 'Sports']
regions    = ['North', 'South', 'East', 'West', 'Central']

data = {
    'order_id':       range(1001, 1001 + n),
    'date':           np.random.choice(pd.date_range('2024-01-01', '2024-12-31'), n),
    'category':       np.random.choice(categories, n, p=[0.25, 0.2, 0.2, 0.2, 0.15]),
    'region':         np.random.choice(regions, n),
    'sales':          np.random.lognormal(5, 0.8, n).round(2),
    'quantity':       np.random.randint(1, 15, n),
    'discount':       np.random.choice([0, 0.05, 0.1, 0.15, 0.2], n, p=[0.5, 0.2, 0.15, 0.1, 0.05]),
    'customer_rating':np.random.choice([1, 2, 3, 4, 5], n, p=[0.05, 0.1, 0.2, 0.35, 0.3]),
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Inject issues
df.loc[np.random.choice(df.index, 30), 'customer_rating'] = np.nan
df.loc[np.random.choice(df.index, 15), 'discount']        = np.nan
df = pd.concat([df, df.sample(20)], ignore_index=True)   # duplicates
df.loc[np.random.choice(df.index, 5),  'sales']           = np.random.uniform(5000, 10000, 5)  # outliers

print(f"\n[RAW DATASET]")
print(f"  Rows          : {len(df)}")
print(f"  Columns       : {df.shape[1]}")
print(f"  Missing values: {df.isnull().sum().sum()}")
print(f"  Duplicates    : {df.duplicated(subset=['order_id']).sum()}")


# ─────────────────────────────────────────
# STEP 2: Data Cleaning
# ─────────────────────────────────────────
print("\n[CLEANING STEPS]")

# 2a. Remove duplicates
before = len(df)
df_clean = df.drop_duplicates(subset=['order_id'])
print(f"  Duplicates removed     : {before - len(df_clean)}")

# 2b. Fill missing values
df_clean['customer_rating'] = df_clean['customer_rating'].fillna(
    df_clean['customer_rating'].median()
)
df_clean['discount'] = df_clean['discount'].fillna(0)
print(f"  Missing values fixed   : {df.isnull().sum().sum()}")

# 2c. Remove outliers (IQR / quantile method)
q_hi = df_clean['sales'].quantile(0.97)
outliers = (df_clean['sales'] > q_hi).sum()
df_clean = df_clean[df_clean['sales'] <= q_hi].copy()
print(f"  Outliers removed       : {outliers}")

# 2d. Feature engineering
df_clean['month']      = df_clean['date'].dt.strftime('%b')
df_clean['month_num']  = df_clean['date'].dt.month
df_clean['profit']     = (df_clean['sales'] * (1 - df_clean['discount'])).round(2)

print(f"\n[CLEAN DATASET]")
print(f"  Rows     : {len(df_clean)}")
print(f"  Missing  : {df_clean.isnull().sum().sum()}")
print(df_clean[['sales', 'discount', 'customer_rating', 'profit']].describe().round(2))


# ─────────────────────────────────────────
# STEP 3: Aggregations
# ─────────────────────────────────────────
monthly  = df_clean.groupby('month_num').agg(
    month=('month', 'first'),
    sales=('sales', 'sum'),
    profit=('profit', 'sum'),
    orders=('order_id', 'count')
).reset_index().sort_values('month_num')

cat_perf = df_clean.groupby('category').agg(
    sales=('sales', 'sum'),
    orders=('order_id', 'count'),
    avg_rating=('customer_rating', 'mean')
).reset_index().sort_values('sales', ascending=False)

reg_perf = df_clean.groupby('region').agg(
    sales=('sales', 'sum'),
    orders=('order_id', 'count')
).reset_index().sort_values('sales', ascending=False)

rating_dist = df_clean['customer_rating'].value_counts().sort_index()


# ─────────────────────────────────────────
# STEP 4: Visualization Dashboard
# ─────────────────────────────────────────
sns.set_theme(style='whitegrid', palette='muted')
COLORS  = ['#6366f1','#3b82f6','#10b981','#f59e0b','#ec4899']
ACCENT  = '#6366f1'

fig = plt.figure(figsize=(16, 14), facecolor='#F8FAFC')
fig.suptitle('Retail Sales Dashboard — 2024', fontsize=18, fontweight='bold',
             y=0.98, color='#1E293B')

gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

# ── 4a. Cleaning summary (text panel) ──────────────────────
ax0 = fig.add_subplot(gs[0, :])
ax0.axis('off')
summary_items = [
    ('Raw rows', '520'), ('Clean rows', str(len(df_clean))),
    ('Duplicates removed', '20'), ('Missing values fixed', '45'),
    ('Outliers removed', str(outliers)),
    ('Total sales', f"${df_clean['sales'].sum():,.0f}"),
    ('Avg rating', f"{df_clean['customer_rating'].mean():.2f} ★"),
]
for i, (label, val) in enumerate(summary_items):
    x = 0.04 + i * 0.135
    ax0.add_patch(plt.Rectangle((x, 0.1), 0.12, 0.8, transform=ax0.transAxes,
                                 facecolor='white', edgecolor='#E2E8F0', lw=1, zorder=2))
    ax0.text(x + 0.06, 0.72, val, transform=ax0.transAxes,
             ha='center', fontsize=14, fontweight='bold', color='#1E293B', zorder=3)
    ax0.text(x + 0.06, 0.28, label, transform=ax0.transAxes,
             ha='center', fontsize=9, color='#64748B', zorder=3)
ax0.set_title('Key Metrics & Cleaning Summary', fontsize=11, loc='left',
               pad=4, color='#64748B')

# ── 4b. Monthly sales trend ─────────────────────────────────
ax1 = fig.add_subplot(gs[1, :])
x = np.arange(len(monthly))
width = 0.4
bars1 = ax1.bar(x - width/2, monthly['sales'],   width, label='Sales',  color='#3b82f6', alpha=0.9)
bars2 = ax1.bar(x + width/2, monthly['profit'],  width, label='Profit', color='#10b981', alpha=0.9)
ax1.set_xticks(x)
ax1.set_xticklabels(monthly['month'], fontsize=10)
ax1.set_title('Monthly Sales vs Profit', fontsize=12, fontweight='bold', color='#1E293B')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'${v/1000:.0f}K'))
ax1.legend(fontsize=10)
ax1.set_facecolor('#F8FAFC')
for bar in bars1: bar.set_linewidth(0)
for bar in bars2: bar.set_linewidth(0)

# ── 4c. Category donut chart ────────────────────────────────
ax2 = fig.add_subplot(gs[2, 0])
wedges, texts, autotexts = ax2.pie(
    cat_perf['sales'], labels=cat_perf['category'],
    autopct='%1.0f%%', colors=COLORS,
    startangle=140, wedgeprops={'linewidth': 2, 'edgecolor': 'white'},
    pctdistance=0.80
)
for t in autotexts: t.set_fontsize(9)
for t in texts:     t.set_fontsize(9)
centre = plt.Circle((0, 0), 0.55, fc='#F8FAFC')
ax2.add_patch(centre)
ax2.set_title('Sales by Category', fontsize=12, fontweight='bold', color='#1E293B')

# ── 4d. Region bar chart ────────────────────────────────────
ax3 = fig.add_subplot(gs[2, 1])
bars = ax3.barh(reg_perf['region'], reg_perf['sales'], color=COLORS, alpha=0.9)
ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'${v/1000:.0f}K'))
ax3.set_title('Sales by Region', fontsize=12, fontweight='bold', color='#1E293B')
ax3.invert_yaxis()
ax3.set_facecolor('#F8FAFC')
for bar in bars: bar.set_linewidth(0)

# ── 4e. Rating distribution ─────────────────────────────────
ax4 = fig.add_subplot(gs[2, 2])
rating_colors = ['#ef4444','#f97316','#f59e0b','#22c55e','#10b981']
bars = ax4.bar(rating_dist.index.astype(int), rating_dist.values,
               color=rating_colors, edgecolor='white', linewidth=1.5)
ax4.set_xlabel('Customer Rating', fontsize=10)
ax4.set_title('Rating Distribution', fontsize=12, fontweight='bold', color='#1E293B')
ax4.set_xticks([1, 2, 3, 4, 5])
ax4.set_xticklabels(['★1','★2','★3','★4','★5'])
ax4.set_facecolor('#F8FAFC')
for bar in bars: bar.set_linewidth(0)

plt.savefig('retail_sales_dashboard.png', dpi=150, bbox_inches='tight',
            facecolor='#F8FAFC')
print("\n[OUTPUT] Saved → retail_sales_dashboard.png")
plt.show()

print("\n[DONE] Project complete!")
