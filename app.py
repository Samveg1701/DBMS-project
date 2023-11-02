from flask import Flask, render_template, request, jsonify
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

def parse_data(data):
    date_array = []
    first_value_array = []
    second_value_array = []
    third_value_array = []
    fourth_value_array = []

    for entry in data:
        date_array.append(entry[0])
        first_value_array.append(entry[1])
        second_value_array.append(entry[2])
        third_value_array.append(entry[3])
        fourth_value_array.append(entry[4])
    return [date_array, first_value_array, second_value_array, third_value_array, fourth_value_array]


@app.route('/dashboard2.html',  methods=['POST','GET'] )  # Gets called when home page is requested
def home():
    if request.method == 'POST':
        try:
            data = request.json  # Get the JSON data from the request
            date_from = data.get('date_from')  
            date_to = data.get('date_to')  
            print("date_from:", date_from)
            print("date_to:", date_to)

            if date_from > date_to:  # If user gives a from date that's after to date
                # swap dates
                temp = date_from
                date_from = date_to
                date_to = temp

            if date_from and date_to:  # If both (from and to) dates were given from the user
                # Get per day cases and deaths for the 'country' between 'date_from' and 'date_to' dates
                covid19_africa = Create_database.select_data_between_dates('covid19_africa', date_from, date_to,)
                covid19_europe = Create_database.select_data_between_dates('covid19_europe', date_from, date_to,)
                covid19_asia = Create_database.select_data_between_dates('covid19_asia', date_from, date_to,)
                covid19_world = Create_database.select_data_between_dates('covid19_world',date_from, date_to,)
                covid19_oceania = Create_database.select_data_between_dates('covid19_oceania',date_from, date_to,)
                covid19_northamerica = Create_database.select_data_between_dates('covid19_northamerica',date_from, date_to,)
                covid19_southamerica = Create_database.select_data_between_dates('covid19_southamerica',date_from, date_to,) 
                # country_names = Create_database.select_total_countries()
                # covid19_world = Create_database.select_data_between_dates('covid19_world', date_from, date_to,)

                # Access the data arrays for each region as needed
                africa_date_array = parse_data(covid19_africa)
                europe_date_array = parse_data(covid19_europe)
                asia_date_array = parse_data(covid19_asia)
                world_date_array = parse_data(covid19_world)
                oceania_date_array = parse_data(covid19_oceania)
                northamerica_date_array = parse_data(covid19_northamerica)
                southamerica_date_array = parse_data(covid19_southamerica)

                return_result = {
                    'covid19_africa': africa_date_array,
                    'covid19_europe': europe_date_array,
                    'covid19_asia': asia_date_array,
                    'covid19_world': world_date_array,
                    'covid19_oceania': oceania_date_array,
                    'covid19_northamerica': northamerica_date_array,
                    'covid19_southamerica': southamerica_date_array,
                }

                return jsonify(return_result)
            
        except Exception as e:
            print(f"Error: {str(e)}")  # Print the exception message
            return render_template('error.html', error=str(e)), 500

    elif request.method == 'GET':
        # Your GET request handling logic here
        # For example, you might want to initialize some variables or perform other operations specific to the GET request
        # Then, render the 'dashboard2.html' template
        return render_template('dashboard2.html')  # Change 'dashboard2.html' to your actual template file

    else:
        return 'Method Not Allowed', 405

@app.route('/map.html', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        try:
            data = request.json  # Get the JSON data from the request
            date_from = data.get('date')  # Extract the 'date' field from the JSON data
            country = data.get('country')  # Extract the 'country' field from the JSON data
            print("Received date:", date_from)
            print("Received country:", country)

            if not date_from or not country:
                return render_template('error.html', error="Invalid request. Missing required fields."), 400

            result2 = Create_database.country("covid19_world",country, date_from)  # Get total cases and deaths for 'country'
            result = Create_database.select_tests(country, date_from)
            print(result2)
            if result2:
                date_from = result2[0][0]
                country = result2[0][1]
                confirmed = result2[0][2]
                deaths = result2[0][3]
                recovered = result2[0][4]
                active = result2[0][5]
            else:
                date_from, country, confirmed, deaths, recovered, active = (None, None, None, None, None, None)

            if result:
                total_tests = result[0][2]
            else:
                total_tests = None
            
            # Assuming confirmed, deaths, recovered, active, and total_tests are defined elsewhere
            response_data = {
                'date': date_from,
                'country': country,
                'confirmed': confirmed,
                'deaths': deaths,
                'recovered': recovered,
                'active': active,
                'total_tests': total_tests,
            }

            # Return the data as a JSON response
            return jsonify(response_data)

        except Exception as e:
            print(f"Error: {str(e)}")  # Print the exception message
            return render_template('error.html', error=str(e)), 500

    elif request.method == 'GET':
        # Your GET request handling logic here
        # For example, you might want to initialize some variables or perform other operations specific to the GET request
        # Then, render the 'map.html' template
        return render_template('map.html')  # Change 'map.html' to your actual template file

    else:
        return 'Method Not Allowed', 405
    
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

@app.route('/add_entries.html', methods=['GET'])
def admin_as_get():
    return render_template('add_entries.html')

@app.route('/add_entries.html', methods=['POST'])
def add_entries():
    data = request.json  # Retrieve JSON data from the request

    username = data['username']
    password = data['password']
    tableName = data['tableName']
    continent = update_dict.get(tableName)  # Assuming update_dict is a predefined dictionary
    country = data['country']
    region = data['region']
    confirmed = data['confirmed']
    deaths = data['deaths']
    recovered = data['recovered']
    active = data['active']
    totalTests = data['totalTests']
    population = data['population']
    testsPerMillion = data['testsPerMillion']
    testsPerPerson = data['testsPerPerson']
    date = data['date']
    auth = Create_database.correct_authentication(username, password)
    if auth==True:
        # Redirect to the admin panel or handle it as needed
        # Check the logic
        Create_database.update(continent, date, country, region, confirmed, deaths, recovered, active, totalTests, population, testsPerMillion, testsPerPerson)
        return render_template('dashboard2.html')
    else:
        return render_template('add_entries.html')

if __name__ == '__main__':
    # This should be changed later  
    app.run(host='0.0.0.0', debug=True)


