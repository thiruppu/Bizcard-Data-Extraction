# BizCardX: Business Card Data Extraction with OCR

BizCardX is a powerful tool designed to simplify the extraction and organization of data from business cards using Optical Character Recognition (OCR) technology. This application leverages Streamlit for the user interface, EasyOCR for text extraction, OpenCV for image processing, and MySQL for data storage.

## Features

- **Easy Upload:** Upload images of business cards in various formats (PNG, JPG, JPEG).
- **Accurate Data Extraction:** Utilizes EasyOCR to accurately extract text from images.
- **Structured Data Output:** Organizes extracted data into categories such as Name, Designation, Company Name, Contact, Email, Website, Address, and Pincode.
- **Visual Display:** Displays the uploaded image and highlights the extracted text for easy verification.
- **Data Management:** Allows modification and deletion of stored business card data.
- **Database Integration:** Stores extracted data in a MySQL database for easy retrieval and management.

## Technology Stack

- **Streamlit:** For building the interactive web application.
- **EasyOCR:** For extracting text from images using deep learning.
- **OpenCV:** For image processing and annotation.
- **Pandas:** For data manipulation and storage.
- **MySQL:** For database management.
- **SQLAlchemy:** For database interaction.

## Installation

1. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up the database:**
   - Ensure MySQL is installed and running on your machine.
   - Create a database named `project03` and a table named `bizcard` with the appropriate schema.

3. **Configure database connection:**
   - Update the `db_config` dictionary in the script with your MySQL credentials.

## Usage

1. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Navigate to the application:**
   - Open your web browser and go to `http://localhost:8501`.

3. **Home:**
   - Provides an overview of the application and its features.

4. **Upload:**
   - Upload a business card image.
   - View the uploaded image and the annotated image with highlighted text.
   - Extract data and upload it to the database.

5. **Modify:**
   - Select a business card by name.
   - Modify the extracted details and update the database.

6. **Delete:**
   - Select a business card by name.
   - Delete the selected business card data from the database.

## Code Structure

- `app.py`: Main application script that contains the Streamlit app configuration, functions for OCR, data extraction, and database operations.
- `requirements.txt`: List of dependencies required to run the application.

## Functions

- `image_ext(image_np)`: Processes the uploaded image with OCR, annotates it, and returns the results along with a DataFrame.
- `extracted_data(details, df2)`: Organizes extracted data into a structured DataFrame.
- `insert_to_sql(df_concat)`: Inserts the extracted data into the MySQL database.
- `names_from_selectbox()`: Retrieves a list of names from the database for the selectbox.
- `show_data()`: Fetches and displays all data from the database.

## Database Configuration

```python
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'project03'
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Special thanks to the developers of Streamlit, EasyOCR, OpenCV, and other open-source libraries used in this project.

Happy coding!
