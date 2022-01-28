# if we want to create routes for our app, we need access to our app
# import the app object we made

from app import app
from flask import flash, render_template, request
from flask_login import login_required
from .forms import currentRatesForm, historicalRatesForm, DATE_FORMAT

@app.route('/historical', methods=['GET', 'POST'])
@login_required
def historical():
    form = historicalRatesForm() # used by both GET and POST
    rates = []
    dates = []
    symbols = get_symbols()
    form.base.choices = symbols
    form.rate.choices = symbols

    if request.method == 'POST':
        dates, rates = get_historical_rates(form)

    return render_template('historical.html', form=form, rates=rates, dates=dates) # GET    

@app.route('/', methods=['GET', 'POST'])
@app.route('/current', methods=['GET', 'POST'])
@login_required
def current():
    form = currentRatesForm() # used by both GET and POST
    rates = {}
    symbols = get_symbols()
    form.base.choices = symbols
    form.rate.choices = symbols

    if request.method == 'POST':
        # if the user submits form
        if form.rate.data:
            rates = get_current_rates(form)
        else:
            flash('Select one or more Rate Currency(s)', category='danger')
            rates = {}
            

    return render_template('current.html', form=form, rates=rates) # GET


def get_symbols():
    import requests as r
    data = r.get('https://api.exchangerate.host/symbols')
    if data.status_code == 200:
        data = data.json()
        symbols = list(data['symbols'])
        return symbols


def get_historical_rates(form: currentRatesForm):
    dates = []
    rates = []
    date_from = form.date_from.data.strftime(DATE_FORMAT)
    date_to = form.date_to.data.strftime(DATE_FORMAT)
    url = f'https://api.exchangerate.host/timeseries?start_date={date_from}&end_date={date_to}&base={form.base.data}&symbols={form.rate.data}'
    import requests as r
    api_data = r.get(url).json()['rates']
    for date, rate in api_data.items():
        api_rates = list(rate.values())
        if api_rates:      
            dates.append(date)
            rates.append(api_rates[0])
    return dates, rates

def get_current_rates(form: historicalRatesForm):
    api_symbols = ','.join(form.rate.data)
    url = f'https://api.exchangerate.host/latest?&base={form.base.data}&symbols={api_symbols}'
    import requests as r
    api_rates = r.get(url).json()['rates']
    # rates = {symbol: rate for symbol, rate in api_rates.items()}
    return api_rates


@app.route('/about')
def about():
    context = {
        'developer': 'Paul',
        'copyright': 'Coding Temple 2022'
    }
    # we're taking that context dictionary and unpacking it's k/v pairs into keyword arguments for the render template function
    # using **kwargs (keyword arguments)
    return render_template('about.html', classname='Foxes78', **context)