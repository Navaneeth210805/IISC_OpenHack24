import duck
import history
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder, speech_to_text
import streamlit as st
import os
import google.generativeai as genai
from langchain.chains.summarize import load_summarize_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoConfig, pipeline
from dotenv import load_dotenv
from firebase_admin import firestore
import spacy
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

previous = ""

content_generated = False
p=[]

def app():
    state = st.session_state
    x = []
    x = history.history("", "", "")
    ph = ''
    if st.session_state.username == '':
        ph = 'Login to be able to post!!'
    translate_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
    tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

    def summarize_text(search, selected_language):
        content=False
        response = model.generate_content(f"Search and provide information on {search} on as a multiple paragraphs not as points and if you are not able to output any details just return No response")
        relevant_links = duck.set_search_query(search_query=search)
        if 'No response' in response:
            llm = ChatGoogleGenerativeAI(temperature=0, model='gemini-pro')
            loader = WebBaseLoader(relevant_links[0])
            docs = loader.load()
            chain = load_summarize_chain(llm, chain_type='stuff')
            response = chain.run(docs)
            content = True
        try:
            if content:
                nlp = spacy.load("en_core_web_lg")
                doc = nlp(response)
                named_entities = [ent.text for ent in doc.ents]
                response = model.generate_content(f"Search and provide information on as a multiple paragraphs not as points {search} using the keywords in {named_entities} bolded")
            else:
                nlp = spacy.load("en_core_web_lg")
                doc = nlp(response.text)
                named_entities = [ent.text for ent in doc.ents]
                response = model.generate_content(f"Search and provide information on as a multiple paragraphs not as points {search} using the keywords in {named_entities} bolded")
        except:
            pass
        llm = ChatGoogleGenerativeAI(temperature=0, model='gemini-pro')
        text_splitter = CharacterTextSplitter()
        texts = text_splitter.split_text(response.text)
        docs = [Document(page_content=text) for text in texts]
        chain = load_summarize_chain(llm, chain_type='map_reduce')
        summarized_response = chain.run(docs)
        translated_summary=''
        var=False
        if selected_language != 'English':
            summary_translator = pipeline('translation', model=translate_model, tokenizer=tokenizer,
                                          src_lang='en', tgt_lang=select_language[selected_language])

            translated_summary = summary_translator(summarized_response)
            st.markdown(f"Summarized content in {selected_language} : ")
            st.chat_message('assistant').markdown(
                translated_summary[0].get("translation_text"))
            var=True

        else:
            st.chat_message('assistant').markdown("*Summarized response*")
            st.markdown(summarized_response)

        relevant_links = duck.set_search_query(search_query=search)
        search = 'Summarized content on ' + search
        if var:
            x = history.history(search, translated_summary, relevant_links)
        else:
            x = history.history(search, summarized_response, relevant_links)
        if 'db' not in state:
            state.db = ''
        db = firestore.client()
        state.db = db

        if search != "":
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

    def llm_output(search, voice_text, selected_language):
        global content_generated
        target_lang = select_language[selected_language]
        translator = pipeline('translation', model=translate_model, tokenizer=tokenizer, src_lang="en"
                              , tgt_lang=target_lang, max_length=1024)

        if voice_text:
            search = voice_text
        elif search == "":
            search = "What is LLM?"
            content_generated = False
        content=False
        st.chat_message("user").markdown(search)
        response = model.generate_content(f"Search and provide information on {search} on as a multiple paragraphs not as points and if you are not able to output any details just return No response")
        relevant_links = duck.set_search_query(search_query=search)
        if 'No response' in response:
            llm = ChatGoogleGenerativeAI(temperature=0, model='gemini-pro')
            loader = WebBaseLoader(relevant_links[0])
            docs = loader.load()
            chain = load_summarize_chain(llm, chain_type='stuff')
            response = chain.run(docs)
            content=True
        try :
            if content:
                nlp = spacy.load("en_core_web_lg")
                doc = nlp(response)
                named_entities = [ent.text for ent in doc.ents]
                response = model.generate_content(f"Search and provide information on as a multiple paragraphs not as points {search} using the keywords in {named_entities} bolded")
            else:
                nlp = spacy.load("en_core_web_lg")
                doc = nlp(response.text)
                named_entities = [ent.text for ent in doc.ents]
                response = model.generate_content(f"Search and provide information on as a multiple paragraphs not as points {search} using the keywords in {named_entities} bolded")
        except:
            pass
        var=False
        translated_text=''
        if not selected_language:
            selected_language = "English"
        elif selected_language == "English":
            st.chat_message("assistant").markdown(response.text)
        else:
            translated_text_array = []
            for i in range(0, len(response.text), 200):
                translated_text = translator(response.text[i:i + 200])
                translated_text_array.append(translated_text)
                var=True
            st.chat_message('assistant').markdown(f"*Translation into {selected_language}*")
            for i in translated_text_array:
                st.markdown(i[0].get('translation_text'))



        st.write("Relevant Links : ")
        html_for_relevant_links = ("<ul>" + "".join(f"<li><a href='{link}'>{link}</a></li>" for link in relevant_links)
                                   + "</ul>")
        st.write(html_for_relevant_links, unsafe_allow_html=True)
        if var:
            x = history.history(search_query, translated_text, relevant_links)
        else:
            x = history.history(search_query, response.text, relevant_links)
        global previous
        previous = search  # Return the updated value of search
        content_generated = True
        if 'db' not in state:
            state.db = ''
        db = firestore.client()
        state.db = db

        if search_query != "":
            username = state.username  # Make sure state.username is defined
            doc_ref = db.collection('History').document(username)
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

    global previous
    search_query = st.text_input("Ask a question")
    search_btn = st.button("Search", use_container_width=20)
    if not search_btn:
        search_query = ""
    st.write("Audio Input :")
    text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')
    if text is not None:
        previous = text
    elif search_query:
        previous = search_query
    select_language = {
        "English": "English",
        "Tamil": "tam_Taml",
        "Telugu": "tel_Telu",
        "Kannada": "kan_Knda",
        "Malayalam": "mal_Mlym",
        "Hindi": "hin_Deva"
    }

    selected_lang = st.sidebar.selectbox("Choose a language", list(select_language.keys()))

    global content_generated
    if search_btn or text:
        llm_output(previous, previous, selected_lang)

    if content_generated and st.button("Summarize", use_container_width=20):
        summarize_text(previous, selected_lang)
