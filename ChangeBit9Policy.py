# Install the Python Requests library:
# `pip install requests`

import requests
import json
import Tkinter as tk
import tkMessageBox
import unicodedata
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
try:
	import sys
except:
	pass

compNames = ''
policyName = ''
policyId = ''
apiKey = ""

def changePolicy():
	# Request
	# GET https://cb.mydomain.local/api/bit9platform/v1/computer
	setPrevious = 0
	policyName = policyType.get()
	if policyName == "Back to Previous":
		setPrevious = 1
	elif policyName == "Local Approval":
		policyId = "4"

	compNames = scanIP.get("1.0","end-1c")
	compNames = unicodedata.normalize('NFKD', compNames).encode('ascii','ignore')
	compNames = compNames.split("; ")
	compNames = " ".join(compNames)
	newNameList = compNames.replace('\r', ',').replace('\n', ',')
	compNames = newNameList.split(",")

	for server in compNames:
		server = server.upper()
		server = "*%s*" % server
		sep = "."
		server = server.split(sep, 1)[0]
		response = requests.get(
			url="https://cb.mydomain.local/api/bit9platform/v1/computer?q=name:%s&q=deleted:False" % server,
			headers={
				"X-Auth-Token": apiKey,
				"Content-Type": "application/json",
			},
			verify=False,
		)

		device = json.loads(response.content)
		try:
			deviceId = device[0]['id']
			name = device[0]['name']
			prevPolicy = device[0]['policyName']
			prevPolicyId = device[0]['previousPolicyId']
			localApproval = device[0]['localApproval']
			#print(prevPolicyId)
		except IndexError:
			print("%s name does not exist") % server



		# This section is a temporary fix for changing from Local Approval
		if setPrevious == 1:
			if prevPolicyId == 21 or prevPolicyId == 22:

				if localApproval == True:
					response = requests.put(
						url="https://cb.mydomain.local/api/bit9platform/v1/computer/%s" % deviceId,
						headers={
							"X-Auth-Token": apiKey,
							"Content-Type": "application/json",
						},
						data=json.dumps({
							"policyId": "23"
						}),
						verify=False,
					)

			elif prevPolicyId == 13 or prevPolicyId == 18:

				if localApproval == True:
					response = requests.put(
						url="https://cb.mydomain.local/api/bit9platform/v1/computer/%s" % deviceId,
						headers={
							"X-Auth-Token": apiKey,
							"Content-Type": "application/json",
						},
						data=json.dumps({
							"policyId": "5"
						}),
						verify=False,
					)

			response = requests.put(
				url="https://cb.mydomain.local/api/bit9platform/v1/computer/%s" % deviceId,
				headers={
					"X-Auth-Token": apiKey,
					"Content-Type": "application/json",
				},
				data=json.dumps({
					"policyId": "%s" % prevPolicyId
				}),
				verify=False,
			)
		# End Section
		else:
			response = requests.put(
				url="https://cb.mydomain.local/api/bit9platform/v1/computer/%s" % deviceId,
				headers={
					"X-Auth-Token": apiKey,
					"Content-Type": "application/json",
				},
				data=json.dumps({
					"policyId": "%s" % policyId
				}),
				verify=False,
			)

		print(name + " set from " + prevPolicy + " to " + policyName)

	tkMessageBox.showinfo("Success","Devices have been moved.")

def exitOption():
	try:
		app.destroy()
	except:
		exit()

app = tk.Tk()

app.title("Carbon Black Policy Change App")
app.geometry('615x500+200+200')
app.resizable(width=False, height=False)
app.grid_columnconfigure(1, weight=1)
labelText = tk.StringVar()
labelText.set("Change CB Policy")
label1 = tk.Label(app, textvariable=labelText, height=3)
label1.config(font=('bold',14))
label1.grid(row=0, columnspan=4)

# File Menu
menu = tk.Menu(app)
app.config(menu=menu)
fileMenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Exit", command=exitOption)

OPTIONS = [
	"Back to Previous",
	"Local Approval",
]

# Policy Type menu
policyType = tk.StringVar(app)
policyType.set(OPTIONS[1])
policyMenu = tk.OptionMenu(app, policyType, *OPTIONS)
policyMenu.grid(row=7, columnspan=4)

# Get list of IPs
ipLabel = tk.StringVar()
ipLabel.set("Enter the server names, separated by comma or line break:")
label2 = tk.Label(app, textvariable=ipLabel, height=4)
label2.grid(row=11, columnspan=3)
scanIP = tk.Text(app, width=48, height=16)
scanIP.grid(row=13, padx=15, columnspan=3)

# Create Submit Button
submit = tk.Button(app, text="Change Policy", width=20, command=changePolicy)
submit.grid(row=14, padx=15, pady=15, columnspan=4)
entry = tk.Entry(app)

app.mainloop()

