"""
Validate preprocessed data quality
"""
import pandas as pd
import numpy as np
import sys
import os

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def validate_dataset(filepath, dataset_name):
    """Validate a single dataset"""
    print(f"\n{'='*80}")
    print(f"Validating: {dataset_name}")
    print(f"{'='*80}\n")
    
    try:
        df = pd.read_csv(filepath)
        
        # Basic info
        print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Missing values
        missing = df.isnull().sum().sum()
        missing_pct = (missing / (df.shape[0] * df.shape[1])) * 100
        print(f"\nMissing Values: {missing:,} ({missing_pct:.2f}%)")
        
        if missing > 0:
            print("\nColumns with missing values:")
            missing_cols = df.isnull().sum()
            for col, count in missing_cols[missing_cols > 0].items():
                print(f"  - {col}: {count:,} ({count/len(df)*100:.2f}%)")
        
        # Duplicates
        duplicates = df.duplicated().sum()
        print(f"\nDuplicate Rows: {duplicates:,}")
        
        # Data types
        print(f"\nData Types:")
        dtype_counts = df.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            print(f"  - {dtype}: {count} columns")
        
        # Numeric columns stats
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"\nNumeric Columns: {len(numeric_cols)}")
            print(f"  Min values: {df[numeric_cols].min().min():.2f}")
            print(f"  Max values: {df[numeric_cols].max().max():.2f}")
            print(f"  Mean values: {df[numeric_cols].mean().mean():.2f}")
        
        # Categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            print(f"\nCategorical Columns: {len(categorical_cols)}")
            for col in categorical_cols[:5]:  # Show first 5
                unique_count = df[col].nunique()
                print(f"  - {col}: {unique_count} unique values")
        
        # Quality score
        quality_score = 100
        if missing > 0:
            quality_score -= min(missing_pct, 20)
        if duplicates > 0:
            quality_score -= min(duplicates / len(df) * 100, 10)
        
        print(f"\n✓ Data Quality Score: {quality_score:.1f}/100")
        
        return {
            'name': dataset_name,
            'rows': df.shape[0],
            'cols': df.shape[1],
            'missing': missing,
            'duplicates': duplicates,
            'quality_score': quality_score
        }
        
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return None

def main():
    """Main validation function"""
    print("\n" + "="*80)
    print("ScoreSight - Data Quality Validation")
    print("="*80)
    
    datasets = [
        ("data_raw_match.csv", "Raw Match Data"),
        ("data_raw_player.csv", "Raw Player Data"),
        ("data_raw_league.csv", "Raw League Data"),
        ("data_cleaned_match.csv", "Cleaned Match Data"),
        ("data_cleaned_player.csv", "Cleaned Player Data"),
        ("data_cleaned_league.csv", "Cleaned League Data"),
        ("data_features_match.csv", "Feature-Engineered Match Data"),
        ("data_features_player.csv", "Feature-Engineered Player Data"),
        ("data_features_league.csv", "Feature-Engineered League Data"),
        ("data_encoded_match.csv", "Encoded Match Data"),
        ("data_encoded_player.csv", "Encoded Player Data"),
        ("data_encoded_league.csv", "Encoded League Data"),
        ("data_final_match_prediction.csv", "Final Match Prediction Dataset"),
        ("data_final_top_scorer.csv", "Final Top Scorer Dataset"),
        ("data_final_points_tally.csv", "Final Points Tally Dataset"),
    ]
    
    results = []
    for filepath, name in datasets:
        if os.path.exists(filepath):
            result = validate_dataset(filepath, name)
            if result:
                results.append(result)
        else:
            print(f"\n✗ File not found: {filepath}")
    
    # Summary
    print(f"\n{'='*80}")
    print("VALIDATION SUMMARY")
    print(f"{'='*80}\n")
    
    print(f"{'Dataset':<45} {'Rows':>10} {'Cols':>6} {'Missing':>8} {'Dups':>6} {'Score':>6}")
    print("-" * 80)
    
    for r in results:
        print(f"{r['name']:<45} {r['rows']:>10,} {r['cols']:>6} {r['missing']:>8,} {r['duplicates']:>6,} {r['quality_score']:>6.1f}")
    
    # Overall assessment
    avg_quality = sum(r['quality_score'] for r in results) / len(results)
    total_missing = sum(r['missing'] for r in results)
    total_duplicates = sum(r['duplicates'] for r in results)
    
    print("\n" + "="*80)
    print("OVERALL ASSESSMENT")
    print("="*80)
    print(f"\nAverage Quality Score: {avg_quality:.1f}/100")
    print(f"Total Missing Values: {total_missing:,}")
    print(f"Total Duplicate Rows: {total_duplicates:,}")
    
    if avg_quality >= 95 and total_missing == 0 and total_duplicates == 0:
        print("\n✓ EXCELLENT: Data is ready for model training!")
    elif avg_quality >= 85:
        print("\n✓ GOOD: Data quality is acceptable for model training")
    elif avg_quality >= 70:
        print("\n⚠ FAIR: Consider additional cleaning before model training")
    else:
        print("\n✗ POOR: Significant data quality issues detected")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
