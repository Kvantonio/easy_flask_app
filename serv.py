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
def requirements(data_list = None):              #1
    link = 'requirements.txt'
    data_list = []
    with open(link) as read:
        for i in read:
            data_list.append(i)
    return render_template('requirements.html', data_list=data_list) 


@app.route('/generate-users/')
@app.route('/generate-users/<int:count>')
def generateusers(count=100):                    #2
    dict_data = {} 
    for i in range(count):  #добавляем данные в словарь для удобного вызова
        dict_data[fake.unique.first_name()] = fake.ascii_free_email()  
    return render_template('generate-users.html', dict_data = dict_data)



@app.route('/mean/')                            #3
def mean():
    link = 'static/hw.csv'
    t = 0 #счетчик количества данных
    height_inch = 0.0
    weight_pound = 0.0
    with open(link) as csv_file:
        reader = csv.reader(csv_file,  delimiter = ',', skipinitialspace=True) #считываем данные и делим их по запятой игнорируя пробелы
        for row in reader:
            if len(row)!=0 and row[0].isdigit(): #проверка на то что это число и список не пустой
                                                #чтобы отсечь первую строку и в самом конце пустые строки                       
                height_inch += float(row[1])
                weight_pound += float(row[2])
                t+=1
    height_cm = (height_inch * 2.54)/t #переводим в см и получаем средний рост
    weight_kg = (weight_pound * 0.453592)/t #переводим в кг и получаем средний вес
    #не делал перевод через библиотеки
    return render_template('mean.html', height_cm = height_cm, weight_kg = weight_kg)


@app.route('/space/')                           #4
def space():
    r = requests.get('http://api.open-notify.org/astros.json')
    num_cosmonaut = r.json()["number"]
    return f'<p>Now in the station: <b>{ num_cosmonaut }</b> cosmonunt!</p>'