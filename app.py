from flask import Flask, escape, url_for, render_template, request
import flask
import json
import random
from time import localtime, strftime
from marquee import getMarqueeData
from dcfAnalysis import getDCF

app = Flask(__name__)

tickersToGSID = {'CCL': '75154', 'LL': '193067', 'ULTA': '194688', 'CHKP': '902608', 'SAH': '85627', 'WYNN': '150407', 'CRM': '161467', 'RL': '85072', 'GIB': '86372', 'MXIM': '11896', 'WDAY': '230958', 'MA': '177256', 'TGT': '49154', 'AZO': '76605', 'PAY': '173578', 'BBY': '85914', 'LULU': '193324', 'TIF': '75100', 'NFLX': '149756', 'BYD': '79758', 'STZ': '69796', 'VECO': '81116', 'AVGO': '202271', 'RCL': '79145', 'UNFI': '84275', 'SFLY': '183269', 'CBS': '76226', 'PG': '18163', 'ADTN': '80791', 'STX': '152963', 'V': '197235', 'GRPN': '222946', 'ADSK': '85631', 'CMCSA': '25022', 'PAYX': '61621', 'GPS': '59010', 'FLEX': '902704', 'FLT': '216587', 'JNPR': '901237', 'TSCO': '80286', 'BBBY': '77659', 'TXN': '15579', 'MU': '53613', 'HSY': '16600', 'ODP': '75573', 'GM': '216722', 'CLX': '46578', 'IPG': '53065', 'APH': '84769', 'PVH': '13936', 'RAD': '46922', 'ADS': '905632', 'VMW': '193155', 'ROST': '91556', 'COST': '64064', 'FLIR': '79265', 'DKS': '151048', 'EXPE': '176665', 'KLAC': '46886', 'FSLR': '183414', 'CCEP': '70500', 'GT': '16432', 'ULTI': '86196', 'KO': '11308', 'WMT': '55976', 'INFN': '188804', 'K': '26825', 'WEX': '172890', 'GPN': '905288', 'ARW': '29209', 'CNK': '188329', 'ADM': '10516', 'SYMC': '75607', 'CL': '18729', 'KR': '16678', 'ADP': '44644', 'ZNGA': '223416', 'NTAP': '82598', 'DIS': '26403', 'TAP': '59248', 'INTU': '78975', 'AKAM': '903917', 'MGA': '78045', 'IBM': '12490', 'TJX': '40539', 'RGC': '148401', 'KMB': '17750', 'FISV': '10696', 'GLW': '22293', 'WDC': '66384', 'CHH': '85517', 'CSOD': '217708', 'EBAY': '86356', 'GRMN': '905255', 'AAPL': '14593'}

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


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		print("enter")
		result = request.form
	print(result)
	print(request.form)
	print(request.method)
	print(result['TICKER'])
	results = getDCF(result['TICKER'])

	MarqueeData = getMarqueeData(tickersToGSID[result['TICKER']])
	date = strftime("%Y-%m-%d %H:%M:%S", localtime())
	print(results['projected_free_cash_flow'])
	return render_template('result.html', ticker = result['TICKER'], growthData = MarqueeData.growth, financialReturnsData = MarqueeData.financialReturns, integeratedData = MarqueeData.integrated, multipleData = MarqueeData.multiples, date = date, projectedCashFlow = results['projected_free_cash_flow'], discountRate = results['discount_rate'], terminalValue = results['terminal_value'], DCF = results['DCF'], shareValue = results['share_value'], EBIDTA = results['EBIDTA'], marketShareValue = results['market_share_value'], marketCap = results['market_cap'], shareDiff = round(results['share_diff'], 4), evalDiff = round(results['eval_diff'], 4))


@app.route('/404')
def error():
	return render_template('404.html')

if __name__ == '__main__':
	app.run(debug = True)