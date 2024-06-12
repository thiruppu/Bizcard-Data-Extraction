import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import cv2
from streamlit_option_menu import option_menu
import re
import pandas as pd
import io
import mysql.connector as SQLC
from sqlalchemy import create_engine
import sqlite3

# Database configuration
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'project03'
}
mydb = SQLC.connect(**db_config)

# Create a cursor object
cursor = mydb.cursor()

# SQLAlchemy engine for pandas to_sql function
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

# Initialize EasyOCR reader globally
reader = easyocr.Reader(['en'])

def image_ext(image_np):
    details = []

    # Perform OCR on the image
    results = reader.readtext(image_np)
    for i in results:
        details.append(i[1])
    
    for (bbox, text, prob) in results:
        # Unpack the bounding box
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))

        # Draw the bounding box
        cv2.rectangle(image_np, top_left, bottom_right, (0, 255, 0), 2)

        # Put the recognized text
        cv2.putText(image_np, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    # Convert the annotated image back to PIL format for display in Streamlit
    annotated_image_pil = Image.fromarray(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
    
    # Image to Bytes
    image_bytes = io.BytesIO()
    annotated_image_pil.save(image_bytes, format="PNG")
    image_data = image_bytes.getvalue()

    io_data = {"IMAGE": [image_data]}
    df2 = pd.DataFrame(io_data)
    
    return results, details, annotated_image_pil, df2

def extracted_data(details, df2):
    extd_dict = {"NAME": [], "DESIGNATION": [], "COMPANY_NAME": [], "CONTACT": [], "EMAIL": [], "WEBSITE": [], "ADDRESS": [], "CITY": [], "STATE": [], "PINCODE": []}

    if details:
        extd_dict["NAME"].append(details[0])
        if len(details) > 1:
            extd_dict["DESIGNATION"].append(details[1])

    for i in range(2, len(details)):
        if details[i].startswith("+") or (details[i].replace("-", "").isdigit() and '-' in details[i]):
            extd_dict["CONTACT"].append(details[i])
        elif "@" in details[i] and ".com" in details[i]:
            extd_dict["EMAIL"].append(details[i])
        elif "www" in details[i].lower():
            extd_dict["WEBSITE"].append(details[i].lower())
        elif re.match(r'^\d{6}$', details[i]):
            extd_dict["PINCODE"].append(details[i])
        elif re.match(r'^[A-Za-z]', details[i]):
            extd_dict["COMPANY_NAME"].append(details[i])
        else:
            remove_colon = re.sub(r'[,;]', '', details[i])
            extd_dict["ADDRESS"].append(remove_colon)
    
    for key, value in extd_dict.items():
        if value:
            extd_dict[key] = [" ".join(value)]
        else:
            extd_dict[key] = ["NA"]

    df = pd.DataFrame(extd_dict)
    df_concat = pd.concat([df, df2], axis=1) 
    return df_concat

def insert_to_sql(df_concat):
    df_concat.to_sql('bizcard', con=engine, if_exists='append', index=False)

def names_from_selectbox():
    cursor.execute("SELECT NAME FROM bizcard")
    names = cursor.fetchall()
    name_list = [name[0] for name in names]  # Extract names from tuples
    return name_list

def show_data():
    cursor.execute("SELECT * FROM bizcard")
    data_table = cursor.fetchall()
    return data_table

# Streamlit App Configuration
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color:#393f4d;
        color: #431c5d;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp div {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    select = option_menu("Main Menu", ["Home", "Upload", "Modify", "Delete"])

if select == "Home":
    st.title("BizCardX:")
    st.subheader("Extracting Business Card Data with OCR")
    st.markdown("""
    ## About BizCardX
    BizCardX is an innovative tool designed to simplify the process of extracting and organizing data from business cards using Optical Character Recognition (OCR) technology. With BizCardX, you can effortlessly digitize your physical business cards and manage your contact information more efficiently.

    ## Features
    - **Easy Upload**: Upload images of business cards in various formats (PNG, JPG, JPEG).
    - **Accurate Data Extraction**: Utilizes EasyOCR to accurately extract text from images.
    - **Structured Data Output**: Organizes extracted data into categories such as Name, Designation, Company Name, Contact, Email, Website, Address, and Pincode.
    - **Visual Display**: Displays the uploaded image and highlights the extracted text for easy verification.

    ## How to Use
    1. **Upload Image**: Click on the "Choose the Image to upload" button to upload a business card image.
    2. **View Uploaded Image**: The uploaded image will be displayed on the left side of the screen.
    3. **Extract Data**: The extracted data will be shown on the right side of the screen in a structured format.
    4. **Highlighted Text**: The extracted text will be highlighted on the image for easy cross-reference.

    ## Supported Formats
    - PNG
    - JPG
    - JPEG

    ## Technology
    BizCardX leverages powerful technologies to provide accurate and efficient data extraction:
    - **Streamlit**: For building the interactive web application.
    - **EasyOCR**: For extracting text from images using deep learning.
    - **OpenCV**: For image processing and annotation.

    ## Benefits
    - **Efficiency**: Save time by quickly digitizing business cards.
    - **Accuracy**: Reduce errors with accurate text extraction.
    - **Organization**: Keep your contacts organized and easily accessible.
    - **Convenience**: Access your digitized contacts anytime, anywhere.

    ## Get Started
    To begin using BizCardX, simply upload an image of a business card and let the app do the rest. Experience the convenience of having all your important contact information at your fingertips.

    For any questions or feedback, feel free to reach out to us at [support@bizcardx.com](mailto:support@bizcardx.com).

    Happy Networking!
    """)
elif select == "Upload":
    st.title("BizCardX:")
    st.subheader("Extracting Business Card Data with OCR")
    st.markdown("<h4>Data Extraction:</h4>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose the Image to upload", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Read the image file buffer with PIL
        image = Image.open(uploaded_file)

        # Display the uploaded image
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Uploaded Image")

        # Convert the image to a format suitable for EasyOCR and OpenCV
        image_np = np.array(image)
        image_cv2 = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # OCR processing
        results, details, annotated_image, df2 = image_ext(image_cv2)

        # Extracting and displaying the results
        with col2:
            st.image(annotated_image, caption="Annotated Image")
        st.success("Text is Extracted Successfully")

        # Display extracted data
        extracted_info = extracted_data(details, df2)
        st.dataframe(extracted_info)
        upload_button = st.button("Upload data")
        if upload_button:
            insert_to_sql(extracted_info)
            st.success("Data Uploaded to DB")
        st.divider()
elif select == "Modify":
    st.title("BizCardX:")
    st.subheader("Extracting Business Card Data with OCR")
    st.markdown("<h4>Data Modification:</h4>", unsafe_allow_html=True)

    name_list_selectbox = names_from_selectbox()
    selected_name = st.selectbox("Select Name to Modify:", name_list_selectbox)
    
    if selected_name:
        cursor.execute("SELECT * FROM bizcard WHERE NAME = %s", (selected_name,))
        row = cursor.fetchone()
        if row:
            new_name = st.text_input("Name", value=row[0])
            new_designation = st.text_input("Designation", value=row[1])
            new_company_name = st.text_input("Company Name", value=row[2])
            new_contact = st.text_input("Contact", value=row[3])
            new_email = st.text_input("Email", value=row[4])
            new_website = st.text_input("Website", value=row[5])
            new_address = st.text_input("Address", value=row[6])
            new_city = st.text_input("City", value=row[7])
            new_state = st.text_input("State", value=row[8])
            new_pincode = st.text_input("Pincode", value=row[9])

            if st.button("Update Data"):
                cursor.execute("""
                    UPDATE bizcard SET NAME=%s, DESIGNATION=%s, COMPANY_NAME=%s, CONTACT=%s, EMAIL=%s, WEBSITE=%s, ADDRESS=%s, CITY=%s, STATE=%s, PINCODE=%s
                    WHERE NAME=%s
                """, (new_name, new_designation, new_company_name, new_contact, new_email, new_website, new_address, new_city, new_state, new_pincode, selected_name))
                mydb.commit()
                st.success("Data Updated Successfully")
            if st.button("Show Data"):
                df2=show_data()
                st.dataframe(df2)

elif select == "Delete":
    st.title("BizCardX:")
    st.subheader("Extracting Business Card Data with OCR")
    st.markdown("<h4>Data Deletion:</h4>", unsafe_allow_html=True)

    name_list_selectbox = names_from_selectbox()
    selected_name = st.selectbox("Select Name to Delete:", name_list_selectbox)
    
    if selected_name and st.button("Delete Data"):
        cursor.execute("DELETE FROM bizcard WHERE NAME=%s", (selected_name,))
        mydb.commit()
        st.success("Data Deleted Successfully")
    if st.button("Show Data"):
        df2=show_data()
        st.dataframe(df2)

# Close the cursor and database connection at the end
cursor.close()
mydb.close()