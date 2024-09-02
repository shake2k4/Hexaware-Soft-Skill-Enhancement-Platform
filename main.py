import streamlit as st
from streamlit_option_menu import option_menu
import loginpage

st.set_page_config(
    page_title="Soft Skill Enhancement Platform",
    layout="wide"  # Make the layout wide so that the header spans across the page
)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        # Full-width header
        st.markdown(
            """
            <style>
            .full-header {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: #0072B2;
                color: white;
                text-align: center;
                padding: 10px 0;
                font-size: 24px;
                font-weight: bold;
                z-index: 9999;
            }

            .stApp {
                margin-top: 50px;
            }

            .sidebar .sidebar-content {
                margin-top: 60px; /* Adjust this value to move the sidebar down */
            }
            </style>
            <div class="full-header">
                Soft Skill Enhancement Platform
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.sidebar:
            app = option_menu(
                menu_title='User Credentials',
                options=['Login'],  # Only 'Login' option is available
                icons=['person-circle'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )
        if app == 'Login':
            loginpage.main()

# Initialize and run the app
app = MultiApp()
app.run()
