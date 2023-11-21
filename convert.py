import requests
import pandas as pd

# Replace with your Webex API key or authentication method
headers = {
    'Authorization': 'Bearer ZTg4ZjY1NjktYjYwNC00MzAwLTg4ZWYtYjVhODljYTNhMTJjMTAyMjZlZmMtMTQ4_PF84_3bf06e7b-f230-427f-9163-c54d2e428d6a',
}

# Get organization data
org_url = "https://webexapis.com/v1/organizations"
org_response = requests.get(org_url, headers=headers)
org_data = org_response.json()["items"]

# Create a DataFrame to store the final data
result_df = pd.DataFrame(columns=[
    'org_id', 'Name', 'id', 'LicenseName',
    'totalUnits', 'consumedUnits', 'subscriptionId'
])

# Loop through organizations
for org in org_data:
    org_id = org["id"]
    org_name = org["displayName"]

    # Get licenses data for the organization
    licenses_url = f"https://webexapis.com/v1/licenses?orgId={org_id}"
    licenses_response = requests.get(licenses_url, headers=headers)

    
    licenses_data = licenses_response.json().get("items", [])

    # Loop through licenses and append data to the DataFrame
    for license in licenses_data:
        row_data = {
            'org_id': org_id,
            'Name': org_name,
            'id': license["id"],
            'LicenseName': license["name"],
            'totalUnits': license["totalUnits"],
            'consumedUnits': license["consumedUnits"],
            'subscriptionId': license.get("subscriptionId", ""),
        }
        result_df = result_df._append(row_data, ignore_index=True)
        

# Display the DataFrame


# Write DataFrame to Excel file
result_df.to_excel("webex_data.xlsx", index=False)
