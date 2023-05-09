import streamlit as st

st.title("🎬 Generative AI Studio")

st.header("Initialize System")
with st.form("input_form"):
    st.subheader("Input and Output Configuration")

    input_output_container = st.container()

    with input_output_container:
        input_col, output_col = st.columns(2)
        with input_col:
            input_type = st.radio("Supported input types:", ["Plain Text", "Audio", "PDF", "Text File"])

        with output_col:
            output_type = st.radio("Supported output types:", ["Plain Text", "Audio"])

    stt_model = ""
    stt_features = ""
    if input_type == "Audio":
        st.subheader("Speech-To-Text Configuration")

        # TODO:
        #  Add config for the models like tiny or large for Whisper
        #  Add config for Nova - Enhanced
        stt_model = st.radio("Please select the STT model from Deepgram:", ["Deepgram Nova", "OpenAI Whisper"])

        stt_features = st.multiselect("Pick any of the additional features:",
                                      ["Diarization", "Punctuation", "Topic Detection", "Keyword Extraction"])

    submitted = st.form_submit_button("Validate and Set Input Config")
    if submitted and input_type == 'audio':
        st.warning("Please specify additional information")
    elif submitted:
        st.success("Config initialized!")

with st.form("llm_form"):
    st.subheader("LLM Configuration")
    llm = st.selectbox("Pick any of the available large language models:",
                       ["google/flan-t5-large", "bigscience/bloomz-560m", "bigscience/bloomz-1b1", "bigscience/bloomz-3b", "bigscience/bloomz-7b",
                        "llama-7b", "vicuna-13b", "other"])

    temp_llm = llm
    if llm == "other":
        temp_llm = "other"
        llm = st.text_input("LLM name from Huggingface:")

    # FIXME: logical flow to handle all scenarios
    submitted = st.form_submit_button("Validate and Set Model Config")
    if submitted and temp_llm == "other":
        # st.write("Please specify a valid model!")
        st.info("Please specify a valid model...!")
    elif submitted and input_type == "audio":
        # st.write("Please specify the STT engine!")
        st.info("Please specify the STT engine!")
    elif submitted and llm != "other":
        # and (input_type == "audio" and stt_model != ""):
        # st.write("Config initialized!")
        st.success("Config initialized!")
    else:
        st.write()

# st.divider()
config = {
    'input_type': input_type,
    'output_type': output_type,
    'llm_selected': llm,
    'stt_model': stt_model,
    'stt_features': stt_features,
}
st.session_state['config'] = config

# debug logs
st.header("JSON Config:")
st.write(config)
