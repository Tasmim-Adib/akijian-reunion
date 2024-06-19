import streamlit as st
import os
import re
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# MongoDB connection details
MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_CLIENT = os.getenv("MONGODB_CLIENT")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")

client = MongoClient(MONGODB_URL)
database = client[MONGODB_CLIENT]
collection = database[MONGODB_COLLECTION]

# Streamlit app
st.markdown("<h1 style='text-align: center;'>Akijian Reunion (Since 1991)</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color : tomato'>**ফর্মটি পূরণ করার আগে নিচের নির্দেশনাগুলি পড়ে নিন**</p>", unsafe_allow_html=True)
name = st.text_input("Enter your name", value="", help="Give your full name")

whatsapp_number_input = st.text_input("Enter your WhatsApp number", value="+88", help="Give your valid whatsapp number")

batch = st.radio("Label", ('6','7', '8','9','10', 'SSC', 'HSC'), help="This is the label of SSC or HSC")

year = st.selectbox("Select Year", options=list(range(1991, 2025)), help="Which year your batch passed SSC/HSC exam")

whatsapp_pattern = r'^\+88(013|014|015|016|017|018|019)\d{8}$'

def validate_whatsapp_number(number):
    return re.match(whatsapp_pattern, number)


def check_whatsapp_number_unique(number):
    number = clean_whatsapp_number(number)
    return collection.find_one({"no": number}) is None

def clean_whatsapp_number(number):
    return number.replace("+88", "")

error_message = ""

is_loading = False


if st.button("Submit", key='submit_button', disabled=is_loading):

    if not name or not whatsapp_number_input or not batch or not year:
        st.error("সবগুলো ফিল্ড পূরণ করুন")

    elif not validate_whatsapp_number(whatsapp_number_input):
        st.error("WhatsApp number টি সঠিক নয়")

    elif not check_whatsapp_number_unique(whatsapp_number_input):
        st.error("Number টি আগেই ব্যবহার করা হয়েছে")

    else:
        is_loading = True
        
        whatsapp_number = clean_whatsapp_number(whatsapp_number_input)

        student = {
            "na": name,
            "no": whatsapp_number,
            "tg": batch,
            "yr": year
        }

        with st.spinner("Submitting..."):
            collection.insert_one(student)
            st.success("Student profile added successfully!")

            name = ""
            whatsapp_number_input = ""
            education_level = ""
            year = ""


# Display rules
st.markdown("<h4 style='text-align: center;'>নির্দেশনাবলি</h4>", unsafe_allow_html=True)
st.markdown("""
1. এই ফরমটি শুধুমাত্র তথ্য সংগ্রহের জন্য। এটি কোন রেজিস্ট্রেশন ফর্ম নয়।
2. আপনি আকিজ কলেজিয়েট স্কুলে একদিনের জন্যও ভর্তি হয়ে থাকলে আপনি একজন আকিজিয়ান।
3. আপনি SSC ও HSC উভয়ই যদি আকিজ কলেজিয়েট স্কুল থেকে পাশ করে থাকেন তবে আপনার SSC এর পাশের সনটি উল্লেখ করুন।
4. আপনি ভর্তি হয়েছিলেন কিন্তু আকিজ কলেজিয়েট স্কুল থেকে SSC-HSC কোন পরীক্ষায় অংশগ্রহন করেননি। তাহলে আপনি যে ব্যচের সাথে আকিজ কলেজিয়েট স্কুলে ভর্তি হয়েছিলেন 
সেই ব্যচের তথ্য প্রদান করুন।
5. সর্বপরি লিংকটি আপনার পরিচিত আকিজিয়ানদের সাথে শেয়ার করুন।
""")

