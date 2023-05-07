import streamlit as st

st.title("Health Check")

st.header("Current Config:")
config = st.session_state['config']
st.write(config)
