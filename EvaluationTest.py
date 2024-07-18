import os
from dotenv import load_dotenv,dotenv_values 
from hubspot import HubSpot
import requests
from hubspot.crm.contacts import SimplePublicObjectInputForCreate
from hubspot.crm.contacts.exceptions import ApiException


load_dotenv() 

def getContacts():
    try:
        response = requests.get(
        os.getenv("AWS_URl"),
        headers={"Authorization": f"Bearer {os.getenv("AWS_TOKEN")}"}
        )
       
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}') 
    except Exception as err:
        print(f'An error occurred: {err}')
    return None
    


api_client = HubSpot(access_token= os.getenv("MY_TOKEN"))

def remove_duplicates_and_none(contacts):
    seen_emails = set()
    filtered_contacts = []
    for contact in contacts:
        email = contact.get('email')
        if email and email not in seen_emails:
            seen_emails.add(email)
            filtered_contacts.append(contact)
    return filtered_contacts


def create_hubspot_contact(contacts):
    success_count = 0
    exception_count = 0

    for contact in contacts:
        try:
            simple_public_object_input_for_create = SimplePublicObjectInputForCreate(
                properties={
                    "hs_object_id": contact["id"],
                    "firstname": contact["first_name"],
                    "lastname": contact["last_name"],
                    "email": contact["email"],
                    "gender": contact["gender"],
                    "phone": contact["phone_number"]}
            )
            api_response = api_client.crm.contacts.basic_api.create(
                simple_public_object_input_for_create=simple_public_object_input_for_create
            )
            success_count += 1
        except ApiException as e:
            print("Exception when creating contact: %s\n" % e)
            exception_count += 1
            print(contact) 

    return f"Operation Summary: {success_count} contacts created, {exception_count} exceptions encountered."

def main():
    
    aws_contacts = getContacts()

    if aws_contacts is None:
        print("Failed to retrieve AWS contacts. Exiting.")
        return
    
    clean_contacts = remove_duplicates_and_none(aws_contacts)
    print(create_hubspot_contact(clean_contacts))



if __name__ == "__main__":
    main()