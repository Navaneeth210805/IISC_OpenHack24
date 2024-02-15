import streamlit as st
from firebase_admin import firestore

def app():
    db = firestore.client()

    try:
        st.title('Search History')

        result = db.collection('History').document(st.session_state['username']).get().to_dict()
        questions = result['Questions']
        response = result['Responses']

        def delete_post(k):
            c = int(k)
            h = questions[c]
            try:
                updated_questions = questions[:c] + questions[c + 1:]
                updated_response = response[:c] + response[c + 1:]

                db.collection('History').document(st.session_state['username']).update({"Questions": updated_questions})
                db.collection('History').document(st.session_state['username']).update({"Responses": updated_response})

                st.warning('Post Deleted')
            except:
                st.warning('Something went wrong...')

        for c in range(len(questions) - 1, -1, -1):
            st.text_area(label="Question", value=questions[c])
            st.text_area(label="Responses", value=response[c])
            st.button("Delete Question", on_click=delete_post, args=(c,), key=c)
    except:
        if st.session_state['username'] == '':
            st.write('Login with username')
