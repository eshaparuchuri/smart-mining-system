import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Smart Mining Digital Twin", layout="wide")

# 🔴 CHANGE THIS AFTER DEPLOYMENT
API_URL = "http://127.0.0.1:5000/predict"

# -----------------------------
# STYLING
# -----------------------------
st.markdown("""
<style>
.card {
    padding:15px;
    border-radius:12px;
    color:white;
    text-align:center;
}
.green { background-color:#16a34a; }
.red { background-color:#dc2626; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🏭 Digital Twin System")
page = st.sidebar.radio("Navigation", ["📊 Overview", "🏭 Machine", "🚨 Alerts"])

# -----------------------------
# SESSION STATE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = {}

if "alerts" not in st.session_state:
    st.session_state.alerts = []

# -----------------------------
# FETCH DATA
# -----------------------------
def fetch_data():
    try:
        res = requests.get(API_URL)
        return res.json()
    except:
        return {}

data = fetch_data()

if not data:
    st.warning("Waiting for Digital Twin data...")
    st.stop()

# -----------------------------
# STORE HISTORY
# -----------------------------
for machine_id, info in data.items():

    if machine_id not in st.session_state.history:
        st.session_state.history[machine_id] = []

    values = info["data"]
    st.session_state.history[machine_id].append(values)

    # limit memory
    if len(st.session_state.history[machine_id]) > 50:
        st.session_state.history[machine_id].pop(0)

    if info["anomaly"]:
        st.session_state.alerts.append({
            "machine": machine_id,
            "time": values["timestamp"],
            "temp": values["temperature"]
        })

# -----------------------------
# 📊 OVERVIEW
# -----------------------------
if page == "📊 Overview":

    st.title("📊 Digital Twin Overview")

    total = len(data)
    anomalies = sum(1 for m in data.values() if m["anomaly"])

    c1, c2, c3 = st.columns(3)
    c1.metric("Machines", total)
    c2.metric("Normal", total - anomalies)
    c3.metric("Anomalies", anomalies)

    st.divider()

    cols = st.columns(len(data))

    for i, (machine_id, info) in enumerate(data.items()):

        status_class = "green" if not info["anomaly"] else "red"
        score = int(info["prediction_score"] * 100)

        with cols[i]:
            st.markdown(f"""
            <div class="card {status_class}">
                <h3>{machine_id}</h3>
                <p>{info['status']}</p>
                <p>Health: {score}%</p>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------
# 🏭 MACHINE VIEW
# -----------------------------
elif page == "🏭 Machine":

    st.title("🏭 Machine Digital Twin")

    machine_id = st.selectbox("Select Machine", list(data.keys()))

    machine = data[machine_id]
    values = machine["data"]
    forecast = machine["forecast"]

    score = int(machine["prediction_score"] * 100)

    if machine["anomaly"]:
        st.error(f"🚨 ANOMALY (Score: {score}%)")
    else:
        st.success(f"✅ NORMAL (Score: {score}%)")

    # metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temp", f"{values['temperature']:.2f}")
    c2.metric("Vibration", f"{values['vibration']:.2f}")
    c3.metric("Load", f"{values['load']:.2f}")
    c4.metric("Pressure", f"{values['pressure']:.2f}")

    st.divider()

    # 🔹 HISTORY
    df = pd.DataFrame(st.session_state.history[machine_id])

    if not df.empty:
        st.subheader("📈 Past Trend")
        st.line_chart(df[["temperature", "vibration", "load", "pressure"]])

    # 🔮 FORECAST
    if forecast:
        future_df = pd.DataFrame(forecast)

        st.subheader("🔮 Future Forecast")
        st.line_chart(future_df[["temperature", "vibration", "load", "pressure"]])

# -----------------------------
# 🚨 ALERTS
# -----------------------------
elif page == "🚨 Alerts":

    st.title("🚨 Alerts")

    if st.session_state.alerts:
        df = pd.DataFrame(st.session_state.alerts[::-1])
        st.dataframe(df, width='stretch')
    else:
        st.success("No alerts")

# -----------------------------
# AUTO REFRESH
# -----------------------------
time.sleep(2)
st.rerun()