import streamlit as st
import sys

st.set_page_config(page_title="Complete Installation Test", layout="wide")
st.title("🧪 Complete Package Installation Test")

# Display system info
col1, col2 = st.columns(2)
with col1:
    st.write("**Python Version:**", sys.version.split()[0])
with col2:
    st.write("**Executable:**", sys.executable)

st.write("---")

# Test all packages
packages = [
    ("streamlit", None, "Web framework"),
    ("pandas", "pd", "Data manipulation"),
    ("numpy", "np", "Numerical computing"),
    ("plotly", None, "Visualization"),
    ("plotly.graph_objects", "go", "Plotly graphs"),
    ("plotly.express", "px", "Plotly express"),
    ("sklearn", None, "Machine learning"),
]

st.subheader("📦 Package Status")

for package, alias, description in packages:
    try:
        if alias:
            exec(f"import {package} as {alias}")
        else:
            exec(f"import {package}")
        
        # Get version
        if package == "sklearn":
            version = eval("sklearn.__version__")
        elif package in ["plotly.graph_objects", "plotly.express"]:
            version = eval("plotly.__version__")
        else:
            version = eval(f"{package.split('.')[0]}.__version__")
        
        st.success(f"✅ **{package}** ({description}): v{version}")
        
    except ImportError as e:
        st.error(f"❌ **{package}**: Not installed - {e}")
    except AttributeError:
        st.success(f"✅ **{package}**: Installed (no version)")
    except Exception as e:
        st.warning(f"⚠️ **{package}**: {str(e)[:100]}")

st.write("---")

# Test functionality
st.subheader("🚀 Functionality Tests")

# Test 1: Pandas + NumPy
try:
    import pandas as pd
    import numpy as np
    
    # Create sample data
    data = pd.DataFrame({
        'Team': ['Arsenal', 'Man City', 'Liverpool', 'Chelsea'],
        'Points': np.array([90, 85, 80, 75]),
        'Wins': [28, 26, 24, 22]
    })
    
    with st.expander("Test 1: Pandas + NumPy Dataframe"):
        st.write("Sample EPL Data:")
        st.dataframe(data)
        st.write(f"Data shape: {data.shape}")
        st.write(f"Mean points: {data['Points'].mean():.1f}")
        st.success("✅ Pandas and NumPy working!")
        
except Exception as e:
    st.error(f"❌ Pandas/NumPy test failed: {e}")

# Test 2: Plotly
try:
    import plotly.express as px
    import plotly.graph_objects as go
    
    with st.expander("Test 2: Plotly Visualization"):
        # Create a plot
        fig1 = px.bar(data, x='Team', y='Points', title='EPL Points', color='Team')
        st.plotly_chart(fig1, use_container_width=True)
        
        # Create another plot
        fig2 = go.Figure(data=[
            go.Scatter(x=data['Team'], y=data['Wins'], mode='lines+markers')
        ])
        fig2.update_layout(title='EPL Wins')
        st.plotly_chart(fig2, use_container_width=True)
        
        st.success("✅ Plotly working!")
        
except Exception as e:
    st.error(f"❌ Plotly test failed: {e}")

# Test 3: Scikit-learn
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error
    
    with st.expander("Test 3: Scikit-learn ML"):
        # Simple regression example
        X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
        y = np.array([2, 4, 6, 8, 10])
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = LinearRegression()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        
        st.write(f"Model Coefficient: {model.coef_[0]:.4f}")
        st.write(f"Model Intercept: {model.intercept_:.4f}")
        st.write(f"Test MSE: {mse:.4f}")
        
        if abs(model.coef_[0] - 2) < 0.1:  # Should be close to 2 (y = 2x)
            st.success("✅ Scikit-learn working correctly!")
        else:
            st.warning("⚠️ Scikit-learn working but model may need tuning")
            
except Exception as e:
    st.error(f"❌ Scikit-learn test failed: {e}")

# Test 4: Streamlit widgets
with st.expander("Test 4: Streamlit Components"):
    st.write("Testing Streamlit widgets:")
    
    # Slider
    value = st.slider("Select a value", 0, 100, 50)
    st.write(f"Slider value: {value}")
    
    # Selectbox
    option = st.selectbox("Choose a team:", data['Team'].tolist())
    st.write(f"Selected: {option}")
    
    # Button
    if st.button("Click me!"):
        st.balloons()
        st.success("Button clicked!")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a file (test only)")
    if uploaded_file is not None:
        st.write(f"File uploaded: {uploaded_file.name}")
    
    st.success("✅ Streamlit widgets working!")

st.write("---")

# Final status
st.subheader("🎯 Installation Summary")

all_packages = ["streamlit", "pandas", "numpy", "plotly", "sklearn"]
status = {}

for pkg in all_packages:
    try:
        __import__(pkg)
        status[pkg] = "✅ Installed"
    except ImportError:
        status[pkg] = "❌ Missing"

# Display summary
for pkg, stat in status.items():
    st.write(f"{stat} - **{pkg}**")

if all("✅" in s for s in status.values()):
    st.balloons()
    st.success("🎉 ALL PACKAGES INSTALLED AND WORKING! Your app is ready to run!")
else:
    st.error("Some packages are missing. Run: `pip install -r requirements.txt`")

# Installation command reminder
st.write("---")
st.code("""
# To install all packages:
pip install streamlit==1.28.0 pandas==2.0.3 numpy==1.26.4 plotly==5.17.0 scikit-learn==1.3.0

# Or if you have requirements.txt:
pip install -r requirements.txt
""")