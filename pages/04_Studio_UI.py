import os

import requests
import json
from pathlib import Path

import streamlit as st
import boto3

config = st.session_state['config']
URL = "http://localhost:5999"

grey = "#EBDBB2"

st.title("Studio UI")
st.write(
    "The ```Config Initializer``` tab in the sidebar can be used to configure things like input/output type, the machine learning models used, etc.")
st.write("")


# config = {
#     "input_type": "Plain Text",
#     "output_type": "Plain Text",
#     "llm_selected": "bigscience/bloomz-560m",
#     "stt_model": "",
#     "stt_features": ""
# }

# st.button("Refresh")


def get_llm_predictions(utterance: str):
    print(f"Getting response from LLM for the input: {utterance}")
    response = call_studio_handler(utterance, config["llm_selected"])['result']
    if utterance in response:
        response = str(response).replace(utterance, "")
    print("Done!")
    return response


@st.cache_resource
def call_studio_handler(utterance: str, llm_selected: str):
    url = URL + "/studio_handler"
    payload = json.dumps({
        "input_type": config["input_type"],
        "output_type": config["output_type"],
        "llm_selected": llm_selected,
        "utterance": utterance,
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    print(response)
    return response


@st.cache_resource
def deepgram_stt(conv_id: str, s3_audio_file_path: str, stt_model: str):
    url = URL + "/stt"
    print(f'Calling studio_handler at: {url}')

    payload = json.dumps({
        "conversation_id": conv_id,
        "s3_audio_file_path": s3_audio_file_path,
        "stt_model": stt_model,
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


# st.subheader(f"Model selected: ```{config['llm_selected']}```")

if config['input_type'] == "Plain Text" and config['output_type'] == "Plain Text":
    prompt_ = st.text_area(f"Text input:", height=400, label_visibility="collapsed",
                           placeholder="Enter your input here...")
    if prompt_:
        st.write("")
        st.subheader("Output:")
        decoded_output = get_llm_predictions(prompt_)
        st.write(decoded_output)
elif config['input_type'] == "Audio":
    audio_file_ = st.file_uploader("Audio File Upload", type=["mp3", "wav"],
                                   help="Upload an audio file of the allowed formats to process")

    if audio_file_:
        # Save uploaded file
        save_folder = '/Users/snehalyelmati/Documents/studio-ui-streamlit/audio_files'
        save_path = Path(save_folder, st.session_state['conv_id'])
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        save_path = Path(save_path, audio_file_.name)

        with open(save_path, mode='wb') as w:
            w.write(audio_file_.getvalue())

        if save_path.exists():
            print(f'File {audio_file_.name} is successfully saved!')

        s3 = boto3.resource("s3")

        # Upload a new file
        data = open(save_path, 'rb')
        s3_path = 'audio_files/' + st.session_state['conv_id'] + '_' + audio_file_.name
        s3.Bucket('onyx-test-001').put_object(Key=s3_path, Body=data)
        st.success(f'File {audio_file_.name} is successfully uploaded to AWS S3!')

        st.audio(audio_file_)
        st.write("")
        st.write("")

        st.subheader("Transcript:")

        deepgram_response = deepgram_stt(st.session_state['conv_id'], str(s3_path), config['stt_model']).json()
        transcript = deepgram_response['verbatim']

        st.write(transcript)
        st.write("")
        st.write("")

        # Pass the transcript with prompt to process with LLM
        st.subheader("Prompt:")
        prompt_ = st.text_area(f"Text input:", height=150, label_visibility="collapsed",
                               placeholder="Enter your prompt here...")
        st.write("")

        if prompt_:
            st.subheader("Output:")
            llm_input = "Context: " + transcript + "\n\n" + prompt_
            decoded_output = get_llm_predictions(llm_input)
            st.write(decoded_output)
            st.write("")
            st.write("")
else:
    st.header("Current Config:")
    st.write(config)

st.markdown(f"""<p style='text-align: right; color: {grey}; font-family: monospace; font-weight: 600; letter-spacing: -0.005em; line-height: 1.2; margin-top: 0%'>
({config['llm_selected']})
</p>""", unsafe_allow_html=True)
