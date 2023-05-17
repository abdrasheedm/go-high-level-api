import random
import requests
from django.http import JsonResponse
# Create your views here.

def fetch_contacts(request):
    api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6IkpOVEpTV04ya0tkRVZkMElFbEZhIiwiY29tcGFueV9pZCI6ImJmb1Q3MkNWcm9oMlg4ZWZPUmdRIiwidmVyc2lvbiI6MSwiaWF0IjoxNjYxNDE2NzQzNTcxLCJzdWIiOiJQcVJEWDZqMjdXempXRUNsQm92eCJ9.u6WPtyudfB9R4nLnLbBZ6i9KquDeK6WnIOZxKAeE9Hg'
    contacts_url = 'https://rest.gohighlevel.com/v1/contacts/'
    custom_fields_url = 'https://rest.gohighlevel.com/v1/custom-fields/'
    field_name = 'DFS Booking Zoom Link'
    new_value = 'TEST'

    headers = {
        "Authorization" : f"Bearer {api_key}",
        "Content-Type" : "application/json"
    }
    
    # Fetching contacts
    response = requests.get(contacts_url, headers=headers)

    if response.status_code == 200:
        contacts = response.json().get("contacts")

        # Select Random Contact
        random_contact = random.choice(contacts)

        #Fetching custom fields
        custom_fields_response = requests.get(custom_fields_url, headers=headers)

        if custom_fields_response.status_code == 200:
            custom_fields = custom_fields_response.json().get("customFields")

            # Find the custom field ID for the given field name
            field_id = None
            for custom_field in custom_fields:
                if custom_field["name"] == field_name:
                    field_id = custom_field["id"]
                    break

            if field_id:
                # Update the custom field for the random contact
                contact_id = random_contact["id"]
                update_url = f"{contacts_url}/{contact_id}"
                payload = {
                    "customField" : {
                        field_id : new_value
                    }
                }

                update_response = requests.put(update_url, json=payload, headers=headers)

                if update_response.status_code == 200:
                    return JsonResponse({"message": "Custom field updated successfully"})
                else:
                    return JsonResponse({"error": "Failed to update custom field"})
            
            else:
                return JsonResponse({"error": "Custom field not found"})
        else:
            return JsonResponse({"error" : "Failed to fetch custom fields"})
    
    else:
        return JsonResponse({"error": "Failed to fetch contacts"})

