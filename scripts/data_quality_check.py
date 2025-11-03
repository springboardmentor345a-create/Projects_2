"""
Data Quality Check and Cleaning Script
Performs: Null checks, duplicate removal, outlier detection
"""
import pandas as pd
import numpy as np
import os


def check_and_clean_dataset(filepath):
    """Performs 5-step data quality check on a dataset"""
    print(f"\n{'='*80}")
    print(f"Processing: {os.path.basename(filepath)}")
    print('='*80)
    
    df = pd.read_csv(filepath)
    original_shape = df.shape
    print(f"Original shape: {original_shape}")
    
    changes = False
    
    # Step 1: Check for Null Values
    print("\n[STEP 1] Checking for Null Values...")
    null_counts = df.isnull().sum()
    null_cols = null_counts[null_counts > 0]
    
    if not null_cols.empty:
        print(f"  [FOUND] Found null values in {len(null_cols)} columns:")
        print(f"  {null_cols.to_dict()}")
        # Step 2: Handle Null Values - drop rows with any nulls
        df_before_nulls = len(df)
        df = df.dropna()
        rows_dropped_nulls = df_before_nulls - len(df)
        print(f"  [OK] Dropped {rows_dropped_nulls} rows containing null values.")
        changes = True
    else:
        print("  [OK] No null values found.")
    
    # Step 3: Check for Duplicates
    print("\n[STEP 2] Checking for Duplicates...")
    duplicate_count = df.duplicated().sum()
    
    if duplicate_count > 0:
        print(f"  [FOUND] Found {duplicate_count} duplicate rows.")
        # Step 4: Drop Duplicates
        df_before_dups = len(df)
        df = df.drop_duplicates()
        rows_dropped_dups = df_before_dups - len(df)
        print(f"  [OK] Dropped {rows_dropped_dups} duplicate rows.")
        changes = True
    else:
        print("  [OK] No duplicate rows found.")
    
    # Step 5: Check for Outliers
    print("\n[STEP 3] Checking for Outliers (using IQR method)...")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        outlier_summary = {}
        outlier_rows = set()
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            if not outliers.empty:
                outlier_summary[col] = len(outliers)
                outlier_rows.update(outliers.index.tolist())
        
        if outlier_summary:
            print(f"  [WARNING] Found potential outliers in {len(outlier_summary)} columns:")
            for col, count in outlier_summary.items():
                print(f"     - {col}: {count} outliers")
            print(f"  [INFO] Total unique rows with outliers: {len(outlier_rows)}")
            print(f"  [INFO] Note: Outliers are NOT automatically removed.")
            print(f"     Review contextually before deciding to remove.")
        else:
            print("  [OK] No extreme outliers detected.")
    else:
        print("  [INFO] No numeric columns to check for outliers.")
    
    # Final summary
    final_shape = df.shape
    print(f"\n--- Final Summary ---")
    print(f"Final shape: {final_shape}")
    
    if original_shape != final_shape:
        print(f"\nChanges made. Saving cleaned data...")
        df.to_csv(filepath, index=False)
        return True
    else:
        print("\nNo changes needed for this dataset.")
        return False


def main():
    """Main execution"""
    print("\n" + "="*80)
    print("DATA QUALITY CHECK AND CLEANING")
    print("="*80)
    
    # Define file paths
    files_to_process = [
        'data/final/data_final_match_prediction.csv',
        'data/final/data_final_top_scorer.csv',
        'data/final/data_final_points_tally.csv'
    ]
    
    changes_made = False
    
    for filepath in files_to_process:
        if os.path.exists(filepath):
            if check_and_clean_dataset(filepath):
                changes_made = True
        else:
            print(f"\n[ERROR] File not found: {filepath}")
    
    print("\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80)
    if changes_made:
        print("[OK] Some datasets were cleaned. Changes saved.")
    else:
        print("[OK] No changes needed. All datasets are clean.")
    print("="*80)


if __name__ == '__main__':
    main()

