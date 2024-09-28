from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Set up Google Sheets API
def connect_to_google_sheet():
    scopes = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]


    creds=Credentials.from_service_account_file("creadentials.json",scopes=scopes)
    client=gspread.authorize(creds)
    sheet_id="1cOxBdqI5X-l6ZsjdkIPT7C7bz-Oq2-pV7BycH-Ptm84"

    sheet=client.open_by_key(sheet_id)

    values_list=sheet.sheet1.row_values(1)
    print(values_list)
    work_sheet=sheet.sheet1
    return work_sheet

@app.route('/')
def home():
    return "API is running!"

# Function to check and add column names if they don't exist
def ensure_column_headers(worksheet):
    # Get all values in the first row (this will return an empty list if the sheet is empty)
    first_row = worksheet.row_values(1)
    
    # If the first row is empty, we need to add the headers
    if not first_row:
        # Add headers: Name, Address, Contact, Email
        worksheet.append_row(['Name', 'Address', 'Contact', 'Email'])

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        # Extract data from the request
        name = request.json.get('name')
        address = request.json.get('address')
        contact = request.json.get('contact')
        email = request.json.get('email')
        
        if not all([name, address, contact, email]):
            return jsonify({"status": "error", "message": "All fields are required"}), 400
        
        # Connect to Google Sheets
        sheet = connect_to_google_sheet()
        
        # Ensure the column headers exist
        ensure_column_headers(sheet)
        
        # Append the new row
        sheet.append_row([name, address, contact, email])
        
        return jsonify({"status": "success", "message": "Data added successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)