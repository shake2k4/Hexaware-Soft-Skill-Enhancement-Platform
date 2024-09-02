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
    st.markdown(
        """
        <style>
        .course-card {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .course-title {
            font-size: 18px;
            font-weight: bold;
        }
        .course-description {
            margin: 10px 0;
        }
        .course-duration {
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Course Catalog")
    st.markdown("### Explore Our Courses")
    
    courses = [
        {"title": "Introduction to Python", "description": "Learn the basics of Python programming.", "duration": "4 weeks"},
        {"title": "Data Science Fundamentals", "description": "Understand the fundamentals of data science.", "duration": "6 weeks"},
        {"title": "Web Development with Streamlit", "description": "Build web apps using Streamlit.", "duration": "5 weeks"},
    ]
    
    for course in courses:
        st.markdown(
            f"""
            <div class="course-card">
                <div class="course-title">{course["title"]}</div>
                <div class="course-description">{course["description"]}</div>
                <div class="course-duration">**Duration:** {course['duration']}</div>
                <button class="course-enroll-button" style="background-color: #0072B2; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;">
                    Enroll
                </button>
            </div>
            """,
            unsafe_allow_html=True
        )

def show_user_profile():
    st.title("User Profile")
    st.write(f"Username: {st.session_state.username}")
    st.write("Email: user@example.com")
    # Add more profile-related content here

def main():
    # Initialize session state to toggle between login and registration
    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if 'show_profile' not in st.session_state:
        st.session_state.show_profile = False

    if st.session_state.logged_in:
        # Add header with "View Profile" and "Logout" buttons, positioned slightly lower
        st.markdown(
            """
            <style>
            .header {
                position: fixed;
                top: 60px; /* Adjust this value to move the header lower */
                left: 0;
                width: 100%;
                background-color: #C0C0C0; /* Light grey color */
                color: black;
                text-align: center;
                padding: 10px 20px;
                font-size: 24px;
                z-index: 9999;
                display: flex;
                justify-content: center; /* Center the title */
                align-items: center;
            }
            .header-buttons {
                position: absolute;
                right: 20px;
                display: flex;
                gap: 10px;
            }
            .header-button {
                background-color: #ffffff;
                color: #0072B2;
                border: none;
                padding: 4px 8px; /* Reduced size */
                border-radius: 20px; /* Rounded corners */
                cursor: pointer;
                font-size: 14px; /* Adjust font size */
            }
            .header-button:hover {
                background-color: #e0e0e0;
            }
            .stApp {
                margin-top: 120px; /* Adjust this value to ensure content starts below the header */
            }
            </style>
            <div class="header">
                <div>Soft Skill Enhancement Platform</div>
                <div class="header-buttons">
                    <button class="header-button" onclick="window.location.href='?show_profile=true';">Profile</button>
                    <button class="header-button" onclick="window.location.href='?logout=true';">Logout</button>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Handle query parameters for logout and profile
        query_params = st.experimental_get_query_params()
        if 'logout' in query_params:
            st.session_state.logged_in = False
            st.session_state.show_profile = False
            st.experimental_rerun()

        if 'show_profile' in query_params:
            st.session_state.show_profile = True

        if st.session_state.show_profile:
            show_user_profile()
        else:
            show_course_catalog()

    elif st.session_state.show_registration:
        show_registration()
    else:
        show_login()

if __name__ == "__main__":
    main()
 