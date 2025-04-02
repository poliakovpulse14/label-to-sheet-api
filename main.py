from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Авторизація Google Sheets
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

SPREADSHEET_ID = "11AaS-IWTAN1-oFmRMNX4QvVVlMGEvksrHfMASN0hh5c"
SHEET_NAME = "Лист1"
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

@app.route("/add-row", methods=["POST"])
def add_row():
    data = request.json
    required = ["model", "sku", "us", "uk", "eu", "cm", "color"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400
    row = [data[k] for k in required]
    sheet.append_row(row)
    return jsonify({"message": "✅ Рядок додано!"})

@app.route("/")
def home():
    return "API працює! Надішліть POST-запит на /add-row"

if __name__ == "__main__":
    app.run()
