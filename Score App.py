# app.py
# Streamlit multipage demo app with 5 problem statements, interactive charts, and styled front page.
# Author: Cleaned for Javith-Farvez (2025-12-01)
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Multi-Problem Demo", layout="wide", initial_sidebar_state="collapsed")

# ---------- Styling via st.markdown (HTML/CSS) ----------
# Use a lighter, readable background to avoid 'black' appearance
st.markdown(
    """
    <style>
    /* App background: light, modern gradient and readable text */
    .stApp {
        background: linear-gradient(135deg, #eaf6ff 0%, #dfeef9 50%, #cfe9ff 100%);
        color: #0b2545;
        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }

    /* Centered container styling */
    .center {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }

    .big-title {
        font-size:42px;
        font-weight:700;
        color: #0b3d91;
        margin-bottom: 4px;
    }

    .subtitle {
        font-size:18px;
        color: #234e70;
        margin-bottom: 20px;
    }

    .big-button {
        background: linear-gradient(90deg,#ff7e5f,#feb47b);
        border: none;
        color: white;
        padding: 12px 28px;
        text-align: center;
        font-size:16px;
        border-radius: 10px;
        cursor: pointer;
        box-shadow: 0 6px 12px rgba(0,0,0,0.12);
    }

    .small-button {
        background: linear-gradient(90deg,#667eea,#764ba2);
        border: none;
        color: white;
        padding: 8px 18px;
        font-size:14px;
        border-radius: 8px;
        cursor: pointer;
    }

    .card {
        background: rgba(11,37,69,0.04);
        padding: 14px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.06);
        margin-bottom: 12px;
    }

    .muted {
        color: #234e70;
    }

    /* Make native Streamlit buttons a bit larger in columns (non-breaking) */
    .stButton > button {
        min-width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Session state initialization ----------
if "page" not in st.session_state:
    st.session_state.page = 0  # 0: front page, 1..5 problems, 6 summary
if "results" not in st.session_state:
    st.session_state.results = {}  # store percentages for pages 1..5
if "seed_base" not in st.session_state:
    st.session_state.seed_base = int(datetime.now().timestamp()) % 10000

# Navigation helpers
def go_to(page: int):
    st.session_state.page = page

def next_page():
    st.session_state.page += 1

# Compute score for each problem using widget values stored in session_state
def compute_score(page: int):
    """Return a percentage score (0-100) based on the inputs for the given page."""
    # Page 1: Category proportion
    if page == 1:
        cat = st.session_state.get("input_1_category", "A")
        thresh = st.session_state.get("input_1_threshold", 50)
        rng = np.random.RandomState(st.session_state.seed_base + 1)
        df = pd.DataFrame({
            "Category": ["A", "B", "C", "D"],
            "Value": rng.randint(10, 120, size=4)
        })
        # Ensure selected category exists
        if cat not in df["Category"].values:
            selected_val = df.loc[0, "Value"]
        else:
            selected_val = int(df.loc[df["Category"] == cat, "Value"].squeeze())
        score = np.clip((selected_val - thresh) / max(1, thresh) * 100, 0, 100)
        return float(round(score, 2)), df

    # Page 2: Line fit variance explained
    elif page == 2:
        noise = st.session_state.get("input_2_noise", 10)
        npoints = st.session_state.get("input_2_npoints", 30)
        rng = np.random.RandomState(st.session_state.seed_base + 2)
        x = np.linspace(0, 10, npoints)
        y_true = 2.5 * x + 5
        y = y_true + rng.normal(0, noise, size=npoints)
        coef = np.polyfit(x, y, 1)
        y_pred = np.polyval(coef, x)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0
        score = float(round(max(0, min(1, r2)) * 100, 2))
        df = pd.DataFrame({"x": x, "y": y, "y_true": y_true, "y_pred": y_pred})
        return score, df

    # Page 3: Classification by threshold and simulated accuracy
    elif page == 3:
        n = st.session_state.get("input_3_n", 200)
        prob_threshold = st.session_state.get("input_3_threshold", 0.5)
        rng = np.random.RandomState(st.session_state.seed_base + 3)
        probs = rng.rand(n)
        labels = (probs > 0.5).astype(int)  # true labels using 0.5
        preds = (probs > prob_threshold).astype(int)
        accuracy = (preds == labels).mean()
        score = float(round(accuracy * 100, 2))
        df = pd.DataFrame({"prob": probs, "label": labels, "pred": preds})
        return score, df

    # Page 4: Time-series moving average difference percent
    elif page == 4:
        days = st.session_state.get("input_4_days", 30)
        window = st.session_state.get("input_4_window", 3)
        rng = np.random.RandomState(st.session_state.seed_base + 4)
        dates = [ (datetime.today() - timedelta(days=(days - 1 - i))).date() for i in range(days) ]
        vals = rng.randint(20, 120, size=days).astype(float)
        df = pd.DataFrame({"date": dates, "value": vals})
        df["ma"] = df["value"].rolling(window=window, min_periods=1).mean()
        pct = (df["value"] > df["ma"]).mean()
        score = float(round(pct * 100, 2))
        return score, df

    # Page 5: Distribution top-bin percentage
    elif page == 5:
        n = st.session_state.get("input_5_n", 500)
        bins = st.session_state.get("input_5_bins", 5)
        rng = np.random.RandomState(st.session_state.seed_base + 5)
        data = rng.randn(n) * 15 + 50
        hist, edges = np.histogram(data, bins=bins)
        top_bin_pct = float(round(hist.max() / hist.sum() * 100, 2))
        # Prepare binned df for charting
        binned = pd.cut(data, bins=bins).astype(str)
        counts = binned.value_counts().sort_index()
        chart_df = pd.DataFrame({"bin": counts.index, "count": counts.values})
        return top_bin_pct, chart_df

    return 0.0, pd.DataFrame()

# ---------- Front page ----------
def front_page():
    # Centered big title, subtitle and Next button
    st.markdown('<div class="center">', unsafe_allow_html=True)
    st.markdown('<div class="big-title">Interactive Problem Statements Demo</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">A Streamlit-only app demonstrating 5 problems with interactive datasets and charts.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Next — Start Problems", key="front_next"):
            go_to(1)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Problem pages ----------
PROBLEMS = {
    1: {
        "title": "Problem 1 — Category Proportions",
        "desc": (
            "You are given a small categorical dataset with numeric values per category. "
            "Select a category and threshold. The score reflects how much the selected category's value "
            "exceeds the threshold (normalized to percent)."
        ),
    },
    2: {
        "title": "Problem 2 — Line Fit / Variance Explained",
        "desc": (
            "A noisy linear dataset is generated. Adjust noise and number of points. "
            "The score shows R² (variance explained) of a simple linear fit."
        ),
    },
    3: {
        "title": "Problem 3 — Probability Thresholding / Classification",
        "desc": (
            "Random probabilities are generated and true labels are defined by 0.5. "
            "Adjust the classification threshold to see accuracy change."
        ),
    },
    4: {
        "title": "Problem 4 — Time Series & Moving Average",
        "desc": (
            "A time series is generated. Choose days and moving average window. "
            "The score is the percent of days where the value is above the moving average."
        ),
    },
    5: {
        "title": "Problem 5 — Distribution & Binning",
        "desc": (
            "A numeric distribution is sampled. Choose number of bins and sample size. "
            "The score is the percentage of values in the top bin."
        ),
    },
}

def render_problem(page: int):
    meta = PROBLEMS.get(page, {})
    st.markdown(f'<div class="card"><h2 style="margin:0px;">{meta.get("title","")}</h2></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="muted">{meta.get("desc","")}</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Layout: Inputs left, Chart right
    left, right = st.columns([1, 2])

    if page == 1:
        with left:
            rng = np.random.RandomState(st.session_state.seed_base + 1)
            df_preview = pd.DataFrame({
                "Category": ["A", "B", "C", "D"],
                "Value": rng.randint(10, 120, size=4)
            })
            st.write("Dataset preview:")
            st.dataframe(df_preview, height=150)

            category = st.selectbox("Select category", options=df_preview["Category"].tolist(), key="input_1_category")
            threshold = st.slider("Threshold value", min_value=0, max_value=150, value=50, key="input_1_threshold")
            st.caption("Press Submit/Next to lock result and go to the next problem.")
        score, df = compute_score(1)
        with right:
            st.subheader("Values by Category")
            bar = alt.Chart(df).mark_bar().encode(
                x=alt.X("Category:N", sort=None),
                y=alt.Y("Value:Q"),
                color=alt.Color("Category:N", legend=None)
            ).properties(height=300)
            st.altair_chart(bar, use_container_width=True)
            st.metric("Computed percentage", f"{score}%")
    elif page == 2:
        with left:
            noise = st.slider("Noise (std dev)", 0, 50, 10, key="input_2_noise")
            npoints = st.slider("Number of points", 10, 200, 30, key="input_2_npoints")
            st.caption("Adjust and Submit/Next to save result.")
        score, df = compute_score(2)
        with right:
            st.subheader("Data and Linear Fit")
            base = alt.Chart(df).mark_line().encode(x="x:Q", y=alt.Y("y:Q", title="Observed"))
            truth = alt.Chart(df).mark_line(strokeDash=[5,5]).encode(x="x:Q", y="y_true:Q")
            pred = alt.Chart(df).mark_line().encode(x="x:Q", y="y_pred:Q")
            chart = (base + truth + pred).properties(height=350)
            st.altair_chart(chart, use_container_width=True)
            st.metric("R² (variance explained)", f"{score}%")
    elif page == 3:
        with left:
            n = st.slider("Number of samples", 50, 2000, 200, step=50, key="input_3_n")
            threshold = st.slider("Classification threshold", 0.0, 1.0, 0.5, step=0.01, key="input_3_threshold")
            st.caption("Try different thresholds and Submit/Next.")
        score, df = compute_score(3)
        with right:
            st.subheader("Probability Distribution")
            hist = alt.Chart(df).mark_bar().encode(
                alt.X("prob:Q", bin=alt.Bin(maxbins=30), title="Predicted probability"),
                y='count()',
            ).properties(height=300)
            st.altair_chart(hist, use_container_width=True)
            st.metric("Accuracy", f"{score}%")
    elif page == 4:
        with left:
            days = st.slider("Days in time series", 7, 180, 30, key="input_4_days")
            window = st.slider("MA window", 1, 30, 3, key="input_4_window")
            st.caption("Moving average window affects the percentage metric.")
        score, df = compute_score(4)
        with right:
            st.subheader("Time Series with Moving Average")
            line = alt.Chart(df).mark_line().encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("value:Q", title="Value")
            )
            ma = alt.Chart(df).mark_line().encode(x="date:T", y="ma:Q")
            st.altair_chart((line + ma).properties(height=350), use_container_width=True)
            st.metric("Percent days value > MA", f"{score}%")
    elif page == 5:
        with left:
            n = st.slider("Number of samples", 100, 2000, 500, step=50, key="input_5_n")
            bins = st.slider("Number of bins", 3, 12, 5, key="input_5_bins")
            st.caption("Bin count changes where the mass of the distribution lies.")
        score, chart_df = compute_score(5)
        with right:
            st.subheader("Binned distribution (counts)")
            bar = alt.Chart(chart_df).mark_bar().encode(
                x=alt.X("bin:N", sort=None, title="Bin"),
                y=alt.Y("count:Q", title="Count")
            ).properties(height=320)
            st.altair_chart(bar, use_container_width=True)
            st.metric("Percent in top bin", f"{score}%")
    else:
        st.write("Unknown problem page.")

    # Submit / Next button centered
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        def submit_and_next(pg=page):
            score_val, _ = compute_score(pg)
            st.session_state.results[f"problem_{pg}"] = score_val
            if pg < 5:
                go_to(pg + 1)
            else:
                go_to(6)  # summary

        if st.button("Submit / Next", key=f"submit_{page}"):
            submit_and_next()

    # Also provide back button
    if page > 1:
        back_col1, back_col2, back_col3 = st.columns([1, 2, 1])
        with back_col1:
            if st.button("Back", key=f"back_{page}"):
                go_to(page - 1)

# ---------- Summary page ----------
def summary_page():
    st.markdown('<div class="card"><h2 style="margin:0px;">Summary</h2></div>', unsafe_allow_html=True)
    st.markdown("Below are the computed percentages/scores from each problem. You can review each problem and retake if desired.")
    st.markdown("---")

    results = st.session_state.get("results", {})
    summary_list = []
    for p in range(1, 6):
        key = f"problem_{p}"
        if key not in results:
            score_val, _ = compute_score(p)
            results[key] = score_val
        summary_list.append({"problem": p, "score": results.get(key, 0.0)})

    summary_df = pd.DataFrame(summary_list)
    st.table(summary_df.set_index("problem").style.format({"score": "{:.2f}%"}))

    chart_df = pd.DataFrame({
        "problem": summary_df["problem"].astype(str),
        "score": summary_df["score"].astype(float)
    })

    bar = alt.Chart(chart_df).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X("problem:N", title="Problem"),
        y=alt.Y("score:Q", title="Score (%)"),
        color=alt.Color("score:Q", scale=alt.Scale(scheme="blues")),
        tooltip=["problem", "score"]
    ).properties(height=320)
    st.altair_chart(bar, use_container_width=True)

    for p in range(1, 6):
        st.markdown(f"### Problem {p} detail")
        _, df = compute_score(p)
        if p == 1:
            chart = alt.Chart(df).mark_bar().encode(x="Category:N", y="Value:Q", color="Category:N")
            st.altair_chart(chart.properties(height=200), use_container_width=True)
        elif p == 2:
            chart = alt.Chart(df).mark_line().encode(x="x:Q", y="y:Q")
            st.altair_chart(chart.properties(height=200), use_container_width=True)
        elif p == 3:
            chart = alt.Chart(df).mark_bar().encode(x=alt.X("prob:Q", bin=alt.Bin(maxbins=30)), y='count()')
            st.altair_chart(chart.properties(height=200), use_container_width=True)
        elif p == 4:
            chart = alt.Chart(df).mark_line().encode(x="date:T", y="value:Q")
            st.altair_chart(chart.properties(height=200), use_container_width=True)
        elif p == 5:
            chart = alt.Chart(df).mark_bar().encode(x="bin:N", y="count:Q")
            st.altair_chart(chart.properties(height=200), use_container_width=True)

    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        if st.button("Restart (Front Page)"):
            st.session_state.seed_base = int(datetime.now().timestamp()) % 10000
            st.session_state.results = {}
            go_to(0)
    with col_b:
        if st.button("Review Problem 1"):
            go_to(1)
    with col_c:
        if st.button("Review Problem 5"):
            go_to(5)

# ---------- Main rendering ----------
def main():
    page = st.session_state.page
    st.markdown(f"<div style='margin-bottom:12px;color:#234e70'>Page: {page} (0=Front, 1-5=Problems, 6=Summary)</div>", unsafe_allow_html=True)

    if page == 0:
        front_page()
    elif 1 <= page <= 5:
        render_problem(page)
    elif page == 6:
        summary_page()
    else:
        st.write("Unknown page. Resetting to front.")
        go_to(0)

if __name__ == "__main__":
    main()
