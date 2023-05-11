import requests
import json
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM

st.title("Studio")

config = st.session_state['config']
# config = {
#     "input_type": "Plain Text",
#     "output_type": "Plain Text",
#     "llm_selected": "bigscience/bloomz-560m",
#     "stt_model": "",
#     "stt_features": ""
# }

# st.button("Refresh")
device = "cpu"


@st.cache_resource
def load_data(llm_selected):
    # st.info(f"Loading model: {llm_selected}")
    tokenizer = AutoTokenizer.from_pretrained(llm_selected)
    if "flan" in llm_selected:
        model = AutoModelForSeq2SeqLM.from_pretrained(llm_selected).to(device)
    else:
        model = AutoModelForCausalLM.from_pretrained(llm_selected).to(device)
    # st.success(f"Finished loading model!")

    return tokenizer, model


def get_llm_predictions(utterance: str):
    print(f"Getting response from LLM for the input: {input_}")
    response = call_studio_handler(utterance)['result']
    print("Done!")
    return response


@st.cache_resource
def call_studio_handler(utterance):
    url = "http://localhost:5999/studio_handler"
    payload = json.dumps({
        "input_type": config["input_type"],
        "output_type": config["output_type"],
        "llm_selected": config["llm_selected"],
        "utterance": utterance,
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    print(response)
    return response


if config['input_type'] == "Plain Text" and config['output_type'] == "Plain Text":
    st.subheader(f"Model Selected: ```{config['llm_selected']}```")
    input_ = st.text_area("Input", height=300)
    if input_:
        st.subheader("Response from the LLM:")
        decoded_output = get_llm_predictions(input_)
        st.write(decoded_output)
else:
    st.header("Current Config:")
    st.write(config)
