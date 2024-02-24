import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoConfig, pipeline
import google.generativeai as genai
import os
from dotenv import load_dotenv
import history
from firebase_admin import firestore
load_dotenv()

genai.configure(api_key=os.getenv("AIzaSyA3teT3iVBatc3sM-9Q3WhZ9GfB3fCUP-w"))
model = genai.GenerativeModel('gemini-pro')


def app():

    def url_summarizer(url, selected_language="English"):
        if url == "":
            st.markdown("Please enter a valid URL")
            return 1
        llm = ChatGoogleGenerativeAI(temperature=0, model='gemini-pro')
        loader = WebBaseLoader(url)
        docs = loader.load()
        chain = load_summarize_chain(llm, chain_type='stuff')
        st.chat_message('user').markdown(f"***Summarize content from {url}***")
        summarized_from_url = chain.run(docs)
        st.chat_message('assistant').markdown(summarized_from_url)

        if selected_language != "English":
            translate_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
            tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

            url_summary_translator = pipeline('translation', model=translate_model, tokenizer=tokenizer,
                                              src_lang='en', tgt_lang=select_language[selected_language])

            translated_url_summary = url_summary_translator(summarized_from_url)
            st.chat_message('assistant').markdown(f"Summary of the provided URL in {selected_language}")
            st.chat_message('assistant').markdown(translated_url_summary)
        state = st.session_state
        x = []
        ph = ''
        if st.session_state.username == '':
            ph = 'Login to be able to post!!'
        x = history.history( url, summarized_from_url , url)
        if 'db' not in state:
            state.db = ''
        db = firestore.client()
        state.db = db
        if url != "":
            username = state.username  # Make sure state.username is defined
            # doc_ref = db.collection('History').document(username)
            doc_ref = db.collection('History').document(username.strip())

            info = doc_ref.get()
            if info.exists:
                info_dict = info.to_dict()
                questions = info_dict.get('Questions', [])
                responses = info_dict.get('Responses', [])
                questions.append(x[-1][0])
                responses.append(x[-1][1])
                doc_ref.update({
                    'Questions': firestore.ArrayUnion([x[-1][0]]),
                    'Responses': firestore.ArrayUnion([x[-1][1]]),
                })
            else:
                data = {
                    "Questions": [x[-1][0]],
                    'Responses': [x[-1][1]],
                    'UserName': username
                }
                doc_ref.set(data)
        return 0

    select_language = {
        "English": "English",
        "Tamil": "tam_Taml",
        "Telugu": "tel_Telu",
        "Kannada": "kan_Knda",
        "Malayalam": "mal_Mlym",
        "Hindi": "hin_Deva"
    }

    selected_lang = st.sidebar.selectbox("Choose a language", list(select_language.keys()))

    url_query = st.text_input("Enter a URL to summarize", placeholder="URL :")

    url_search_btn = st.button("Summarize URL")

    if not url_search_btn:
        url_query = ""
    url_summarizer(url_query, selected_lang)
