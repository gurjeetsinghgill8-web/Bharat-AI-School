import streamlit as st
import db

def login_user(email, password):
    if not hasattr(db, 'supabase') or not db.supabase:
        st.error("🚨 Database connection is missing! (चेक करें कि db.py सही से सेव हुई है या नहीं)")
        return False, None
        
    try:
        response = db.supabase.table("users").select("*").eq("email", email).execute()
        
        if len(response.data) > 0:
            user = response.data[0]
            if user.get('password_hash') == password: 
                return True, user['username']
            else:
                st.error("❌ Incorrect password.")
                return False, None
        else:
            st.error("❌ Email not found. Please Sign Up first.")
            return False, None
            
    except Exception as e:
        st.error(f"🚨 Supabase Database Error (Login): {str(e)}")
        return False, None

def signup_user(username, email, password):
    if not hasattr(db, 'supabase') or not db.supabase:
        st.error("🚨 Database connection is missing!")
        return False, None
        
    try:
        data = {
            "username": username,
            "email": email,
            "password_hash": password,
            "role": "Student"
        }
        response = db.supabase.table("users").insert(data).execute()
        st.success("✅ Signup Successful! Please switch to the Login tab.")
        return True, username
        
    except Exception as e:
        st.error(f"🚨 Supabase Database Error (Signup): {str(e)}")
        return False, None

def main():
    st.title("Bharat AI School 🏫")
    st.markdown("Welcome to the future of learning.")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login to Your Account")
        email = st.text_input("Email ID", key="log_email")
        password = st.text_input("Password", type="password", key="log_pass")
        if st.button("Login", type="primary"):
            success, username = login_user(email, password)
            if success:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
                
    with tab2:
        st.subheader("Create New Account")
        new_user = st.text_input("Username", key="reg_user")
        new_email = st.text_input("Email ID", key="reg_email")
        new_pass = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Sign Up", type="primary"):
            if new_user and new_email and new_pass:
                signup_user(new_user, new_email, new_pass)
            else:
                st.warning("Please fill in all details.")

if __name__ == "__main__":
    main()