from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import os

class sendinblue:
    def __init__(self):
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = os.getenv('SENDINBLUE')
        
    def create_contact(self):
        api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        create_contact = sib_api_v3_sdk.CreateContact(email="adak07151@gmail.com", list_ids=[2])

        try:
            api_response = api_instance.create_contact(create_contact)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ContactsApi->create_contact: %s\n" % e)
    
    def run_service(self,email,data):
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        subject = "My Subject"
        html_content = f"<html><body><h1>{data}</h1></body></html>"
        sender = {"name":"MALACROCHET","email":"adakchandramala@gmail.com"}
        to = [{"email":email,"name":"User"}]
        headers = {"Some-Custom-Name":"unique-id-1234"}
        params = {"parameter":"My param value","subject":"New Subject"}
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)        
        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)