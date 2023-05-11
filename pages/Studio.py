import requests
import json
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM

config = st.session_state['config']

st.markdown(f"""<p style='text-align: right; color: rgb(9, 171, 59); font-family: monospace; font-weight: 600; letter-spacing: -0.005em; line-height: 1.2; margin-bottom: 0%;'>
({config['llm_selected']})
</p>""", unsafe_allow_html=True)
st.title("Studio")


# config = {
#     "input_type": "Plain Text",
#     "output_type": "Plain Text",
#     "llm_selected": "bigscience/bloomz-560m",
#     "stt_model": "",
#     "stt_features": ""
# }

# st.button("Refresh")

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
    print(f"Getting response from LLM for the input: {utterance}")
    response = call_studio_handler(utterance, config["llm_selected"])['result']
    if utterance in response:
        response = str(response).replace(utterance, "")
    print("Done!")
    return response


@st.cache_resource
def call_studio_handler(utterance: str, llm_selected: str):
    url = "http://localhost:5999/studio_handler"
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
        st.audio(audio_file_)
        st.write("")
        st.write("")

        st.subheader("Transcript:")

        # TODO: Get transcript from Middleware - Deepgram
        transcript = "Yeah, as much as it's worth celebrating the first spacewalk with an all-female team, " \
                     "I think many of us are looking forward to it just being normal. And I think if it signifies " \
                     "anything, it is to honor the women who came before us who were skilled and qualified and didn't " \
                     "get the same opportunities that we have today."
        input_ = st.text_area("", height=300, label_visibility="collapsed", placeholder=transcript, disabled=True)
        st.write("")
        st.write("")

        # Pass the transcript with prompt to process with LLM
        st.subheader("Prompt:")
        prompt_ = st.text_area(f"Text input:", height=150, label_visibility="collapsed",
                               placeholder="Enter your prompt here...")
        st.write("")

        if prompt_:
            st.write("")
            st.subheader("Output:")
            # TODO: To use get_llm_predictions()
            llm_input = "Context: " + transcript + "\n\n" + prompt_
            decoded_output = get_llm_predictions(llm_input)
            st.write(decoded_output)
else:
    st.header("Current Config:")
    st.write(config)
