from __future__ import absolute_import, division, print_function, unicode_literals

import urllib.request, json

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np

NUM_DATA_POINTS = 4
NUM_POINTS_PER_SYMBOL = 6

TRAIN_SYMBOLS = ["GOOGL", "FB", "AMZN", "COKE", "TSLA", "VZ", "MSFT", "IBM", "CIEN", "INTC"]

EBITDA_MULTIPLE = 10

CASH_FLOW_URL = "https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/"
QUARTER_STRING = "?period=quarter"

BETA_URL = "https://financialmodelingprep.com/api/v3/company/profile/"
METRICS_URL = "https://financialmodelingprep.com/api/v3/company-key-metrics/"
ENTERPRISE_URL = "https://financialmodelingprep.com/api/v3/enterprise-value/"

INCOME_STATEMENT_URL = "https://financialmodelingprep.com/api/v3/financials/income-statement/"
BALANCE_SHEET_URL = "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/"

training_input = []
training_labels = []

def getCashFlows(ticker, num_points):
    with urllib.request.urlopen(CASH_FLOW_URL + ticker + QUARTER_STRING) as url:
        data = json.loads(url.read().decode())
        output = []

        for i in range(num_points):
            output.append(data.get("financials")[i].get("Free Cash Flow"))

        return [float(x) for x in output]


def getDiscount(ticker):
    beta = json.loads(urllib.request.urlopen(BETA_URL + ticker).read().decode())
    cost_of_equity = 2.1 + 6.4 * float(beta.get("profile").get("beta"))

    income_statement = json.loads(urllib.request.urlopen(INCOME_STATEMENT_URL + ticker).read().decode())
    balance_sheet = json.loads(urllib.request.urlopen(BALANCE_SHEET_URL + ticker).read().decode())
    total_debt = float(balance_sheet.get("financials")[0].get("Total debt"))

    if total_debt == 0:
        return 7.751645014131961
    else:
        cost_of_debt = 100 * float(income_statement.get("financials")[0].get("Interest Expense")) / float(balance_sheet.get("financials")[0].get("Total debt"))
        metrics = json.loads(urllib.request.urlopen(METRICS_URL + ticker).read().decode())
        debt_percent = float(metrics.get("metrics")[0].get("Debt to Assets"))
        equity_percent = debt_percent / float(metrics.get("metrics")[0].get("Debt to Equity"))

    return cost_of_equity * equity_percent + cost_of_debt * debt_percent * (1 - 0.06) + 4


def getTerminal(ticker):
    income_statement = json.loads(urllib.request.urlopen(INCOME_STATEMENT_URL + ticker).read().decode())
    EBITDA = float(income_statement.get("financials")[0].get("EBITDA"))

    return EBITDA * EBITDA_MULTIPLE


def getShareNumber(ticker):
    enterprise = json.loads(urllib.request.urlopen(ENTERPRISE_URL + ticker).read().decode())
    return float(enterprise.get("enterpriseValues")[0].get("Number of Shares"))


def addFCF(ticker):
    global training_labels, training_input

    data = getCashFlows(ticker, NUM_POINTS_PER_SYMBOL + NUM_DATA_POINTS + 1)
    train_data = []

    for count, point in enumerate(data[1:]):
        train_data.append(((point / data[count]) + 3) * (2/15))

    for counter in range(NUM_POINTS_PER_SYMBOL):
        training_input.append([train_data[counter:][:NUM_DATA_POINTS]])
        training_labels.append(train_data[counter + NUM_DATA_POINTS])


def predictFCF(ticker, model):
    data = getCashFlows(ticker, NUM_DATA_POINTS + 2)
    input_data = []
    output = []

    for count, point in enumerate(data[1:], 0):
        input_data.append(((point / data[count]) + 3) * (2/15))

    prediction_index = model.predict(np.asarray([[input_data[:-1]]]))[0][1]
    temp_last = data[0]

    print(prediction_index)

    for i in range(20):
        temp_last = (temp_last * (0.5 + prediction_index))
        output.append(temp_last)

    return output


def startModel():
    global training_input, training_labels

    for symbols in TRAIN_SYMBOLS:
        addFCF(symbols)

    training_input = np.asarray(training_input)
    training_labels = np.asarray(training_labels)

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(1, NUM_DATA_POINTS)),
        keras.layers.Dense(4, activation=tf.nn.relu),
        keras.layers.Dense(2, activation=tf.nn.softmax),
    ])

    model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

    model.fit(training_input, training_labels, epochs=5)

    return model


def getDCF(ticker):
    model = startModel()
    DCF = 0
    projection = predictFCF(ticker, model)
    discount_rate = getDiscount(ticker)
    terminal = getTerminal(ticker)

    for count, projected_cash_flow in enumerate(projection, 1):
        DCF += projected_cash_flow / ((1 + discount_rate) ** count)
    DCF += terminal

    enterprise = json.loads(urllib.request.urlopen(ENTERPRISE_URL + ticker).read().decode())
    current_stock = enterprise.get("enterpriseValues")[0].get("Stock Price")
    market_cap = enterprise.get("enterpriseValues")[0].get("Market Capitalization")

    return {'projcted_free_cash_flow':projection, 'discount_rate':discount_rate, 'terminal_value':terminal,
            'DCF':DCF, 'share_value':(DCF / getShareNumber(ticker)), 'market_share_value':current_stock,
            'market_cap':market_cap}
