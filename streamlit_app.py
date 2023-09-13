import streamlit as st
import subprocess

def start():

    # Define the command you want to run
    command = "streamlit run app.py"

    # Use subprocess to run the command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the process to finish
    stdout, stderr = process.communicate()

    # Check if the command was successful
    if process.returncode == 0:
        print("Streamlit app has started successfully.")
    else:
        print(f"Error running Streamlit app:\n{stderr.decode('utf-8')}")


st.title("FaceLink Attendance")
st.button("Start",on_click=start)