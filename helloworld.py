import streamlit as st

st.title("👋 Hello Streamlit Cloud!")
st.write("If you can see this, your app is working perfectly 🎉")

name = st.text_input("What's your name?")
if name:
    st.success(f"Welcome, {name}!")
