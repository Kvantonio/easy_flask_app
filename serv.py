from flask import Flask, url_for, request,render_template
from markupsafe import escape
from faker import Faker


app = Flask(__name__)
fake = Faker()

@app.route('/')
def index():
    return '<h1>index</h1>'

@app.route('/requirements/')
def requirements(data_list = None):
    link = url_for('static', filename = 'requirements.txt')
    data_list = []
    with open('.' + link) as read:
        for i in read:
            data_list.append(i)

    return render_template('requirements.html', data_list=data_list) 


@app.route('/generate-users/')
@app.route('/generate-users/<count>')
def generateusers(count=100):
    count = escape(count)
    if (count.isdigit() == True) and (int(count)<=100):
        count = int(count)
        names = [fake.unique.first_name() for i in range(count)]
        adr = [fake.ascii_free_email() for j in range(count)]
        dict_data = {}
        for i in range(count):
            dict_data[names[i]] = adr[i]
        return render_template('generate-users.html', dict_data=dict_data)
    else:
        return '"{}" - invalid data'.format(count)


@app.route('/mean/')
def mean(data_list = None):
    link = url_for('static', filename = 'hw.csv')
    data_list = []
    with open('.' + link, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['Height(Inches)'], row['Weight(Pounds)'])

    return render_template('mean.html')

#@app.route('/user/<count>')
#def profile(username):
#    return '{}\'s profile'.format(escape(username))

