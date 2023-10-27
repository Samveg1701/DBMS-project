from flask import Flask, render_template, request
import Create_database


app = Flask(__name__)
@app.route("/")
def hello_world():
    return "Hello World"

table_names =['covid19_africa', 'covid19_asia', 'covid19_europe', 'covid19_northamerica', 'covid19_southamerica', 'covid19_world', 'covid19_tests', 'world_population']
@app.route('/home')  # Gets called when home page is requested
def home():
    result = Create_database.select_total_continents(table_names[0])
    country_names = Create_database.select_total_countries()
    return render_template(
        'home.html',
        rlt=result,
        cntr_nms=country_names,
    )

@app.route('/result', methods=['POST'])  # Called when form is submitted
def result():
    date_from = request.form['date1']  # Get the given 'from date' from the form
    date_to = request.form['date2']  # Get the given 'to date' from the form

    if date_from > date_to:  # If user gives a from date that's after to date
        # swap dates
        temp = date_from
        date_from = date_to
        date_to = temp

    if date_from and date_to:  # If both (from and to) dates were given from the user
        # Get per day cases and deaths for the 'country' between 'date_from' and 'date_to' dates
        result = Create_database.select_data_between_dates(table_names, date_from, date_to, )
    else:  # User selected only a country
        # Get per day cases and deaths for the 'country' for all available dates
        result = Create_database.select_total_continents(table_names[0])

    result2 = json_to_database.select_cases_and_deaths_per_country(country)  # Get total cases and deaths for 'country'

    return render_template(
        'home.html',
        rlt4=result,
        rlt2=result2,
        cntr_nms=country_names,
        gl_cs_dths=global_cases_deaths,
        d_from=date_from,
        d_to=date_to,
    )

if __name__ == '__main__':
    # This should be changed later  
    app.run(host='0.0.0.0', debug=True)
    
#Login route
@app.route('/login')
def login():
    return render_template('login.html')







