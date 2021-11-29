import requests
import json
import time

# sets requests variables for Metabase and PagSeguro

url_session = "https://metabase.moip.com.br/api/session"
url_refunds = "https://metabase.moip.com.br/api/card/10697/query"
url_pagseguro = "https://api.pagseguro.com/charges/"
username = # PLACE USERNAME
password = # PLACE USERNAME

# starts metabase session

print("Starting new session")

payload = json.dumps({
  "username": username ,
  "password": password
})
headers = {
  'Content-Type': 'application/json',
}

response_session = requests.request("POST", url_session, headers=headers, data=payload)
response_dict = json.loads(response_session.text)
session_id = response_dict['id']

print("New session started: " + session_id)

# retrieves the pending refunds from metabase and creates a list of charges

print("Getting pending refunds list")

payload = json.dumps({
  "ignore_cache": False,
  "parameters": []
})
headers = {
  'X-Metabase-Session': session_id,
  'Content-Type': 'application/json',
  'Cookie': 'metabase.SESSION='+session_id
}

response_refunds = requests.request("POST", url_refunds, headers=headers, data=payload)
refunds_dict = json.loads(response_refunds.text)
refund_row = refunds_dict['data']['rows']

charges = [item[0] for item in refund_row]
payments = [item[1] for item in refund_row]
amounts = [int(item[3]) for item in refund_row]
affiliations = [item[4] for item in refund_row]

print("Starting the refunds in PagSeguro")

# processes the refunds in PagSeguro

for charge, amount, affiliation in zip(charges, amounts, affiliations):

  payload={}
  headers = {
    'Authorization': "Bearer " + affiliation,
    'Content-Type': 'application/json',
    'x-api-version': '4.0'
  }

  response = requests.request("GET", url_pagseguro + str(charge), headers=headers, data=payload)
  http_status = response.status_code
  response_json = json.loads(response.text)

  if(http_status == 200):
      charge_status = response_json['status']
      refunded_amount = response_json['amount']['summary']['refunded']
      missing = amount - refunded_amount

      if(missing > 0):
        payload = json.dumps({
          "amount": { 
          "value": missing
          }
        })
        headers = {
          'Authorization': "Bearer " + affiliation,
          'Content-Type': 'application/json',
          'X-api-version': '4.0'
        }
        response = requests.request("POST", url_pagseguro + str(charge) + "/cancel", headers=headers, data=payload)
        http_status = response.status_code
        response_json = json.loads(response.text)

        if((http_status == 200) or (http_status == 201)):
          charge_status = response_json['status']
          refunded_amount = response_json['amount']['summary']['refunded']
          print("POST-cancel; ID:" + charge + ";STATUS: " + charge_status + "; REFUNDED_AMOUNT: " + str(refunded_amount) + "; TOTAL: " + str(amount) + "; HTTP_STATUS: " + str(http_status) + ";" + "" + ";MISSING: " + str(missing))
        else:
          error = response_json['error_messages']
          print("POST-cancel-error; ID: " + charge + ";" + "" + ";" + "" + ";" + "" + ";" + str(http_status) + ";" + str(error) +";" + "")
      else:
        print("GET-refund; ID: " +charge + ";STATUS: " + charge_status + "; REFUNDED_AMOUNT: " + str(refunded_amount) + "; TOTAL: " + str(amount) + "; HTTP_STATUS: " + str(http_status) + ";MISSING: " + str(missing))

  else:
    print("GET-refund-error; ID: " + ";" + charge + ";" + "" + ";" + "" + ";" + "" + ";" + str(http_status))
