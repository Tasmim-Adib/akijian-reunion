import streamlit as st
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection details
MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_CLIENT = os.getenv("MONGODB_CLIENT")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")

client = MongoClient(MONGODB_URL)
database = client[MONGODB_CLIENT]
collection = database[MONGODB_COLLECTION]

st.markdown("<h1 style='text-align: center;'>Akijian Reunion (Since 1991)</h1>", unsafe_allow_html=True)


search_batch = st.selectbox("Label", ('6', '7', '8', '9', '10', 'SSC', 'HSC'), help="Please choose a class or degree")
search_year = st.selectbox("Select Year", options=list(range(1991, 2025)), help="Which year your batch passed SSC/HSC exam")

if st.button("Search", key = "search_student_button"):
    if not search_batch or not search_year:
        st.error("সবগুলো ফিল্ড পূরণ করুন")

    students = list(collection.find({"tg": search_batch, "yr": search_year}, {"_id": 0, "na": 1}))
    total_students = len(students)
    
    st.markdown(f"**Label:** {search_batch}")
    st.markdown(f"**Year:** {search_year}")
    st.markdown(f"**Total Students:** {total_students}")
    
    if total_students > 0:
        st.markdown("**Students List:**")
        student_list = "\n".join([f"{index + 1}. {student['na']}" for index, student in enumerate(students)])
        st.markdown(student_list)
    else:
        st.error("No students found.")

