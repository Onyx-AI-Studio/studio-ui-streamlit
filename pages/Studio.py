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


if config['input_type'] == "Plain Text" and config['output_type'] == "Plain Text":
    st.header(f"Chatbot: {config['llm_selected']}")
    tokenizer, model = load_data(config['llm_selected'])

    input_ = st.text_area("Input", height=300)

    if input_:
        st.header("Response from the LLM:")

        with st.spinner():
            inputs = tokenizer(str(input_), return_tensors="pt")["input_ids"].to(device)
            # inputs = tokenizer('A cat in French is "', return_tensors="pt")["input_ids"].to(device)
            outputs = model.generate(inputs, max_length=1000)
            decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
            st.write(decoded_output)
else:
    st.header("Current Config:")
    st.write(config)
