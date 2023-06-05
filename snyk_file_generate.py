import json
import requests

# API endpoint
api_url = "https://api.snyk.io/v1/org/[org_id]/project/[project_id]/ignores"

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "token [token]"
}

# Make the API request with headers
response = requests.get(api_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Extract the initial text from the API response
    initial_text = response.json()

    # Generate the .snyk file content
    snyk_text = "ignore:\n"
    for key, value in initial_text.items():
        snyk_text += f"  {key}:\n"
        for item in value:
            for subkey, subvalue in item.items():
                reason = subvalue['reason']
                if not reason:
                    reason = "no reason given"
                snyk_text += f"    - {subkey}:\n"
                snyk_text += f"        reason: {reason}\n"
                snyk_text += f"        expires: {subvalue['expires']}\n"

    # Write the .snyk file
    with open(".snyk", "w") as file:
        file.write(snyk_text)

    print(".snyk file generated successfully!")
else:
    print(f"API request failed with status code: {response.status_code}")
