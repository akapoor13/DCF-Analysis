from flask import request
import requests
import json
import datetime


auth_data = {
	"grant_type"    : "client_credentials",
    "client_id"     : "27590ede7e3d454c82374eaa8b5a7531",
    "client_secret" : "e341794fbc0a39a030263ebeb270fe8253f2380f52cd306e856f4dda70ba40f5",
    "scope"         : "read_product_data"
}

class Data(object):

	def __init__(self, ticker):
		self.TCK = ticker
		self.growth = []
		self.financialReturns = []
		self.integrated = []
		self.multiples = []

	def addGrowth(self, point):
		self.growth.append(point)

	def addFinancialReturns(self, point):
		self.financialReturns.append(point)

	def addIntegerated(self, point):
		self.integrated.append(point)

	def addMultiples(self, point):
		self.multiples.append(point)

def getMarqueeData(ticker):	
	# Create a session instance

	session = requests.Session()

	auth_request = session.post("https://idfs.gs.com/as/token.oauth2", data = auth_data)
	access_token_dict = json.loads(auth_request.text)
	access_token = access_token_dict["access_token"]

	#Update session headers with the access token
	session.headers.update({"Authorization":"Bearer "+ access_token})

	#URL for the request
	request_url = "https://api.marquee.gs.com/v1/data/USCANFPP_MINI/query"

	request_query = {}
	#What we want to query

	today = datetime.date.today()
	startDate = "2009-01-01"
	endDate = today.strftime("%Y-%m-%d")
	request_query = {
			"where": {
				"gsid": [str(ticker)]
			},
			"startDate": startDate,
		    "endDate": endDate
		}


	#Get the POST request text
	request = session.post(url=request_url, json=request_query)
	results = json.loads(request.text)

	returnData = Data(ticker)
	print(type(results['data'][0]))
	for dataPoint in results['data']:
		try:
			returnData.addGrowth([dataPoint['growthScore']])
			returnData.addFinancialReturns([dataPoint['financialReturnsScore']])
			returnData.addIntegerated([dataPoint['integratedScore']])
			returnData.addMultiples([dataPoint['multipleScore']])
		except:
			continue
	return returnData


