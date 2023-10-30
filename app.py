from flask import Flask, render_template, request, jsonify
import Create_database

app = Flask(__name__)
@app.route("/")
def hello_world():
    return "Hello World"

table_names =['covid19_africa', 'covid19_asia', 'covid19_europe', 'covid19_northamerica', 'covid19_southamerica', 'covid19_world', 'covid19_tests', 'world_population']
update_dict = {
    'Asia': "covid19_asia", 
    'Africa': "covid19africa",
    'Europe': "covid19_europe", 
    'North America': "covid19_northamerica",
    'South America': 'covid19_southamerica', 
    'Oceania': 'covid19_oceania', 
    'World' : 'covid19_world'
}

@app.route('/dashboard2',  methods=['POST', 'GET'] )  # Gets called when home page is requested
def home():
    date_from = request.form['start_date']  # Get the given 'from date' from the form
    date_to =   request.form['end_date']  # Get the given 'to date' from the form
    if date_from > date_to:  # If user gives a from date that's after to date
        # swap dates
        temp = date_from
        date_from = date_to
        date_to = temp

    if date_from and date_to:  # If both (from and to) dates were given from the user
        # Get per day cases and deaths for the 'country' between 'date_from' and 'date_to' dates
        covid19africa = Create_database.select_data_between_dates('covid19africa', date_from, date_to,)
        covid19_europe = Create_database.select_data_between_dates('covid19_europe', date_from, date_to,)
        covid19_asia = Create_database.select_data_between_dates('covid19_asia', date_from, date_to,)
        covid19_world = Create_database.select_data_between_dates('covid19_world',date_from, date_to,)
        covid19_oceania = Create_database.select_data_between_dates('covid19_oceania',date_from, date_to,)
        covid19_northamerica = Create_database.select_data_between_dates('covid19_northamerica',date_from, date_to,)
        covid19_southamerica = Create_database.select_data_between_dates('covid19_southamerica',date_from, date_to,) 
        # country_names = Create_database.select_total_countries()
        result = Create_database.select_data_between_dates('covid19_world', date_from, date_to,)
        return render_template(
            'dashboard2.html',

        )

@app.route('/map', methods=['POST', 'GET'])  # Called when form is submitted for map.html
def result():
    date_from = request.get['start_date']  # Get the given 'from date' from the form
    # date_to =   request.form['date2']  # Get the given 'to date' from the form
    country = request.form.get['Country']  # Country
    # table_names = request.form['Continent'] 
    # continent = update_dict[table_names]
    # if date_from > date_to:  # If user gives a from date that's after to date
    #     # swap dates
    #     temp = date_from
    #     date_from = date_to
    #     date_to = temp

    # if date_from and date_to:  # If both (from and to) dates were given from the user
    #     # Get per day cases and deaths for the 'country' between 'date_from' and 'date_to' dates
    #     result = Create_database.select_data_between_dates('covid19_world', date_from, date_to,)
    # else:  # User selected only a country
    #     # Get per day cases and deaths for the 'country' for all available dates
    #     result = Create_database.select_total_continents(table_names)

    result2 = Create_database.country(country, date_from)  # Get total cases and deaths for 'country'
    result = Create_database.select_tests(country,date_from)

    if result2:
        date = result2[0][0]
        country = result2[0][1]
        confirmed = result2[0][2]
        deaths = result2[0][3]
        recovered = result2[0][4]
        active = result2[0][5]
    else:
        date = None
        country = None
        confirmed = None
        deaths = None
        recovered = None
        active = None

    if result:
        total_tests = result[0][2]
    else:
        total_tests = None
    return render_template(
        'map.html',
        # rlt4=result,
        rlt2=result2,
        # cntr_nms=country_names,
        # gl_cs_dths=global_cases_deaths,
        # d_from=date_from,
        # d_to=date_to,
        date = date,
        country = country,
        confirmed = confirmed,
        deaths = deaths,
        recovered = recovered,
        active = active,
        total_tests = total_tests,
    )

    
#Admin Login route
# @app.route('/login')
# def login():
#     return render_template('login.html')

#User Login route
# @app.route('/userlogin')
# def login():
    # return render_template('userlogin.html')

#--------------------------------------------------------------
security_codes = ["1234", "abcd"]

@app.route('/adminsignup', methods=['GET', 'POST'])
def adminsignup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        security_code = request.form['security_code']

        if security_code in security_codes:
            # Add code for admin account creation.
            return render_template('adminlogin.html')
        else:
            return render_template('adminsignup.html')

    return render_template('adminsignup.html')

@app.route('/add_entries', methods=['GET', 'POST'])
def adminlogin():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     table_names = request.form['Continent'] 
    #     continent = update_dict[table_names]
    #     country = request.form['Country']
    #     reigion = request.form['Region']
    #     confirmed =  request.form['Confirmed Case']
    #     deaths = request.form['Deaths']
    #     recovered = request.form['Recovered']
    #     active = request.form['Active Cases']
    #     total_test = request.form['Total Tests']
    #     population = request.form['Population']
    #     tests_per_million = request.form['Test per Million']
    #     test_per_person = request.form['Tests per Person']
    #     date = request.form['Date']

    #     if Create_database.correct_authentication(username, password):
    #         # Redirect to the admin panel or handle it as needed.
    #         # check the logic
    #         Create_database.update(continent, date, country, reigion, confirmed, deaths, recovered, active, total_test, population, tests_per_million, test_per_person)
        #     return render_template('dashboard2.html')
        # else:
        #     return render_template('add_entries.html')

    return render_template('map.html')


if __name__ == '__main__':
    # This should be changed later  
    app.run(host='0.0.0.0', debug=True)


