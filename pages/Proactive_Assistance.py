import concurrent.futures
import json
import os
import requests
import streamlit as st

st.set_page_config(page_title="Personalization and Proactive Assistance", page_icon="📢", layout="wide")
st.html("<h1 style='text-align: center;'>Personalization and Proactive Assistance</h1>")

def scan_db() -> list:
    if not os.path.exists("data/user_anomalies/user_anomalies.json"):
        os.makedirs("data/user_anomalies", exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(requests.get, f"http://localhost:8001/check_anomaly/Customer{i+1}") for i in range(10)]
    for i, future in enumerate(futures):
        st.session_state["user_anomalies"][f"Customer{i+1}"] = future.result().json()
    with open("data/user_anomalies/user_anomalies.json", "w") as f:
        json.dump(st.session_state["user_anomalies"], f, indent=2)
    with open("data/user_anomalies/user_anomalies.json", "r") as f:
        st.session_state["user_anomalies"] = json.load(f)
    scanned_customers = []
    for customer in st.session_state["user_anomalies"]:
        if st.session_state["user_anomalies"][customer].get("has_issues"):
            scanned_customers.append(customer)
    return scanned_customers

st.write("## Proactive Assistance")
st.subheader("")

c1, c2 = st.columns([0.2, 0.8])
with c1:
    if st.button("Scan"):
        with st.spinner("Scanning..."):
            st.session_state["scanned_customers"] = scan_db()
    
    if st.session_state["scanned_customers"]:
        selected_customer = st.radio("Select Customer", st.session_state["scanned_customers"])
    else:
        selected_customer = None

with c2:
    if selected_customer:
        st.toast(st.session_state["user_anomalies"][selected_customer].get("sms"))
        st.html(st.session_state["user_anomalies"][selected_customer].get("email"))