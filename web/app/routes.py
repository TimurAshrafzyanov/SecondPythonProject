import requests
from flask import render_template, redirect, request
from app import app
from app.forms import StartForm


@app.route('/', methods=['GET', 'POST'])
def start():
    form = StartForm()
    if form.validate_on_submit():
        return redirect('/choise')
    return render_template('start.html', form=form)

@app.route('/choise', methods=['GET', 'POST'])
def choose():
    if request.method == 'POST':
        city = request.form['city']
        return redirect('/cities?city={}'.format(city))
    return render_template('choise.html')


@app.route('/cities')
def city_searching():
    MY_KEY = '5d0b20589fbca89baab98af383e6858a'
    current_city = request.args.get('city')
    if not current_city:
        current_city = 'kazan'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'.format(current_city, MY_KEY)
    response = requests.get(url).json()
    error = ''
    if response.get('cod') != 200:
        message = response.get('message', '')
        error = 'Error getting weather foreast for {}, {}'.format(current_city.title(), message)
        return render_template('final.html', error=True, message=error)
    name = current_city.title()
    current_pressure = response.get('main', {}).get('pressure')
    current_temperature = round(response.get('main', {}).get('temp') - 273.15, 2)
    current_humidity = response.get('main', {}).get('humidity')
    if not current_temperature:
        error = 'Error getting weather forecast for {}'.format(current_city.title())
        return render_template('final.html', error=True, message=error)
    return render_template('final.html', error=False, name=name, 
            temp=current_temperature, pres=current_pressure, hum=current_humidity)
