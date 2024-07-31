# -*- coding: utf-8 -*-
import concurrent.futures
import html
import json
import os
import re
import requests
import streamlit as st

if "user_emails" not in st.session_state:
    st.session_state["user_emails"] = {}
if "user_anomalies" not in st.session_state:
    st.session_state["user_anomalies"] = {}
if "scanned_customers" not in st.session_state:
    st.session_state["scanned_customers"] = []

st.set_page_config(page_title="Personalization and Proactive Assistance", page_icon="📢", layout="wide")
st.html("<h1 style='text-align: center;'>Personalization and Proactive Assistance</h1>")

def generate_emails():
    if not os.path.exists("data/user_emails/user_emails.json"):
        os.makedirs("data/user_emails", exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(requests.get, [f"http://localhost:8001/user_insight/Customer{i+1}" for i in range(10)])
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(requests.get, f"http://localhost:8001/notification/email/Customer{i+1}") for i in range(10)]
        for i, future in enumerate(futures):
            st.session_state["user_emails"][f"Customer{i+1}"] = future.result().text
    with open("data/user_emails/user_emails.json", "w") as f:
        json.dump(st.session_state["user_emails"], f, indent=2)

    with open("data/user_emails/user_emails.json", "r") as f:
        st.session_state["user_emails"] = json.load(f)


st.write("## Contextual Understanding & Personalization")
st.subheader("")

c1, c2 = st.columns([0.2, 0.8])
with c1:
    if st.button("Generate"):
        with st.spinner("Generating..."):
            generate_emails()
    if st.session_state["user_emails"]:
        customer = st.radio("Customers", 
                            list(st.session_state["user_emails"].keys()))
    else:
        customer = None

with c2:
    if customer:
        pattern = r'\`\`\`html(.*?)\`\`\`'
        email = st.session_state["user_emails"][customer]
        match = re.findall(pattern, email, re.DOTALL)
        if match:
            email = match[-1]
        email = email.replace("\\", "")
        email = html.unescape(email)
        with st.container(border=True):
            st.html(email)