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


@st.cache_resource
def get_llm_predictions(utterance: str, llm_selected: str):
    url = "http://localhost:5999/llm_predict"

    payload = json.dumps({
        "utterance": utterance,
        "llm_selected": llm_selected,
    })
    headers = {
        'Content-Type': 'application/json'
    }
    return requests.request("POST", url, headers=headers, data=payload)


if config['input_type'] == "Plain Text" and config['output_type'] == "Plain Text":
    st.subheader(f"Model Selected: ```{config['llm_selected']}```")

    input_ = st.text_area("Input", height=300)
    llm_selected = config['llm_selected']

    if input_:
        st.subheader("Response from the LLM:")

        print(f"Getting response from LLM for the input: {input_}")
        response = get_llm_predictions(input_, llm_selected)
        print("Done!")
        print(response.json())
        decoded_output = response.json()['result']

        st.write(decoded_output)
else:
    st.header("Current Config:")
    st.write(config)
