import streamlit as st
from streamlit_option_menu import option_menu

import auth, home,history1
import url_summarizer


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title="SwiftScan",
                options=["Home", "Account","History","URL Summarizer"],
                icons=["house-fill", "person-fill","file-text","search"],
                menu_icon="chat-text-fill",
                default_index=1,
                styles={
                    "container": {"padding": "5!important",
                                  "background-color": "transparent"},
                    "icon": {"color": "white",
                             "font-size": "15px"},
                    "nav-link": {"color": "white",
                                 "font-size": "15px",
                                 "text-align": "center"},
                    "nav-link-selected": {"background-color": "#8400ff", }

                }

            )

        if app == "Home":
            home.app()
        if app == "Account":
            auth.app()
        if app == "History":
            history1.app()
        if app == "URL Summarizer":
            url_summarizer.app()


# Create an instance of MultiApp
multi_app = MultiApp()

# Add apps to the MultiApp instance
multi_app.add_app("Home", home.app)
multi_app.add_app("Account", auth.app)

multi_app.add_app("History", history1.app)

multi_app.add_app("URL Summarizer", url_summarizer.app)
# Run the MultiApp instance
multi_app.run()
