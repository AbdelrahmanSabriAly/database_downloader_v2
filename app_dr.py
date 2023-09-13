import streamlit as st
import pickle

st.title("Database Downloader ⬇️")

year = st.selectbox("Choose year", ["First Year","Second Year","Third Year","Fourth Year"])
year = year.replace(" ","_")
file_name = f"{year}_database.pkl"
proceed_button = st.button("Proceed")

if proceed_button:
    with open(f'{year}_database.pkl', 'rb') as file:
        existing_dict = pickle.load(file)
    
    st.success(f"There are {len(existing_dict[1])} students")
    st.download_button(
        label="Click here to download the database",
        data=open(file_name, "rb").read(),
        file_name=file_name,
        mime="application/octet-stream",
    )
