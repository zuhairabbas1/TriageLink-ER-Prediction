"""
TriageLink - Week 3: Feature Engineering
Author: Zuhair Abbas
Purpose: Engineer advanced features using historical data, CTAS, and master dataset
Deliverable: features_v1.csv
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class TriageLinkFeatureEngineer:
    """
    Advanced feature engineering for ER wait time prediction.
    Integrates historical data, CTAS clinical logic, and temporal patterns.
    """
    
    def __init__(self, master_file='triage_hospital_master.csv'):
        """
        Initialize feature engineer.
        
        Args:
            master_file (str): Path to Week 2 master dataset
        """
        self.master_df = pd.read_csv(master_file)
        self.master_df['timestamp'] = pd.to_datetime(self.master_df['timestamp'])
        
        print("=" * 80)
        print("TRIAGELINK - WEEK 3: FEATURE ENGINEERING PIPELINE")
        print("=" * 80)
        print(f"\n✅ Loaded master dataset: {len(self.master_df)} records")
        print(f"   Hospitals: {self.master_df['hospital_id'].nunique()}")
        print(f"   Date range: {self.master_df['timestamp'].min()} to {self.master_df['timestamp'].max()}")
        
    def load_historical_data(self, migueldata_dir='migueldata-main'):
        """
        Load historical wait time data from migueldata repository.
        
        Args:
            migueldata_dir (str): Directory containing JSON files
            
        Returns:
            pd.DataFrame: Historical wait time data
        """
        print(f"\n📊 LOADING HISTORICAL DATA FROM: {migueldata_dir}")
        print("-" * 80)
        
        all_records = []
        json_files = sorted([f for f in os.listdir(migueldata_dir) if f.endswith('.json')])
        
        for i, filename in enumerate(json_files, 1):
            filepath = os.path.join(migueldata_dir, filename)
            
            # Read concatenated JSON objects
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Split by }{ pattern
            json_objects = content.replace('}{', '}\n{').split('\n')
            
            for json_str in json_objects:
                try:
                    record = json.loads(json_str)
                    timestamp = record['timestamp']
                    
                    # Flatten hospital data
                    for hospital, wait_time in record['data'].items():
                        all_records.append({
                            'timestamp': timestamp,
                            'hospital_name': hospital,
                            'wait_time_str': wait_time
                        })
                except:
                    continue
            
            if i % 10 == 0:
                print(f"   Processed {i}/{len(json_files)} files...")
        
        # Create DataFrame
        historical_df = pd.DataFrame(all_records)
        historical_df['timestamp'] = pd.to_datetime(historical_df['timestamp'])
        
        print(f"\n✅ Loaded historical data:")
        print(f"   Total records: {len(historical_df):,}")
        print(f"   Date range: {historical_df['timestamp'].min()} to {historical_df['timestamp'].max()}")
        print(f"   Unique hospitals: {historical_df['hospital_name'].nunique()}")
        
        # Parse wait times
        print(f"\n⚙️  Parsing wait times...")
        historical_df['wait_time_minutes'] = historical_df['wait_time_str'].apply(self._parse_wait_time)
        
        available_count = historical_df['wait_time_minutes'].notna().sum()
        print(f"   ✅ Parsed {available_count:,} / {len(historical_df):,} records ({available_count/len(historical_df)*100:.1f}%)")
        
        self.historical_df = historical_df
        return historical_df
    
    def _parse_wait_time(self, wait_time_str):
        """Parse wait time string to minutes."""
        if pd.isna(wait_time_str) or "Not available" in str(wait_time_str):
            return None
        
        try:
            wait_time_str = str(wait_time_str).lower()
            
            # Handle range format: "2 hr 44 min to4 hr 25 min"
            if " to" in wait_time_str or " to " in wait_time_str:
                parts = wait_time_str.replace("to", " to ").split(" to ")
                min_time = self._extract_minutes(parts[0])
                max_time = self._extract_minutes(parts[1])
                if min_time is not None and max_time is not None:
                    return (min_time + max_time) / 2
                return None
            
            # Standard format: "2 hr 12 min"
            return self._extract_minutes(wait_time_str)
        except:
            return None
    
    def _extract_minutes(self, time_str):
        """Extract total minutes from time string."""
        import re
        try:
            hours = 0
            minutes = 0
            
            # Extract hours
            hr_match = re.search(r'(\d+)\s*hr', time_str)
            if hr_match:
                hours = int(hr_match.group(1))
            
            # Extract minutes
            min_match = re.search(r'(\d+)\s*min', time_str)
            if min_match:
                minutes = int(min_match.group(1))
            
            total_minutes = (hours * 60) + minutes
            return total_minutes if total_minutes > 0 else None
        except:
            return None
    
    def create_rolling_features(self, window_hours=[1, 6, 24, 168]):
        """
        Create rolling average features from historical data.
        
        Args:
            window_hours (list): Window sizes in hours [1h, 6h, 24h, 7days]
            
        Returns:
            pd.DataFrame: Data with rolling features
        """
        print(f"\n⏰ CREATING ROLLING AVERAGE FEATURES")
        print("-" * 80)
        
        # Sort by hospital and timestamp
        df = self.historical_df.copy()
        df = df.sort_values(['hospital_name', 'timestamp'])
        
        # Create rolling features for each hospital
        rolling_features = []
        
        for hospital in df['hospital_name'].unique():
            hospital_df = df[df['hospital_name'] == hospital].copy()
            hospital_df = hospital_df.set_index('timestamp')
            
            for hours in window_hours:
                window = f'{hours}H'
                col_name = f'wait_time_rolling_{hours}h'
                hospital_df[col_name] = hospital_df['wait_time_minutes'].rolling(
                    window=window, min_periods=1
                ).mean()
            
            rolling_features.append(hospital_df.reset_index())
        
        df_with_rolling = pd.concat(rolling_features, ignore_index=True)
        
        print(f"✅ Created rolling features:")
        for hours in window_hours:
            col_name = f'wait_time_rolling_{hours}h'
            print(f"   - {col_name}")
        
        self.historical_df = df_with_rolling
        return df_with_rolling
    
    def create_trend_features(self):
        """
        Create trend indicators (increasing/decreasing wait times).
        
        Returns:
            pd.DataFrame: Data with trend features
        """
        print(f"\n📈 CREATING TREND FEATURES")
        print("-" * 80)
        
        df = self.historical_df.copy()
        df = df.sort_values(['hospital_name', 'timestamp'])
        
        # Calculate trends for each hospital
        trend_features = []
        
        for hospital in df['hospital_name'].unique():
            hospital_df = df[df['hospital_name'] == hospital].copy()
            
            # 1-hour trend (current vs 1 hour ago)
            hospital_df['trend_1h'] = hospital_df['wait_time_minutes'].diff(periods=1)
            
            # 3-hour trend
            hospital_df['trend_3h'] = hospital_df['wait_time_minutes'].diff(periods=3)
            
            # Trend direction (1 = increasing, -1 = decreasing, 0 = stable)
            hospital_df['trend_direction'] = np.sign(hospital_df['trend_1h'])
            
            # Volatility (standard deviation over last 6 records)
            hospital_df['volatility_6h'] = hospital_df['wait_time_minutes'].rolling(
                window=6, min_periods=1
            ).std()
            
            trend_features.append(hospital_df)
        
        df_with_trends = pd.concat(trend_features, ignore_index=True)
        
        print(f"✅ Created trend features:")
        print(f"   - trend_1h (change vs 1 hour ago)")
        print(f"   - trend_3h (change vs 3 hours ago)")
        print(f"   - trend_direction (increasing/decreasing/stable)")
        print(f"   - volatility_6h (wait time stability)")
        
        self.historical_df = df_with_trends
        return df_with_trends
    
    def create_historical_benchmarks(self):
        """
        Create historical benchmark features (vs hospital's historical avg/max/min).
        
        Returns:
            pd.DataFrame: Data with benchmark features
        """
        print(f"\n📊 CREATING HISTORICAL BENCHMARK FEATURES")
        print("-" * 80)
        
        df = self.historical_df.copy()
        
        # Calculate hospital-level statistics
        hospital_stats = df.groupby('hospital_name')['wait_time_minutes'].agg([
            ('historical_mean', 'mean'),
            ('historical_median', 'median'),
            ('historical_std', 'std'),
            ('historical_min', 'min'),
            ('historical_max', 'max'),
            ('historical_25th', lambda x: x.quantile(0.25)),
            ('historical_75th', lambda x: x.quantile(0.75))
        ]).reset_index()
        
        # Merge back to main dataframe
        df = df.merge(hospital_stats, on='hospital_name', how='left')
        
        # Calculate relative metrics
        df['wait_time_vs_avg'] = df['wait_time_minutes'] - df['historical_mean']
        df['wait_time_pct_of_max'] = (df['wait_time_minutes'] / df['historical_max']) * 100
        df['is_above_75th_percentile'] = df['wait_time_minutes'] > df['historical_75th']
        df['is_below_25th_percentile'] = df['wait_time_minutes'] < df['historical_25th']
        
        print(f"✅ Created benchmark features:")
        print(f"   - historical_mean, median, std, min, max")
        print(f"   - historical_25th, 75th percentiles")
        print(f"   - wait_time_vs_avg (deviation from normal)")
        print(f"   - wait_time_pct_of_max (capacity indicator)")
        print(f"   - is_above_75th_percentile, is_below_25th_percentile")
        
        self.historical_df = df
        return df
    
    def create_temporal_patterns(self):
        """
        Create features based on time patterns (peak hours, weekends, etc.)
        
        Returns:
            pd.DataFrame: Data with temporal pattern features
        """
        print(f"\n🕐 CREATING TEMPORAL PATTERN FEATURES")
        print("-" * 80)
        
        df = self.historical_df.copy()
        
        # Extract time components
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['day_of_month'] = df['timestamp'].dt.day
        df['week_of_year'] = df['timestamp'].dt.isocalendar().week
        df['is_weekend'] = df['day_of_week'].isin([5, 6])
        df['is_weekday'] = ~df['is_weekend']
        
        # Time of day categories
        df['time_of_day'] = pd.cut(df['hour'], 
                                    bins=[0, 6, 12, 18, 24],
                                    labels=['night', 'morning', 'afternoon', 'evening'],
                                    include_lowest=True)
        
        # Peak hours (typically 6pm-midnight in ERs)
        df['is_peak_hour'] = df['hour'].between(18, 23)
        
        # Off-peak hours (midnight-6am)
        df['is_off_peak'] = df['hour'].between(0, 5)
        
        # Business hours
        df['is_business_hours'] = df['hour'].between(9, 17)
        
        print(f"✅ Created temporal pattern features:")
        print(f"   - hour, day_of_week, day_of_month, week_of_year")
        print(f"   - is_weekend, is_weekday")
        print(f"   - time_of_day (night/morning/afternoon/evening)")
        print(f"   - is_peak_hour, is_off_peak, is_business_hours")
        
        self.historical_df = df
        return df
    
    def integrate_ctas_data(self, ctas_file='ctas3_ped_20251203.xlsx'):
        """
        Integrate CTAS pediatric dataset.
        
        Args:
            ctas_file (str): Path to CTAS Excel file
            
        Returns:
            pd.DataFrame: CTAS data with features
        """
        print(f"\n🏥 INTEGRATING CTAS PEDIATRIC DATA")
        print("-" * 80)
        
        # Load CTAS data
        ctas_df = pd.read_excel(ctas_file)
        
        print(f"✅ Loaded CTAS data:")
        print(f"   Conditions: {len(ctas_df)}")
        print(f"   Systems: {ctas_df['system'].nunique()}")
        print(f"   CTAS Level: {ctas_df['ctas_level'].unique()}")
        
        # Create severity score based on modifiers and risk factors
        ctas_df['severity_score'] = 3  # All are CTAS Level 3 (Urgent)
        
        # Adjust severity based on pediatric specialist requirement
        ctas_df.loc[ctas_df['needs_pediatric_specialist'] == True, 'severity_score'] += 1
        
        # Adjust if NOT safe for general ER
        ctas_df.loc[ctas_df['pediatric_safe_to_general_er'] == False, 'severity_score'] += 1
        
        print(f"\n✅ Created CTAS features:")
        print(f"   - severity_score (range: {ctas_df['severity_score'].min()}-{ctas_df['severity_score'].max()})")
        print(f"   - needs_pediatric_specialist")
        print(f"   - pediatric_safe_to_general_er")
        
        self.ctas_df = ctas_df
        return ctas_df
    
    def create_master_feature_set(self, output_file='features_v1.csv'):
        """
        Combine all features into master feature set.
        
        Args:
            output_file (str): Output CSV filename
            
        Returns:
            pd.DataFrame: Complete feature set
        """
        print(f"\n🔗 CREATING MASTER FEATURE SET")
        print("=" * 80)
        
        df = self.historical_df.copy()
        
        # Select final features
        feature_columns = [
            # Identifiers
            'timestamp', 'hospital_name',
            
            # Target variable
            'wait_time_minutes',
            
            # Rolling averages
            'wait_time_rolling_1h', 'wait_time_rolling_6h', 
            'wait_time_rolling_24h', 'wait_time_rolling_168h',
            
            # Trends
            'trend_1h', 'trend_3h', 'trend_direction', 'volatility_6h',
            
            # Historical benchmarks
            'historical_mean', 'historical_median', 'historical_std',
            'historical_min', 'historical_max',
            'wait_time_vs_avg', 'wait_time_pct_of_max',
            'is_above_75th_percentile', 'is_below_25th_percentile',
            
            # Temporal patterns
            'hour', 'day_of_week', 'is_weekend', 'is_weekday',
            'is_peak_hour', 'is_off_peak', 'is_business_hours'
        ]
        
        # Keep only available columns
        available_features = [col for col in feature_columns if col in df.columns]
        df_features = df[available_features].copy()
        
        # Remove rows with NaN target
        df_features = df_features.dropna(subset=['wait_time_minutes'])
        
        # Save to CSV
        df_features.to_csv(output_file, index=False)
        
        print(f"\n💾 Saved feature set: {output_file}")
        print(f"   Rows: {len(df_features):,}")
        print(f"   Features: {len(available_features)}")
        print(f"   Date range: {df_features['timestamp'].min()} to {df_features['timestamp'].max()}")
        
        print(f"\n📊 FEATURE SUMMARY:")
        print(f"   Rolling features: 4")
        print(f"   Trend features: 4")
        print(f"   Benchmark features: 9")
        print(f"   Temporal features: 7")
        print(f"   TOTAL: {len(available_features)} features")
        
        self.features_df = df_features
        return df_features
    
    def run_full_pipeline(self, migueldata_dir, ctas_file, output_file='features_v1.csv'):
        """
        Run complete feature engineering pipeline.
        
        Args:
            migueldata_dir (str): Path to migueldata directory
            ctas_file (str): Path to CTAS file
            output_file (str): Output filename
            
        Returns:
            pd.DataFrame: Complete feature set
        """
        # Step 1: Load historical data
        self.load_historical_data(migueldata_dir)
        
        # Step 2: Create rolling features
        self.create_rolling_features()
        
        # Step 3: Create trend features
        self.create_trend_features()
        
        # Step 4: Create historical benchmarks
        self.create_historical_benchmarks()
        
        # Step 5: Create temporal patterns
        self.create_temporal_patterns()
        
        # Step 6: Integrate CTAS data
        self.integrate_ctas_data(ctas_file)
        
        # Step 7: Create master feature set
        features_df = self.create_master_feature_set(output_file)
        
        print("\n" + "=" * 80)
        print("✅ WEEK 3 FEATURE ENGINEERING COMPLETE!")
        print("=" * 80)
        print(f"\n📁 Output: {output_file}")
        print(f"📊 Ready for Week 4: ML Model Development")
        
        return features_df


# Example usage
if __name__ == "__main__":
    # Initialize
    engineer = TriageLinkFeatureEngineer('triage_hospital_master.csv')
    
    # Run full pipeline
    features_df = engineer.run_full_pipeline(
        migueldata_dir='migueldata-main',
        ctas_file='ctas3_ped_20251203.xlsx',
        output_file='features_v1.csv'
    )
    
    print("\n✅ Feature engineering complete!")
    print(f"   Output file: features_v1.csv")
    print(f"   Total records: {len(features_df):,}")
    print(f"   Features: {features_df.shape[1]}")