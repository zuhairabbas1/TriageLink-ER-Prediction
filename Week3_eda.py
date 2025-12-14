"""
TriageLink - Week 3: Exploratory Data Analysis (EDA)
Author: Zuhair Abbas
Purpose: Analyze feature distributions and patterns
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

print("=" * 80)
print("TRIAGELINK - WEEK 3: EXPLORATORY DATA ANALYSIS")
print("=" * 80)

# Load features
df = pd.read_csv('features_v1.csv', parse_dates=['timestamp'])

print(f"\n📊 DATASET OVERVIEW")
print(f"Total records: {len(df):,}")
print(f"Features: {df.shape[1]}")
print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"Hospitals: {df['hospital_name'].nunique()}")

print(f"\n\n📈 WAIT TIME STATISTICS")
print("=" * 80)
print(df['wait_time_minutes'].describe())

print(f"\n\n🏥 TOP 10 HOSPITALS BY AVERAGE WAIT TIME")
print("=" * 80)
top_hospitals = df.groupby('hospital_name')['wait_time_minutes'].mean().sort_values(ascending=False).head(10)
for i, (hospital, avg_wait) in enumerate(top_hospitals.items(), 1):
    print(f"{i:2d}. {hospital[:50]:<50s} {avg_wait:6.1f} min ({avg_wait/60:.1f} hrs)")

print(f"\n\n⏰ AVERAGE WAIT TIME BY HOUR OF DAY")
print("=" * 80)
hourly_avg = df.groupby('hour')['wait_time_minutes'].mean().sort_values(ascending=False)
for hour in range(24):
    if hour in hourly_avg.index:
        wait = hourly_avg[hour]
        bar = '█' * int(wait / 10)
        print(f"{hour:02d}:00  {wait:6.1f} min  {bar}")

print(f"\n\n📅 AVERAGE WAIT TIME BY DAY OF WEEK")
print("=" * 80)
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_avg = df.groupby('day_of_week')['wait_time_minutes'].mean()
for day_num, day_name in enumerate(days):
    if day_num in daily_avg.index:
        wait = daily_avg[day_num]
        bar = '█' * int(wait / 10)
        print(f"{day_name:<12s} {wait:6.1f} min  {bar}")

print(f"\n\n🔥 PEAK vs OFF-PEAK HOURS")
print("=" * 80)
peak_avg = df[df['is_peak_hour']]['wait_time_minutes'].mean()
off_peak_avg = df[df['is_off_peak']]['wait_time_minutes'].mean()
print(f"Peak hours (6pm-midnight):    {peak_avg:6.1f} min")
print(f"Off-peak (midnight-6am):       {off_peak_avg:6.1f} min")
print(f"Difference:                     {peak_avg - off_peak_avg:6.1f} min ({((peak_avg/off_peak_avg)-1)*100:.1f}% higher)")

print(f"\n\n📊 WEEKEND vs WEEKDAY")
print("=" * 80)
weekend_avg = df[df['is_weekend']]['wait_time_minutes'].mean()
weekday_avg = df[df['is_weekday']]['wait_time_minutes'].mean()
print(f"Weekend:    {weekend_avg:6.1f} min")
print(f"Weekday:    {weekday_avg:6.1f} min")
print(f"Difference: {weekend_avg - weekday_avg:6.1f} min")

print(f"\n\n📉 TREND ANALYSIS")
print("=" * 80)
increasing = (df['trend_direction'] == 1).sum()
decreasing = (df['trend_direction'] == -1).sum()
stable = (df['trend_direction'] == 0).sum()
total_with_trend = increasing + decreasing + stable
print(f"Increasing wait times: {increasing:,} ({increasing/total_with_trend*100:.1f}%)")
print(f"Decreasing wait times: {decreasing:,} ({decreasing/total_with_trend*100:.1f}%)")
print(f"Stable wait times:     {stable:,} ({stable/total_with_trend*100:.1f}%)")

print(f"\n\n📊 ROLLING AVERAGE INSIGHTS")
print("=" * 80)
print(f"1-hour rolling avg:   mean={df['wait_time_rolling_1h'].mean():.1f} min")
print(f"6-hour rolling avg:   mean={df['wait_time_rolling_6h'].mean():.1f} min")
print(f"24-hour rolling avg:  mean={df['wait_time_rolling_24h'].mean():.1f} min")
print(f"7-day rolling avg:    mean={df['wait_time_rolling_168h'].mean():.1f} min")

print(f"\n\n🎯 CORRELATION WITH WAIT TIME (Top 10)")
print("=" * 80)
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlations = df[numeric_cols].corr()['wait_time_minutes'].sort_values(ascending=False)
for i, (feature, corr) in enumerate(list(correlations.items())[1:11], 1):
    bar = '█' * int(abs(corr) * 20)
    print(f"{i:2d}. {feature[:30]:<30s} {corr:6.3f}  {bar}")

print(f"\n\n✅ MISSING VALUES")
print("=" * 80)
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({'Missing': missing, 'Percentage': missing_pct})
missing_df = missing_df[missing_df['Missing'] > 0].sort_values('Missing', ascending=False)
if len(missing_df) > 0:
    print(missing_df)
else:
    print("No missing values!")

print(f"\n\n" + "=" * 80)
print(f"✅ EDA COMPLETE")
print(f"=" * 80)
print(f"\n📁 Key insights saved in this report")
print(f"📊 Ready for Week 4: ML Model Development")