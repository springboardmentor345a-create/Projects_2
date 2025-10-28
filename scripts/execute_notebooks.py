"""
Execute all preprocessing notebooks sequentially and validate outputs
"""
import subprocess
import sys
import os
from pathlib import Path

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def execute_notebook(notebook_path):
    """Execute a Jupyter notebook and return success status"""
    print(f"\n{'='*80}")
    print(f"Executing: {notebook_path}")
    print(f"{'='*80}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "jupyter", "nbconvert", 
             "--to", "notebook", 
             "--execute", notebook_path,
             "--output", notebook_path.replace('.ipynb', '_executed.ipynb'),
             "--ExecutePreprocessor.timeout=600"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            print(f"✓ SUCCESS: {notebook_path} executed successfully!")
            return True
        else:
            print(f"✗ ERROR: {notebook_path} failed to execute")
            print(f"Error output:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ EXCEPTION: {str(e)}")
        return False

def validate_output_files(expected_files):
    """Validate that expected output files were created"""
    print(f"\n{'='*80}")
    print("Validating Output Files")
    print(f"{'='*80}\n")
    
    all_exist = True
    for file in expected_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✓ {file} ({size:,} bytes)")
        else:
            print(f"✗ {file} - NOT FOUND")
            all_exist = False
    
    return all_exist

def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("ScoreSight - Sequential Notebook Execution")
    print("="*80)
    
    # Change to notebooks directory
    os.chdir('../notebooks')
    
    notebooks = [
        "01_Data_Loading_EDA.ipynb",
        "02_Data_Cleaning.ipynb",
        "03_Feature_Engineering.ipynb",
        "04_Encoding_Feature_Selection.ipynb",
        "05_Data_Visualization.ipynb"
    ]
    
    # Execute each notebook
    results = {}
    for notebook in notebooks:
        success = execute_notebook(notebook)
        results[notebook] = success
        
        if not success:
            print(f"\n⚠ Stopping execution due to failure in {notebook}")
            break
    
    # Print summary
    print(f"\n{'='*80}")
    print("EXECUTION SUMMARY")
    print(f"{'='*80}\n")
    
    for notebook, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {notebook}")
    
    # Validate expected outputs after all notebooks
    if all(results.values()):
        print("\n\nAll notebooks executed successfully!")
        print("Validating output files...")
        
        expected_files = [
            "data_raw_match.csv",
            "data_raw_player.csv",
            "data_raw_league.csv",
            "data_cleaned_match.csv",
            "data_cleaned_player.csv",
            "data_cleaned_league.csv",
            "data_features_match.csv",
            "data_features_player.csv",
            "data_features_league.csv",
            "data_encoded_match.csv",
            "data_encoded_player.csv",
            "data_encoded_league.csv",
            "data_final_match_prediction.csv",
            "data_final_top_scorer.csv",
            "data_final_points_tally.csv"
        ]
        
        validate_output_files(expected_files)
    
    print(f"\n{'='*80}")
    print("Execution Complete")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
