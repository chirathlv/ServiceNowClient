class ServiceNowClient:
    def __init__(self, work_notes_text=None, description=None, ritm_sys_id=None, file_paths=None, update_data=None):
        # Define the Header
        self.headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        
        # RITM Sys ID
        self.ritm_sys_id = ritm_sys_id

        # Record Update data
        self.update_data = update_data

        # Insert Work Notes
        self.work_notes_text = work_notes_text

        # Description
        self.description = description

        # File Paths to be attached
        self.file_paths = file_paths

    def initialize(self):
        try:
            parser = argparse.ArgumentParser(description='Service Now Client')
            
            # Get config
            parser.add_argument('-i', '--instance', help='Specify the Instance URL', required=True)
            parser.add_argument('-u', '--username', help='Specify Service Now Instance login username', required=True)
            parser.add_argument('-p', '--password', help='Specify Service Now Instance login password', required=True)
            parser.add_argument('-rt', '--record_type', help='Specify Service Now Record Type like RITM, Incident or Change', required=True)
            parser.add_argument('-req', '--request_sys_id', help='Specify Service Now Request Sys ID')
            parser.add_argument('-ritm', '--ritm_sys_id', help='Specify Service Now RITM Sys ID')
            parser.add_argument('-inc', '--incident_sys_id', help='Specify Service Now INCIDENT Sys ID')
            parser.add_argument('-chng', '--change_sys_id', help='Specify Service Now CHANGE Sys ID')
            parser.add_argument('-ob', '--opened_by', help='Specify Open by Sys ID', required=True)
            parser.add_argument('-cb', '--created_by', help='Specify Created by Sys ID', required=True)
            parser.add_argument('-rf', '--requested_for', help='Specify Requested for Sys ID', required=True)
            parser.add_argument('-sg', '--stage', help='Specify the stage', required=True)
            parser.add_argument('-st', '--state', help='Specify the state', required=True)
            parser.add_argument('-sla', '--sla_definition_sys_id', help='Specify the SLA Definition sys ID', required=True)
            parser.add_argument('-cat', '--catalog_item_sys_id', help='Specify the Catalog Item sys ID', required=True)
            parser.add_argument('-sd', '--short_description', help='Specify the Short Description', required=True)
            parser.add_argument('-d', '--description', help='Specify the Description', required=True)
            parser.add_argument('-ag', '--assignment_group', help='Specify the Assignment Group sys ID', required=True)
            parser.add_argument('-at', '--assigned_to', help='Specify the Assigned To sys ID', required=True)
            parser.add_argument('-app', '--approval_required', help='Specify the If the Approval is required or not!', required=True) # False if Approval not required (change to True if required)
            parser.add_argument('-bs', '--business_service', help='Specify the Business Service sys ID', required=True)
            parser.add_argument('-ct', '--category_sys_id', help='Specify the Category sys ID', required=True)
            parser.add_argument('-fp', '--file_paths', nargs='+', help='Specify the List of all Absolute File Paths you want to attach', required=True)
            parser.add_argument('-wn', '--work_notes_text', help='Specify the Work Notes to be added', required=True)

            args = parser.parse_args()
            
            # Set Config of Service Request / RITM Parameters
            self.instance = args.instance.strip().lower() if hasattr(args, 'instance') else None
            self.instance_url = f'https://{self.instance}.service-now.com'
            self.username = args.username if hasattr(args, 'username') else None
            self.password = args.password if hasattr(args, 'password') else None
            self.record_type = args.record_type if hasattr(args, 'record_type') else None
            self.request_sys_id = args.request_sys_id if hasattr(args, 'request_sys_id') else None
            self.ritm_sys_id = args.ritm_sys_id if hasattr(args, 'ritm_sys_id') else None
            self.incident_sys_id = args.incident_sys_id if hasattr(args, 'incident_sys_id') else None
            self.change_sys_id = args.change_sys_id if hasattr(args, 'change_sys_id') else None
            self.opened_by = args.opened_by if hasattr(args, 'opened_by') else None
            self.created_by = args.created_by if hasattr(args, 'created_by') else None
            self.requested_for = args.requested_for if hasattr(args, 'requested_for') else None
            self.stage = args.stage if hasattr(args, 'stage') else None
            self.state = args.state if hasattr(args, 'state') else None
            self.sla_definition_sys_id = args.sla_definition_sys_id if hasattr(args, 'sla_definition_sys_id') else None
            self.catalog_item_sys_id = args.catalog_item_sys_id if hasattr(args, 'catalog_item_sys_id') else None
            self.short_description = args.short_description if hasattr(args, 'short_description') else None
            self.description = args.description if hasattr(args, 'description') else None
            self.assignment_group = args.assignment_group if hasattr(args, 'assignment_group') else None
            self.assigned_to = args.assigned_to if hasattr(args, 'assigned_to') else None
            self.approval_required = True if hasattr(args, 'approval_required') and args.approval_required.upper() == 'TRUE' else False if hasattr(args, 'approval_required') and args.approval_required.upper() == 'FALSE' else None
            self.business_service = args.business_service if hasattr(args, 'business_service') else None
            self.category_sys_id = args.category_sys_id if hasattr(args, 'category_sys_id') else None
            self.file_paths = args.file_paths if hasattr(args, 'file_paths') else None
            self.work_notes_text = args.work_notes_text if hasattr(args, 'work_notes_text') else None

            self.update_data = {
                'description' : self.description
            }

        except exception as error:
            print(f'Error in initialize: {error}')

    def create_change_request(self):

        # Check if the Record Type is RITM
        if self.record_type.upper() != "CHANGE":
            print("Error! Specified Record Type is NOT CHANGE! This method is for Change record update only!")
            return False

        change_request_data = {
            "short_description": self.short_description,
            "description": self.description,
            "assignment_group": self.assignment_group,
            "category": self.category_sys_id,
            "state": self.state
        }

        change_request_endpoint = f'{self.instance_url}/api/now/table/change_request'

        try:
            response = requests.post(
                change_request_endpoint,
                headers=self.headers,
                auth=(self.username, self.password),
                data=json.dumps(change_request_data)
            )

            if response.status_code == 201:
                print("Change Request created successfully.")
                return json.loads(response.text)['result']['sys_id']
            else:
                print(f"Failed to create Change Request. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def create_request(self):

        # Check if the Record Type is RITM
        if self.record_type.upper() != "RITM":
            print("Error! Specified Record Type is NOT RITM! This method is for RITM record update only!")
            return False

        request_data = {
            "opened_by": self.opened_by,
            "created_by": self.created_by,
            "requested_for": self.requested_for,
            "stage": self.stage,
            "state": self.state,
            "sla": self.sla_definition_sys_id,  # Associate the SLA Sys ID with the RITM
            "cat_item": self.catalog_item_sys_id
        }

        request_endpoint = f'{self.instance_url}/api/now/table/sc_request'

        try:
            response = requests.post(
                request_endpoint,
                headers=self.headers,
                auth=(self.username, self.password),
                data=json.dumps(request_data)
            )

            if response.status_code == 201:
                print("Request created successfully.")
                self.request_sys_id = json.loads(response.text)['result']['sys_id']
                return self.request_sys_id
            else:
                print(f"Failed to create Request. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def create_requested_item(self):

        # Check if the Record Type is RITM
        if self.record_type.upper() != "RITM":
            print("Error! Specified Record Type is NOT RITM! This method is for RITM record update only!")
            return False

        # Calculate due_date
        due_date = datetime.now() + timedelta(hours=14)

        # Check if the Request is already created before RITM is created
        if self.request_sys_id is None:
            print('Error! Request must be created first!')
            return False

        ritm_data = {
            "request": self.request_sys_id,  # Link RITM to the Request,
            "short_description": self.short_description,
            "description": self.description,
            "assignment_group": self.assignment_group,
            "assigned_to": self.assigned_to,
            "approval": "requested" if self.approval_required else "not required",  # Assuming boolean value for approval_required
            "stage": self.stage,
            "state": self.state,
            "business_service": self.business_service,
            "opened_by": self.opened_by,
            "requested_for": self.requested_for,
            "cat_item": self.catalog_item_sys_id,
            "u_category": self.category_sys_id,
            "due_date" : due_date.strftime('%Y-%m-%d %H:%M:%S')  # Format Due Date as a string
        }
        
        ritm_endpoint = f'{self.instance_url}/api/now/table/sc_req_item'

        try:
            response = requests.post(
                ritm_endpoint,
                headers=self.headers,
                auth=(self.username, self.password),
                data=json.dumps(ritm_data)
            )

            if response.status_code == 201:
                print("Requested Item (RITM) created successfully.")
                self.ritm_sys_id = json.loads(response.text)['result']['sys_id']
                return self.ritm_sys_id
            else:
                print(f"Failed to create Requested Item (RITM). Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def update_record(self):
        # Check if the RITM Sys ID has been provided
        if self.ritm_sys_id is None:
            print("Error! RITM MUST set in order to update!")
            return False
        
        # Update data cannot be empty
        if self.update_data is None:
            print("Error! RITM which Field with what value MUST be provided in a Dictionary to update!")
            return False

        # Checking the Record type and setting parameters
        if self.record_type.upper() == "RITM":
            record_sys_id = self.ritm_sys_id
            table_name = "sc_req_item"
        elif self.record_type.upper() == "INCIDENT":
            record_sys_id = self.incident_sys_id
        else:
            record_sys_id = self.change_sys_id

        # Construct the API URL for updating the RITM
        ritm_endpoint = f'{self.instance_url}/api/now/table/{table_name}/{record_sys_id}'

        try:
            # Send a PATCH request to update the RITM
            response = requests.patch(
                ritm_endpoint,
                headers=self.headers,
                auth=(self.username, self.password),
                data=json.dumps(self.update_data)
            )

            if response.status_code == 200:
                print(f"RITM {record_sys_id} updated successfully.")
                return True
            else:
                print(f"Failed to update RITM {record_sys_id}. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                return None

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def add_work_notes(self):
        # Checking the Record type and setting parameters
        if self.record_type.upper() == "RITM":
            record_sys_id = self.ritm_sys_id
            table_name = "sc_req_item"
        elif self.record_type.upper() == "INCIDENT":
            record_sys_id = self.incident_sys_id
        else:
            record_sys_id = self.change_sys_id

        # Check if the Work Notes has been provided
        if self.work_notes_text is not None:
            work_notes_field = 'work_notes'
        else:
            return False

        # Construct the API URL to update the RITM
        ritm_endpoint = f'{self.instance_url}/api/now/table/{table_name}/{record_sys_id}'

        # Data to add Work Notes
        work_notes_data = {
            work_notes_field: self.work_notes_text
        }

        try:
            response = requests.patch(
                ritm_endpoint,
                headers=self.headers,
                auth=(self.username, self.password),
                data=json.dumps(work_notes_data)
            )

            if response.status_code in (200, 201):
                print("Activity comment added to RITM successfully.")
                return True
            else:
                print(f"Failed to add activity comment. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def close_record(self):
        # Checking the Record type and setting parameters
        if self.record_type.upper() == "RITM":
            record_sys_id = self.ritm_sys_id
            table_name = "sc_req_item"
        elif self.record_type.upper() == "INCIDENT":
            record_sys_id = self.incident_sys_id
        else:
            record_sys_id = self.change_sys_id

        # Define the state you want to set for closing the RITM (e.g., 'Closed' or 'Completed')
        new_state = 'Closed Complete'  # Change to 'Completed' or other state if needed

        # Construct the API URL to update the RITM
        ritm_endpoint = f'{self.instance_url}/api/now/table/{table_name}/{record_sys_id}'

        # Data to update the RITM state
        update_data = {
            'state': new_state
        }

        try:
            response = requests.patch(
                ritm_endpoint,
                headers=self.headers,
                auth=(self.username, self.password),
                data=json.dumps(update_data)
            )

            if response.status_code in (200, 201):
                print(f"RITM {record_sys_id} has been closed.")
                return True
            else:
                print(f"Failed to close RITM. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def create_incident(self):

        # Check if the Record Type is RITM
        if self.record_type.upper() != "INCIDENT":
            print("Error! Specified Record Type is NOT INCIDENT! This method is for INCIDENT record update only!")
            return False

        incident_data = {
            "short_description": self.short_description,
            "description": self.description,
            "assignment_group": self.assignment_group,
            "category": self.category,
            "state": self.state
        }

        incident_endpoint = f'{self.instance_url}/api/now/table/incident'

        try:
            response = requests.post(
                incident_endpoint,
                headers=self.headers,
                auth=(self.username, self.password),
                data=json.dumps(incident_data)
            )

            if response.status_code == 201:
                print("Incident created successfully.")
                return json.loads(response.text)['result']['sys_id']
            else:
                print(f"Failed to create Incident. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def attach_files(self):
        """ RITM, Incident and Change all will use this module to attach files """

        # Check if the Record Type is RITM
        if self.record_type.upper() != "RITM":
            print("Error! Specified Record Type is NOT RITM! This method is for RITM record update only!")
            return False

        if self.record_type.upper() == "RITM":
            record_sys_id = self.ritm_sys_id
            table_name = "sc_req_item"

        elif self.record_type.upper() == "INCIDENT":
            record_sys_id = self.incident_sys_id

        else:
            record_sys_id = self.change_sys_id

        try:
            for file_path in self.file_paths:
                # Get the file name from the file path
                file_name = os.path.basename(file_path)

                # Load the file data
                file_data = open(file_path, 'rb').read()

                # Construct the API URL to attach a file to the RITM
                attachment_endpoint = f'{self.instance_url}/api/now/attachment/file?table_name={table_name}&table_sys_id={record_sys_id}&file_name={file_name}'

                attachment_data = {
                    'table_name': table_name,
                    'table_sys_id': record_sys_id,
                    'file_name': file_name
                }
                
                response = requests.post(
                    attachment_endpoint,
                    headers=self.headers,
                    auth=(self.username, self.password),
                    data=file_data
                )

                if response.status_code == 201:
                    print(f"File '{file_name}' attachment successful.")
                else:
                    print(f"Failed to attach file '{file_name}'. Status Code: {response.status_code}")
                    print(f"Response: {response.text}")
                    
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def get_catalog_item(self):
        # Check if the Record Type is RITM
        if self.record_type.upper() != "RITM":
            print("Error! Specified Record Type is NOT RITM! This method is for RITM record update only!")
            return False

        if self.record_type.upper() == "RITM":
            record_sys_id = self.ritm_sys_id
            table_name = "sc_req_item"

        elif self.record_type.upper() == "INCIDENT":
            record_sys_id = self.incident_sys_id

        else:
            record_sys_id = self.change_sys_id

        # Construct the API URL to query the specific RITM based on its Sys ID
        ritm_endpoint = f'{self.instance_url}/api/now/table/{table_name}/{record_sys_id}'

        try:
            response = requests.get(
                ritm_endpoint,
                headers=self.headers,
                auth=(self.username, self.password)
            )

            if response.status_code == 200:
                ritm_data = response.json().get('result', {})
                if ritm_data:
                    # Retrieve the catalog item Sys ID from the RITM data
                    catalog_item_sys_id = ritm_data.get('cat_item')
                    if catalog_item_sys_id:
                        print(ritm_data)
                        return catalog_item_sys_id
                    else:
                        print(f"Catalog item not found for RITM Sys ID: {ritm_sys_id}")
                        return None
                else:
                    print(f"RITM with Sys ID {ritm_sys_id} not found.")
                    return None
            else:
                print(f"Failed to retrieve RITM. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

def main():
    # Intantiate a Client Object
    client = ServiceNowClient()

    # initialize the parameters
    client.initialize()

    # Create a Work Request
    client.create_request()

    # Create a RITM
    client.create_requested_item()

    # update the RITM
    client.update_record()

    # Add Work Notes
    client.add_work_notes()

    # Attach Files
    client.attach_files()

    # Close Record
    client.close_record()

import os
import json
import requests
import argparse
from datetime import datetime, timedelta

if __name__ == '__main__':
    try:
        ''' To Generate Service Now Records '''
        main()

    except exception as error:
        print(f'Error: {error}')
        exit(1)