import streamlit as st
from uuid import uuid4

st.session_state['conv_id'] = str(uuid4())
st.title("🎬 Generative AI Studio")

# Set default config
config = {
    'input_type': "Plain Text",
    'output_type': "Plain Text",
    'llm_selected': "google/flan-t5-base",
    'stt_model': "",
    'stt_features': "",
}
st.session_state['config'] = config
