# ScoreSight Analytics (Streamlit)

This repository contains the Streamlit app `app.py` for football (EPL) predictions.

## Quick deploy to Streamlit Cloud

1. Push this repository to GitHub (or add these files to your existing GitHub repo).
2. Go to https://streamlit.io/cloud and connect your GitHub account.
3. Create a new app and point it to the repository and branch, and set the main file to `app.py`.
4. Streamlit Cloud will install the packages from `requirements.txt` and launch the app.

## Notes

- If your model files are large (`.joblib`, `.pkl`), consider using Git LFS or hosting them externally (S3, Azure Blob) and loading at runtime.
- The `requirements.txt` contains the minimal dependencies detected by static analysis. If your models require `xgboost`, `lightgbm` or other libraries, add them.

## Git commands (PowerShell)

Replace `<your-repo-url>` with your GitHub repository URL, or run these inside your existing repo (`D:\EPL\Projects_2`) if you already have it:

```powershell
cd D:\EPL\Projects_2
# If this folder is already a git repo, skip `git init` and set remote
git init
git add .
git commit -m "Prepare app for Streamlit Cloud deployment"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```

After pushing, create the Streamlit Cloud app and set `app.py` as the entry point.

## Next steps I can do for you

- Add GitHub Actions to auto-deploy on push (optional for Streamlit Cloud).
- Add Git LFS setup for model files (if you have large models).
- Move these files into your existing repo at `D:\EPL\Projects_2` for deployment.
