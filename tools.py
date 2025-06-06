import requests
import json
import smtplib
from email.mime.text import MIMEText
with open('./credentials.json', 'r') as creds:
    credentials = json.load(creds)
system_host = "https://s4hana2022.mindsetconsulting.com:44300/sap/opu/odata/sap/API_SALES_ORDER_SRV/"


SAP_USERNAME = credentials["SAP_HANA"]["USERNAME"]
SAP_PASSWORD = credentials["SAP_HANA"]["PASSWORD"]

session = requests.Session()
session.auth = requests.auth.HTTPBasicAuth(SAP_USERNAME,SAP_PASSWORD)





def get_salesorder_details(invoice_id: str) -> str:
   """Returns an invoice's details by calling an external odata service.

   Args:
      invoice_id: The invoide id
   """
   print(f"Getting Details for {invoice_id}")
   url = f"{system_host}/A_SalesOrder('{invoice_id}')?$format=json&$select=SalesOrder,SalesOrderType,SalesOrderType,SalesOrganization,DistributionChannel,OrganizationDivision,SoldToParty,OverallDeliveryStatus"
   odataresponse = session.get(url)
   # mailbody = json_to_html_table_for_email(odataresponse.content)
   response = f"The details for invoice {invoice_id} in json is: {odataresponse.content}." 
   # print(mailbody)
   return response

def get_email_address(name: str) -> str:
   """Returns the person's email address

   Args:
      name: The name of the person whose email address is returned
   """
   print(f"Getting Email id of {name}")

   dict = {}
   dict['Ewald'] = 'akhilplw@gmail.com'
   dict['Stefan'] = 'akhilplw@gmail.com'
   dict['Fabian'] = 'akhilplw@gmail.com'
   dict['Vighnesh'] = 'vighneshkamath@mindsetconsulting.com'

   if name in dict.keys():
      response = dict[name]
   else:
      response = dict['Andreas']
   print(f"Email id of {name} is {response}")
   return response



def sendmail(ToAddress:str, MailContent: str, invoice_id: str):
   """Sends the mail to the email id mentioned in the argument

   Args:
      ToAddress: The email id to which mail needs to be sent.
      MailContent: The Mail body which is received from get_invoice_details function which will be sent in the mail.
      invoice_id: Invoice ID value whose status is being sent.
   """
   print(f"Preparing to send mail to {ToAddress} for Invoice ID: {invoice_id}")

   subject = f"Status of Invoice {invoice_id}"
   FromAddress = "akhil.das@mindsetconsulting.com" # Your sender email

   # Create the MIMEText object. If MailContent is HTML, use MIMEText(MailContent, 'html')
   msg = MIMEText(MailContent, 'html') # Assuming plain text for this example
   msg['Subject'] = subject
   msg['From'] = FromAddress
   msg['To'] = ToAddress # Corrected for single string recipient
   
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('akhil.das@mindsetconsulting.com', 'ebty thjn btdd hwuk')
   server.sendmail(FromAddress, ToAddress, msg.as_string())
   print("Mail sent successfully")

def json_to_html_table_for_email(json_string_data):
    """
    Converts a JSON string (specifically the OData V2 single entity format)
    into an HTML table string suitable for email.

    Args:
        json_string_data (str): The JSON string containing the sales order data.

    Returns:
        str: An HTML string representing the data in a table.
             Returns an error message string if parsing fails or data is not as expected.
    """
    try:
        data = json.loads(json_string_data)
    except json.JSONDecodeError as e:
        return f"<p>Error decoding JSON: {e}</p>"

    # OData V2 typically wraps the main content in a 'd' key
    if 'd' not in data or not isinstance(data['d'], dict):
        return "<p>Error: JSON does not contain the expected 'd' key with a dictionary value.</p>"

    sales_order_data = data['d']

    # Start building the HTML table
    # Using inline styles for better email client compatibility
    html_table = """
    <html>
    <head>
      <style>
        table {
          font-family: Arial, sans-serif;
          border-collapse: collapse;
          width: 80%;
          margin: 20px auto; /* Center table and add some margin */
        }
        th, td {
          border: 1px solid #dddddd;
          text-align: left;
          padding: 10px; /* Increased padding */
        }
        th {
          background-color: #f2f2f2; /* Light grey background for headers */
          color: #333;
        }
        tr:nth-child(even) {
          background-color: #f9f9f9; /* Zebra striping for rows */
        }
        caption {
          font-size: 1.2em;
          margin-bottom: 10px;
          font-weight: bold;
        }
      </style>
    </head>
    <body>
      <table>
        <caption>Sales Order Details</caption>
        <tr>
          <th>Field</th>
          <th>Value</th>
        </tr>
    """

    # Iterate through the sales order data, skipping '__metadata'
    for key, value in sales_order_data.items():
        if key == "__metadata":
            continue  # Skip the metadata section

        # Ensure values are properly escaped if they might contain HTML special characters
        # For simple string/number values from this JSON, direct insertion is often fine.
        # For more complex scenarios, consider using html.escape()
        html_table += f"  <tr>\n    <td>{key}</td>\n    <td>{value}</td>\n  </tr>\n"

    html_table += """
      </table>
    </body>
    </html>
    """
    return html_table


# sendmail("akhilplw@gmail.com","The status for invoice 1112 is: Overall Delivery Status - C. The details have been sent to Fabian's email.", "1112")