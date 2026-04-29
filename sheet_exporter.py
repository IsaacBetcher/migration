import requests
import os

# converting the linked Google sheets into a csv file, which the parser will then turn into a format
# that new format will be turned into Monday Check entries

def export_google_sheet_as_csv(sheet_url):

    # Convert normal URL → CSV export URL
    if "/edit" in sheet_url:
        csv_url = sheet_url.split("/edit")[0] + "/export?format=csv"
    else:
        csv_url = sheet_url + "/export?format=csv"

    response = requests.get(csv_url)

    if response.status_code != 200:
        raise Exception(f"Failed to download sheet CSV: {response.status_code}")

    return response.text

# creating and saving a temporary csv files

def save_csv_temp(csv_text, filename="temp_import.csv"):
    path = os.path.join("csv_files", filename)

    os.makedirs("csv_files", exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(csv_text)

    return path