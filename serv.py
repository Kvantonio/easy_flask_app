from flask import Flask, url_for, request, render_template
from markupsafe import escape
from faker import Faker
import csv
import requests

app = Flask(__name__)
fake = Faker()

@app.route('/')
def index():
    return '<h1>index</h1>'

@app.route('/requirements/')
def requirements(data_list = None):
    link = '.' + url_for('static', filename = 'requirements.txt')
    data_list = []
    with open(link) as read:
        for i in read:
            data_list.append(i)
    return render_template('requirements.html', data_list=data_list) 


@app.route('/generate-users/')
@app.route('/generate-users/<count>')
def generateusers(count=100):
    count = escape(count)
    if (count.isdigit() == True) and (int(count) <= 100):
        count = int(count)
        names = [fake.unique.first_name() for i in range(count)]
        adr = [fake.ascii_free_email() for j in range(count)]
        dict_data = {}
        for i in range(count):
            dict_data[names[i]] = adr[i]
        return render_template('generate-users.html', dict_data = dict_data)
    else:
        return '"{}" - invalid data'.format(count)


@app.route('/mean/')
def mean():
    link = '.' + url_for('static', filename = 'hw.csv')
    t = 0
    height_inch = 0.0
    weight_pound = 0.0
    with open(link) as csv_file:
        reader = csv.reader(csv_file,  delimiter = ',', skipinitialspace=True)#?????????????????????
        for row in reade:
            if len(row)!=0 and row[0].isdigit():
                height_inch += float(row[1])
                weight_pound += float(row[2])
                t+=1
    height_cm = (height_inch * 2.54)/t
    weight_kg = (weight_pound * 0.453592)/t
    return render_template('mean.html', height_cm = height_cm, weight_kg = weight_kg)#???????????


@app.route('/space/')
def space():
    r = requests.get('http://api.open-notify.org/astros.json')
    num_cosmonaut = r.json()["number"]
    return f'<p>Now in the station: <b>{ num_cosmonaut }</b> cosmonunt!</p>' #?????