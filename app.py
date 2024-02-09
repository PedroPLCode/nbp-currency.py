from flask import Flask, render_template, request
import csv
import requests

nbp_url = "http://api.nbp.pl/api/exchangerates/tables/C?format=json"
csv_filemane = 'currencies.csv'

response = requests.get(nbp_url)
data = response.json()
currencies_data = data[0]['rates']

app = Flask(__name__)

def export_currencies_array_to_csv_file(currencies_array, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['currency', 'code', 'bid', 'ask']
        writer = csv.DictWriter(csvfile, delimiter =';', fieldnames=fieldnames)
        writer.writeheader()
        for item in currencies_array:
            writer.writerow({'currency': item['currency'],
                             'code': item['code'],
                             'bid': item['bid'],
                             'ask': item['ask']})

@app.route("/", methods=["GET", "POST"])
def currencies_view():
    if request.method == "POST":
        data = request.form
        currency_code = data.get('currencies')
        quantity_to_buy = float(data.get("quantity"))
        
        currency = False
        for item in currencies_data:
            if item['code'] == currency_code:
                currency = float(item['ask'])
                
        pln_cost = round((quantity_to_buy * currency), 2)
        return render_template('currencies-output.html', 
                               quantity_to_buy=round(quantity_to_buy, 2), 
                               currency_code=currency_code, 
                               pln_cost=pln_cost)

    export_currencies_array_to_csv_file(currencies_data, csv_filemane)
    currency_codes_list = [item['code'] for item in currencies_data]     
    return render_template('currencies-input.html', 
                           currency_codes_list=currency_codes_list)
    
if __name__ == '__main__':
    app.run(debug=True)