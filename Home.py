import streamlit as st
from uuid import uuid4

st.session_state['conv_id'] = str(uuid4())
st.title("🎬 Generative AI Studio")

# st.write("Generative AI Studio is a customizable system which can be used to build a configurable user-interface which is integrated with services like speech-to-text (STT) and large language models (LLM).")
# st.write("This helps the user to build and try out various input/output types with conjunction with different combinations of tools.")

# st.subheader("Instructions")
st.write("")
st.write("")

st.write(
    "Use the ```System Status``` tab in the sidebar to view the current status of all the backend services and current system parameters.")
st.write(
    "Use the ```Config Initializer``` tab in the sidebar to configure various parameters like the input/output type, speech-to-text model, the large language model used, etc.")

# Set default config
config = {
    'input_type': "Plain Text",
    'output_type': "Plain Text",
    'llm_selected': "google/flan-t5-base",
    'stt_model': "",
    'stt_features': "",
}
st.session_state['config'] = config
