import requests

import streamlit as st
import boto3

st.title("System Status")
st.write("Displays the status of all the backend services and the current config that is set.")

st.write("")
st.write("")

green = "#36e236"
red = "#f6310a"
grey = "#EBDBB2"
success = "✅"
fail = "❌"


def middleware_health():
    url = "http://localhost:5999/healthcheck"
    response = requests.request("GET", url, headers={}, data={})
    return True if response.status_code == 200 else False


def llm_health():
    url = "http://localhost:6999/healthcheck"
    response = requests.request("GET", url, headers={}, data={})
    return True if response.status_code == 200 else False


def deepgram_health():
    url = "http://localhost:5999/deepgram_healthcheck"
    response = requests.request("GET", url, headers={}, data={})
    return True if response.status_code == 200 else False


def aws_health():
    try:
        s3 = boto3.client("s3")
        s3.list_buckets()
    except:
        return False
    return True


def display_status(name: str):
    color = green
    status_icon = success

    if (name == "Middleware" and middleware_health()) or (name == "LLM Service" and llm_health()) or (
            name == "Deepgram" and deepgram_health()) or (name == "AWS" and aws_health()):
        color = grey
        status_icon = success
    else:
        color = red
        status_icon = fail

    st.markdown(f"""<p style='text-align: left; color: 
        {color}; font-family: monospace; font-weight: 600; letter-spacing: -0.005em; line-height: 1.2; '> 
        {status_icon} {name} </p>""", unsafe_allow_html=True)


# st.header("Services Health:")
col1, col2 = st.columns(2)
with col1:
    display_status("Middleware")
    display_status("LLM Service")
with col2:
    display_status("Deepgram")
    display_status("AWS")

st.write("")
st.write("")

st.subheader("System Parameters")
config = st.session_state['config']
st.write(config)
