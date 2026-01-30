import pandas as pd
import json

# def convert_user_excel_to_json(excel_file, sheet_name, output_json):
#     # Read Excel sheet
#     df = pd.read_excel(excel_file, sheet_name=sheet_name)

#     # Rename columns to lowercase if needed
#     df.columns = [col.lower() for col in df.columns]

#     # Convert to JSON list of dicts
#     data = df.to_dict(orient="records")

#     # Save JSON to file
#     with open(output_json, "w") as f:
#         json.dump(data, f, indent=4)

#     print(f"✅ Saved to {output_json}")

def convert_user_excel_to_json(excel_file, sheet_name, output_json):
    # Read the Excel sheet
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Normalize column names
    df.columns = [col.lower().strip() for col in df.columns]

    # Sanitize username: strip, replace spaces with _, lowercase
    df['username'] = df['username'].astype(str).str.strip().str.replace(' ', '_').str.lower()

    # Sanitize email and password too (optional)
    df['email'] = df['email'].astype(str).str.strip().str.lower()
    df['password'] = df['password'].astype(str).str.strip()

    # Convert to list of dictionaries
    data = df.to_dict(orient="records")

    # Save to JSON
    with open(output_json, "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ JSON saved to {output_json}")

# Usage
convert_user_excel_to_json("cyber-drill.xlsx", "users", "cyber-drill.json")
