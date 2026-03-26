from flask import Flask, render_template, request, redirect
import csv
import os
from datetime import datetime

app = Flask(__name__)

fails = "dati.csv"
dati = []

# Ielādē datus no CSV
def ieladet():
    global dati
    if os.path.exists(fails):
        with open(fails, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            dati = list(reader)

# Saglabā datus CSV
def saglabat():
    with open(fails, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(dati)

@app.route('/')
def index():
    bilance = 0
    for ier in dati:
        summa = float(ier[1])
        if ier[0] == "Ienākums":
            bilance += summa
        else:
            bilance -= summa

    return render_template("index.html", dati=dati, bilance=bilance)

@app.route('/pievienot', methods=['POST'])
def pievienot():
    try:
        tips = request.form['tips']
        summa = float(request.form['summa'])
        apraksts = request.form['apraksts']
        datums = datetime.now().strftime("%Y-%m-%d")

        dati.append([tips, summa, apraksts, datums])
        saglabat()

    except:
        print("Kļūda ievadē!")

    return redirect('/')

@app.route('/dzest/<int:id>')
def dzest(id):
    if 0 <= id < len(dati):
        dati.pop(id)
        saglabat()
    return redirect('/')

if __name__ == "__main__":
    ieladet()
    app.run(debug=True)