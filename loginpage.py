import streamlit as st
import hashlib

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Placeholder for storing registered users (in-memory for simplicity)
users_db = {}

def show_login():
    st.title("Login Page")

    with st.form(key='login_form'):
        st.write("Please enter your login details:")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        login_button = st.form_submit_button("Login")
        if login_button:
            if username in users_db and users_db[username] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("You have successfully logged in!")
                st.write(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password. Please try again.")

    st.write("Don't have an account?")
    if st.button("Register"):
        st.session_state.show_registration = True

def show_registration():
    st.title("Registration Page")

    with st.form(key='registration_form'):
        st.write("Please enter your registration details:")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        register_button = st.form_submit_button("Register")
        if register_button:
            if not username or not password or not confirm_password:
                st.error("All fields are required!")
            elif password != confirm_password:
                st.error("Passwords do not match!")
            elif username in users_db:
                st.error("Username already exists!")
            else:
                users_db[username] = hash_password(password)
                st.success("Registration successful! You can now log in.")
                st.session_state.show_registration = False

    st.write("Already have an account?")
    if st.button("Back to Login"):
        st.session_state.show_registration = False

def show_course_catalog():
    st.title("Course Catalog")
    st.markdown("### Explore Our Courses")

    # Inject custom CSS for course cards
    st.markdown(
        """
        <style>
        .course-card {
            border: 1px solid #ddd;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            background-color: #f9f9f9;
        }
        .course-card:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        .course-title {
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }
        .course-description {
            margin: 10px 0;
            color: #555;
        }
        .course-duration {
            font-weight: bold;
            color: #0072B2;
        }
        .enroll-button {
            background-color: #0072B2;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .enroll-button:hover {
            background-color: #005f8a;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    courses = [
        {"title": "Vocabulary Practice", "description": "Enhance your language skills by mastering new words and their meanings through engaging vocabulary practice.", "duration": "4 weeks"},
        {"title": "Pronunciation Practice", "description": "Improve your spoken clarity and accent with focused pronunciation practice exercises..", "duration": "6 weeks"},
        {"title": "Speech Practice", "description": "Build confidence and fluency in spoken language through targeted speech practice sessions.", "duration": "5 weeks"},
    ]
    
    for course in courses:
        # Using HTML to create styled course cards
        st.markdown(
            f"""
            <div class="course-card">
                <div class="course-title">{course["title"]}</div>
                <div class="course-description">{course["description"]}</div>
                <div class="course-duration">Duration: {course['duration']}</div>
                <button class="enroll-button">Enroll</button>
            </div>
            """,
            unsafe_allow_html=True
        )

def show_user_profile():
    st.title("User Profile")
    st.write(f"**Username:** {st.session_state.username}")
    # Display other user-related information here
    st.write("**Email:** user@example.com")  # Placeholder email
    st.write("**Bio:** Lorem ipsum dolor sit amet, consectetur adipiscing elit.")  # Placeholder bio

def main():
    # Initialize session state to toggle between login, registration, and other views
    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Initialize session state to track page views
    if 'show_course_catalog' not in st.session_state:
        st.session_state.show_course_catalog = False

    if 'show_profile' not in st.session_state:
        st.session_state.show_profile = False

    if st.session_state.logged_in:
        # Inject custom CSS for sidebar buttons
        st.sidebar.markdown(
            """
            <style>
            .sidebar-button {
                display: block;
                width: 100%;
                padding: 10px 20px;
                margin-bottom: 10px;
                background-color: #0072B2;
                color: white;
                border: none;
                border-radius: 10px;
                text-align: center;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s;
            }
            .sidebar-button:hover {
                background-color: #005f8a;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        with st.sidebar:
            st.write("### Welcome, **{}**!".format(st.session_state.username))
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.button("View Profile", key="view_profile"):
                st.session_state.show_course_catalog = False  # Hide course catalog when viewing profile
                st.session_state.show_profile = True  # Show profile on main page
            if st.button("Course Catalog", key="course_catalog"):
                st.session_state.show_profile = False  # Hide profile when viewing course catalog
                st.session_state.show_course_catalog = True  # Set to show course catalog
            if st.button("Logout", key="logout"):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.show_course_catalog = False
                st.session_state.show_profile = False
                st.success("You have been logged out.")

        # Render content based on the selected sidebar option
        if st.session_state.show_course_catalog:
            show_course_catalog()
        elif st.session_state.show_profile:
            show_user_profile()

    elif st.session_state.show_registration:
        show_registration()
    else:
        show_login()

if __name__ == "__main__":
    main()
