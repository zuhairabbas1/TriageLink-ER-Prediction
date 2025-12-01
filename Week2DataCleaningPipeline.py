"""
TriageLink - Week 2: Data Cleaning & Integration
Author: Zuhair Abbas
Purpose: Clean and merge ER wait time data with hospital attributes
Deliverable: triage_hospital_master.csv
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class TriageLinkDataCleaner:
    """
    Data cleaning and integration pipeline for TriageLink project.
    Merges ER Watch, HowLongWillIWait, and Pediatric Triage datasets.
    """
    
    def __init__(self, hospital_mapping_file='Week2_hospital_name_mapping.csv'):
        """
        Initialize the data cleaner with hospital mapping table.
        
        Args:
            hospital_mapping_file (str): Path to hospital name mapping CSV
        """
        self.hospital_mapping = pd.read_csv(hospital_mapping_file)
        print(f"✅ Loaded hospital mapping: {len(self.hospital_mapping)} hospitals")
    
    def parse_wait_time(self, wait_time_str):
        """
        Parse wait time string into minutes.
        
        Handles formats:
        - "2 hr 12 min" → 132 minutes
        - "1 hr or less to 1 hr 9 min" → 34.5 minutes (average)
        - "Not available" → None
        
        Args:
            wait_time_str (str): Raw wait time string
            
        Returns:
            float or None: Wait time in minutes
        """
        if pd.isna(wait_time_str) or "Not available" in str(wait_time_str):
            return None
        
        wait_time_str = str(wait_time_str).lower()
        
        # Handle range format: "1 hr or less to 1 hr 9 min"
        if " to " in wait_time_str:
            parts = wait_time_str.split(" to ")
            min_time = self._extract_minutes(parts[0])
            max_time = self._extract_minutes(parts[1])
            if min_time is not None and max_time is not None:
                return (min_time + max_time) / 2  # Return average
            return None
        
        # Handle standard format: "2 hr 12 min"
        return self._extract_minutes(wait_time_str)
    
    def _extract_minutes(self, time_str):
        """
        Extract total minutes from time string.
        
        Args:
            time_str (str): Time string like "2 hr 12 min"
            
        Returns:
            float or None: Total minutes
        """
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
        
        except Exception as e:
            return None
    
    def normalize_hospital_name(self, raw_name, source='hlwiw'):
        """
        Normalize hospital name to standard format using mapping table.
        
        Args:
            raw_name (str): Raw hospital name from data source
            source (str): Data source ('er_watch', 'hlwiw', or 'pediatric')
            
        Returns:
            tuple: (hospital_id, standard_name)
        """
        if pd.isna(raw_name):
            return (None, None)
        
        # Map source to column name
        column_mapping = {
            'er_watch': 'er_watch_name',
            'hlwiw': 'hlwiw_name',
            'pediatric': 'pediatric_dataset_name'
        }
        
        source_column = column_mapping.get(source, 'hlwiw_name')
        
        # Find matching hospital
        match = self.hospital_mapping[
            self.hospital_mapping[source_column] == raw_name
        ]
        
        if not match.empty:
            return (match.iloc[0]['hospital_id'], match.iloc[0]['standard_name'])
        
        return (None, raw_name)  # Return original if no match
    
    def load_wait_time_data(self, wait_time_file):
        """
        Load and clean wait time data from Excel file.
        
        Args:
            wait_time_file (str): Path to Excel file with wait times
            
        Returns:
            pd.DataFrame: Cleaned wait time data
        """
        print(f"\n📊 Loading wait time data from: {wait_time_file}")
        
        # Load data
        df = pd.read_excel(wait_time_file)
        print(f"   Loaded {len(df)} records")
        
        # Parse wait times
        df['wait_time_minutes'] = df['Wait Time'].apply(self.parse_wait_time)
        
        # Normalize hospital names
        df[['hospital_id', 'standard_name']] = df['Hospital Name'].apply(
            lambda x: pd.Series(self.normalize_hospital_name(x, 'hlwiw'))
        )
        
        # Add data availability flag
        df['data_available'] = df['wait_time_minutes'].notna()
        
        print(f"   ✅ Parsed wait times: {df['data_available'].sum()} available, {(~df['data_available']).sum()} missing")
        
        return df
    
    def merge_hospital_attributes(self, wait_time_df):
        """
        Merge hospital attributes from mapping table.
        
        Args:
            wait_time_df (pd.DataFrame): Wait time data with hospital IDs
            
        Returns:
            pd.DataFrame: Merged data with hospital attributes
        """
        print(f"\n🔗 Merging hospital attributes...")
        
        # Merge on hospital_id
        merged_df = wait_time_df.merge(
            self.hospital_mapping[['hospital_id', 'region', 'has_pediatric_er', 
                                  'is_trauma_centre', 'tier']],
            on='hospital_id',
            how='left'
        )
        
        print(f"   ✅ Merged {len(merged_df)} records with attributes")
        
        return merged_df
    
    def add_temporal_features(self, df):
        """
        Add temporal features (hour, day_of_week, is_weekend, etc.)
        
        Args:
            df (pd.DataFrame): Data with timestamp column
            
        Returns:
            pd.DataFrame: Data with temporal features
        """
        print(f"\n⏰ Adding temporal features...")
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # Extract temporal features
        df['hour_of_day'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek  # 0=Monday, 6=Sunday
        df['is_weekend'] = df['day_of_week'].isin([5, 6])  # Saturday, Sunday
        df['is_night_shift'] = df['hour_of_day'].between(18, 23) | df['hour_of_day'].between(0, 6)
        df['day_name'] = df['timestamp'].dt.day_name()
        df['month'] = df['timestamp'].dt.month
        df['year'] = df['timestamp'].dt.year
        
        print(f"   ✅ Added 7 temporal features")
        
        return df
    
    def handle_missing_values(self, df, strategy='flag'):
        """
        Handle missing wait time values.
        
        Strategies:
        - 'flag': Keep as None, use data_available flag
        - 'drop': Remove rows with missing values
        - 'mean': Impute with hospital's mean wait time
        - 'forward_fill': Use last known value for that hospital
        
        Args:
            df (pd.DataFrame): Data with potential missing values
            strategy (str): Missing value strategy
            
        Returns:
            pd.DataFrame: Data with handled missing values
        """
        print(f"\n🔧 Handling missing values (strategy: {strategy})...")
        
        missing_count = df['wait_time_minutes'].isna().sum()
        print(f"   Missing values: {missing_count} ({missing_count/len(df)*100:.1f}%)")
        
        if strategy == 'flag':
            # Already have data_available flag, keep as is
            print(f"   ✅ Keeping missing values with flag")
            
        elif strategy == 'drop':
            df = df.dropna(subset=['wait_time_minutes'])
            print(f"   ✅ Dropped {missing_count} rows")
            
        elif strategy == 'mean':
            # Impute with hospital mean
            hospital_means = df.groupby('hospital_id')['wait_time_minutes'].transform('mean')
            df['wait_time_minutes'] = df['wait_time_minutes'].fillna(hospital_means)
            print(f"   ✅ Imputed with hospital means")
            
        elif strategy == 'forward_fill':
            # Forward fill within each hospital
            df = df.sort_values(['hospital_id', 'timestamp'])
            df['wait_time_minutes'] = df.groupby('hospital_id')['wait_time_minutes'].fillna(method='ffill')
            print(f"   ✅ Forward filled within hospitals")
        
        return df
    
    def encode_categorical_features(self, df):
        """
        Encode categorical features for ML.
        
        - One-hot encoding for regions
        - Ordinal encoding for tier (1 > 2)
        - Binary encoding for boolean flags
        
        Args:
            df (pd.DataFrame): Data with categorical features
            
        Returns:
            pd.DataFrame: Data with encoded features
        """
        print(f"\n🔢 Encoding categorical features...")
        
        # One-hot encode regions
        if 'region' in df.columns:
            region_dummies = pd.get_dummies(df['region'], prefix='region', drop_first=False)
            df = pd.concat([df, region_dummies], axis=1)
            print(f"   ✅ One-hot encoded regions: {len(region_dummies.columns)} columns")
        
        # Convert boolean strings to actual booleans
        bool_columns = ['has_pediatric_er', 'is_trauma_centre', 'is_weekend', 'is_night_shift']
        for col in bool_columns:
            if col in df.columns:
                df[col] = df[col].map({'TRUE': True, 'FALSE': False, True: True, False: False})
        
        # Fill tier NaN with 0 (non-pediatric hospitals)
        if 'tier' in df.columns:
            df['tier'] = df['tier'].fillna(0).astype(int)
        
        print(f"   ✅ Encoded categorical features")
        
        return df
    
    def create_master_dataset(self, wait_time_file, output_file='triage_hospital_master.csv',
                            missing_strategy='flag'):
        """
        Main pipeline to create master dataset.
        
        Args:
            wait_time_file (str): Path to wait time Excel file
            output_file (str): Output CSV file name
            missing_strategy (str): Strategy for missing values
            
        Returns:
            pd.DataFrame: Master dataset
        """
        print("="*70)
        print("TRIAGELINK - WEEK 2: DATA CLEANING & INTEGRATION PIPELINE")
        print("="*70)
        
        # Step 1: Load wait time data
        df = self.load_wait_time_data(wait_time_file)
        
        # Step 2: Merge hospital attributes
        df = self.merge_hospital_attributes(df)
        
        # Step 3: Add temporal features
        df = self.add_temporal_features(df)
        
        # Step 4: Handle missing values
        df = self.handle_missing_values(df, strategy=missing_strategy)
        
        # Step 5: Encode categorical features
        df = self.encode_categorical_features(df)
        
        # Step 6: Select and order columns
        master_columns = [
            'hospital_id', 'standard_name', 'region', 'tier',
            'has_pediatric_er', 'is_trauma_centre',
            'timestamp', 'hour_of_day', 'day_of_week', 'is_weekend', 'is_night_shift',
            'wait_time_minutes', 'data_available',
            'day_name', 'month', 'year'
        ]
        
        # Add region dummy columns
        region_cols = [col for col in df.columns if col.startswith('region_')]
        master_columns.extend(region_cols)
        
        # Keep only existing columns
        available_columns = [col for col in master_columns if col in df.columns]
        df_master = df[available_columns].copy()
        
        # Step 7: Save to CSV
        df_master.to_csv(output_file, index=False)
        print(f"\n💾 Saved master dataset: {output_file}")
        print(f"   📊 Shape: {df_master.shape[0]} rows × {df_master.shape[1]} columns")
        
        # Step 8: Summary statistics
        self._print_summary(df_master)
        
        print("\n" + "="*70)
        print("✅ WEEK 2 DATA CLEANING COMPLETE!")
        print("="*70)
        
        return df_master
    
    def _print_summary(self, df):
        """Print summary statistics of master dataset."""
        print(f"\n📈 MASTER DATASET SUMMARY")
        print("-" * 70)
        print(f"Total Records: {len(df)}")
        print(f"Unique Hospitals: {df['hospital_id'].nunique()}")
        print(f"Time Range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        print(f"Data Availability: {df['data_available'].sum()} ({df['data_available'].mean()*100:.1f}%)")
        print(f"\nWait Time Statistics (minutes):")
        print(df['wait_time_minutes'].describe())
        print(f"\nHospitals by Region:")
        if 'region' in df.columns:
            print(df.groupby('region')['hospital_id'].nunique())
        print(f"\nPediatric ERs: {df['has_pediatric_er'].sum() if 'has_pediatric_er' in df.columns else 'N/A'}")
        print(f"Trauma Centres: {df['is_trauma_centre'].sum() if 'is_trauma_centre' in df.columns else 'N/A'}")


# Example usage
if __name__ == "__main__":
    # Initialize cleaner
    cleaner = TriageLinkDataCleaner('Week2_hospital_name_mapping.csv')
    
    # Create master dataset
    # Replace 'demo_hospital_wait_times.xlsx' with your actual data file
    master_df = cleaner.create_master_dataset(
        wait_time_file='demo_hospital_wait_times.xlsx',
        output_file='triage_hospital_master.csv',
        missing_strategy='flag'  # Options: 'flag', 'drop', 'mean', 'forward_fill'
    )
    
    print("\n✅ Master dataset ready for Week 3 feature engineering!")