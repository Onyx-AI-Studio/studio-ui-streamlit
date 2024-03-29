import streamlit as st

st.title("Initialize System")
st.write("Configure the Studio UI using the below parameters.")
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
        stt_model = st.radio("Please select the STT model from Deepgram:",
                             ["Deepgram Nova", "Deepgram Whisper [OpenAI]"])

        # 'Smart Format' - "Punctuation", "Numerals", "Paragraphs", "Dates", "Times", "Alphanumerics"
        stt_features = st.multiselect("Pick any of the additional features:",
                                      ["Smart Format", "Diarize",
                                       "Summarize", "Detect Topics", "Profanity Filter",
                                       "Punctuate", "Numerals", "Paragraphs", "Dates", "Times", "Alphanumerics",
                                       ],
                                      default=["Smart Format"])

    submitted = st.form_submit_button("Validate and Set Input Config")
    if submitted and input_type == 'audio':
        st.warning("Please specify additional information")
    elif submitted:
        st.success("Config initialized!")

with st.form("llm_form"):
    st.subheader("LLM Configuration")
    llm = st.selectbox("Pick any of the available large language models:",
                       ["google/flan-t5-base", "google/flan-t5-large", "bigscience/bloomz-560m",
                        "bigscience/bloomz-1b1", "bigscience/bloomz-3b", "bigscience/bloomz-7b",
                        "llama-7b", "vicuna-13b", "Any other model from Huggingface.co"])

    temp_llm = llm
    if llm == "Any other model from Huggingface.co":
        temp_llm = "Any other model from Huggingface.co"
        llm = st.text_input("LLM name from Huggingface:")
    # st.write(temp_llm, llm)

    submitted = st.form_submit_button("Validate and Set Model Config")
    if submitted and str(llm) == "Any other model from Huggingface.co":
        st.info("Please specify a valid model...")
    elif submitted and llm != "":
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
# st.header("JSON Config:")
# st.write(config)
