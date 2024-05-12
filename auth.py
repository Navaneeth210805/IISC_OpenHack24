import streamlit as st
import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import auth


def app():
    try:
        # Attempt to initialize Firebase
        private_key = os.environ.get("PRIVATE_KEY")
        type=os.environ.get("TYPE")
        client_email = os.environ.get("CLIENT_EMAIL")
        client_id = os.environ.get("CLIENT_ID")
        auth_uri = os.environ.get("AUTH_URI")
        token_uri = os.environ.get("TOKEN_URI")
        auth_provider_x509_cert_url = os.environ.get("AUTH_PROVIDER_URI")
        client_x509_cert_url = os.environ.get("CLIENT_URI")
        universe_domain = os.environ.get("DOMAIN")
        Project = os.environ.get("project_id")
        PRIVATE_KEY_ID= os.environ.get("PRIVATE_KEY_ID")
        service_account_info = {
            "type": type,
            "project_id":Project,
            "private_key_id": PRIVATE_KEY_ID,
            "private_key": private_key,
            "client_email": client_email,
            "client_id": client_id,
            "auth_uri": auth_uri,
            "token_uri": token_uri,
            "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
            "client_x509_cert_url": client_x509_cert_url,
            "universe_domain": universe_domain
        }
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)
    except ValueError:
        # Firebase has already been initialized
        pass
    st.title("Welcome to SwiftScan")

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def f():
        try:
            user = auth.get_user_by_email(email)
            # print(user.uid)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email

            global Usernm
            Usernm = (user.uid)

            st.session_state.signedout = True
            st.session_state.signout = True


        except:
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False

    if not st.session_state["signedout"]:  # only show if the state is False, hence the button has never been clicked
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        if choice == 'Sign up':
            username = st.text_input("Enter  your unique username")

            if st.button('Create my account'):
                user = auth.create_user(email=email, password=password, uid=username)

                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()
        else:
            # st.button('Login', on_click=f)
            st.button('Login', on_click=f)

    if st.session_state.signout:
        st.text('Name ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        st.button('Sign out', on_click=t)


def ap():
    st.write('Posts')
