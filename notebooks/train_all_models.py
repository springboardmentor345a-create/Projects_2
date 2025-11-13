"""
Train all 5 problem statements and save only the best model for each.
This script runs each notebook's training cells to ensure actual training occurs.
"""
import subprocess
import sys
from pathlib import Path

notebooks = [
    '10_League_Winner_PS1.ipynb',
    '11_Match_Winner_PS2.ipynb',
    '12_Top_Scorer_PS3.ipynb',
    '13_Total_Points_PS4.ipynb',
    '14_Match_Result_PS5.ipynb'
]

print("="*80)
print("TRAINING ALL 5 PROBLEM STATEMENTS")
print("="*80)

for i, notebook in enumerate(notebooks, 1):
    print(f"\n[{i}/5] Training {notebook}...")
    print("-"*80)
    
    try:
        result = subprocess.run(
            [
                'jupyter', 'nbconvert',
                '--to', 'notebook',
                '--execute',
                notebook,
                '--output', notebook,
                '--ExecutePreprocessor.timeout=600',
                '--inplace'
            ],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {notebook} completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ {notebook} failed with error:")
        print(e.stderr)
        sys.exit(1)

print("\n" + "="*80)
print("✅ ALL MODELS TRAINED SUCCESSFULLY!")
print("="*80)

# List saved models
models_dir = Path('models')
if models_dir.exists():
    print("\n📦 Saved Models:")
    for model_file in sorted(models_dir.glob('*.joblib')):
        size_mb = model_file.stat().st_size / (1024 * 1024)
        print(f"   {model_file.name} ({size_mb:.2f} MB)")
    
    print("\n📄 Metadata Files:")
    for meta_file in sorted(models_dir.glob('*.json')):
        print(f"   {meta_file.name}")
