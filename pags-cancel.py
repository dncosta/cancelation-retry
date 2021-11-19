import requests
import json
import time

charges = ["aaaaa", "bbbbb", "cccc"]
amounts = [1, 2, 3]
token = 'Bearer token'

for charge, amount in zip(charges, amounts):

	url = "https://api.pagseguro.com/charges/" + str(charge)

	payload={}
	headers = {
	  'Authorization': token,
	  'Content-Type': 'application/json',
	  'x-api-version': '4.0'
	}

	response = requests.request("GET", url, headers=headers, data=payload)
	http_status = response.status_code
	response_json = json.loads(response.text)

	if(http_status == 200):
			charge_status = response_json['status']
			refunded_amount = response_json['amount']['summary']['refunded']
			missing = amount - refunded_amount
			
			if(missing > 0):
				url = "https://api.pagseguro.com/charges/" + str(charge) + "/cancel"
				payload = json.dumps({
					"amount": { 
					"value": missing
					}
				})
				headers = {
				  'Authorization': token,
				  'Content-Type': 'application/json',
				  'X-api-version': '4.0'
				}
				response = requests.request("POST", url, headers=headers, data=payload)
				http_status = response.status_code
				response_json = json.loads(response.text)

				if((http_status == 200) or (http_status == 201)):
					charge_status = response_json['status']
					refunded_amount = response_json['amount']['summary']['refunded']
					print("POST-cancel" + charge + ";" + charge_status + ";" + str(refunded_amount) + ";" + str(amount) + ";" + str(http_status) + ";" + "" + ";" + str(missing))
				else:
					error = response_json['error_messages']
					print("POST-cancel-error" + charge + ";" + "" + ";" + "" + ";" + "" + ";" + str(http_status) + ";" + str(error) +";" + "")
				time.sleep(1)
			else:
				print("GET-refund" +charge + ";" + charge_status + ";" + str(refunded_amount) + ";" + str(amount) + ";" + str(http_status) + ";" + str(missing))

	else:
		print("GET-refund-error" + "," + charge + ";" + "" + ";" + "" + ";" + "" + ";" + str(http_status))
	time.sleep(1)
