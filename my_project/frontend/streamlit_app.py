import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="5 Problems App", layout="wide")
st.title("Connect Streamlit → FastAPI (5 problems)")

# Problem 1
with st.form("form1"):
    text_in = st.text_area("Enter text for problem 1")
    submit1 = st.form_submit_button("Send to backend")
if submit1:
    payload = {"text": text_in}
    try:
        resp = requests.post(f"{BACKEND_URL}/problem1", json=payload, timeout=30)
        resp.raise_for_status()
        st.json(resp.json())
    except Exception as e:
        st.error(f"Error: {e}")

# Problem 2
with st.form("form2"):
    uploaded_file = st.file_uploader("Upload CSV or text file", type=["csv", "txt"])
    param = st.text_input("Optional param")
    submit2 = st.form_submit_button("Upload & process")
if submit2:
    if uploaded_file is None:
        st.error("Please upload a file")
    else:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        data = {"param": param}
        try:
            resp = requests.post(f"{BACKEND_URL}/problem2", files=files, data=data, timeout=60)
            resp.raise_for_status()
            st.json(resp.json())
        except Exception as e:
            st.error(f"Error: {e}")

# Problem 3
with st.form("form3"):
    p3_text = st.text_input("Enter text")
    p3_k = st.number_input("k (int)", min_value=1, max_value=100, value=3, step=1)
    submit3 = st.form_submit_button("Send")
if submit3:
    form_data = {"text": p3_text, "k": str(int(p3_k))}
    try:
        resp = requests.post(f"{BACKEND_URL}/problem3", data=form_data, timeout=30)
        resp.raise_for_status()
        st.json(resp.json())
    except Exception as e:
        st.error(f"Error: {e}")

# Problem 4
with st.form("form4"):
    number_val = st.number_input("Enter number", value=2.0, format="%.4f")
    submit4 = st.form_submit_button("Compute")
if submit4:
    payload = {"number": float(number_val)}
    try:
        resp = requests.post(f"{BACKEND_URL}/problem4", json=payload, timeout=30)
        resp.raise_for_status()
        st.json(resp.json())
    except Exception as e:
        st.error(f"Error: {e}")

# Problem 5
with st.form("form5"):
    p5_file = st.file_uploader("Optional file (any type)", key="p5")
    p5_text = st.text_input("Optional text")
    submit5 = st.form_submit_button("Send")
if submit5:
    files = {}
    data = {"text": p5_text}
    if p5_file:
        files = {"file": (p5_file.name, p5_file.getvalue())}
    try:
        resp = requests.post(f"{BACKEND_URL}/problem5", files=files or None, data=data, timeout=60)
        resp.raise_for_status()
        st.json(resp.json())
    except Exception as e:
        st.error(f"Error: {e}")
