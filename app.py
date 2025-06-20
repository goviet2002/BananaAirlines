from flask import Flask, render_template, request, session, jsonify
import string, random, psycopg2
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(minutes=1)

config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', 5432),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'postgres')
}

def get_conn():
    return psycopg2.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        dbname=config['database']
    )
    
conn = get_conn()

cur = conn.cursor()

def close_db(cur, conn):
    conn.commit()
    cur.close()
    conn.close()

class Logger:
	def log(str, level ='info'):
		with open('Log.md','a') as t:
			t.write(f"{level}: {str}\n")
   
def generate_unique_id():
    conn = get_conn()

    cur = conn.cursor()
    while True:
        id = ''.join(random.choices(string.ascii_uppercase, k=5)) + ''.join(random.choices(string.digits, k=5))
        # Check if this ID already exists in the database
        cur.execute("SELECT * FROM user WHERE UserID = %s", (id,))
        if not cur.fetchone():
            # If not, we can use this ID
            return id

class SQL:
    sql1_myFlights = """
        SELECT f.FlightCode, 
        CONCAT(c1.City, ' (', f.SourceAirport, ')') AS SourceCity, 
        CONCAT(c2.City, ' (', f.DestinationAirport, ')') AS DestinationCity, f.Distance, 
        TO_CHAR(f.DepartureTime, 'DD-MM-YYYY HH24:MI') as DepartureTime, 
        TO_CHAR(f.ArrivalTime, 'DD-MM-YYYY HH24:MI') as ArrivalTime, t.Status, t.TicketID,
        CASE 
            WHEN t.Baggage = 1 THEN 'Yes'
            ELSE 'No'
        END as Baggage,
        CASE 
            WHEN t.Request = 1 THEN 'Yes'
            ELSE 'No'
        END as Request, 
        CASE 
            WHEN t.CheckIn = 1 THEN 'Yes'
            ELSE 'No'
        END as CheckIn
        FROM flight f
        JOIN cities c1 ON f.SourceAirport = c1.Code
        JOIN cities c2 ON f.DestinationAirport = c2.Code
        JOIN ticket t ON f.FlightCode = t.FlightCode
        JOIN client cl ON cl.ClientID = t.UserID
        WHERE cl.ClientID = %s AND f.DepartureTime > NOW()
    """
    sql_get_departure = """
    SELECT DISTINCT cities.City 
    FROM flight JOIN cities ON flight.SourceAirport = cities.Code
    """
    sql1_get_destination = "SELECT Code FROM cities WHERE City = %s"
    sql2_get_destination = """
        SELECT DISTINCT cities.City 
        FROM flight 
        JOIN cities ON flight.DestinationAirport = cities.Code 
        WHERE flight.SourceAirport = %s
        """
    sql_get_date = """
    SELECT DISTINCT DATE(DepartureTime) 
    FROM flight 
    WHERE SourceAirport = %s AND DestinationAirport = %s AND DepartureTime > NOW()
    """
    sql1_login = '''
        SELECT u.*
        FROM "user" u
        WHERE u.username = %s AND u.password = %s
    '''
    sql2_login = '''
        SELECT c.*
        FROM client c
        WHERE c.ClientID = %s
    '''
    sql3_login = '''
        SELECT e.*
        FROM employee e
        WHERE e.EmployeeID = %s
    '''
    sql1_register = "INSERT INTO \"user\" (username, UserID, password, UserType) VALUES (%s, %s, %s, %s)"
    sql2_register = "INSERT INTO client (ClientID, FirstName, LastName, Email, MilesEarned, Tier, Birthdate, Gender, MobileNumber, Country) VALUES (%s, %s, %s, %s, 0, %s, %s, %s, %s, %s)"
    sql3_register = """
        SELECT client.FirstName, client.LastName, client.Email, "user".UserID, client.Tier, client.MilesEarned, offer.Offers 
        FROM client 
        JOIN "user" ON client.ClientID = "user".UserID 
        JOIN offer ON client.Tier = offer.Tier 
        WHERE client.Email = %s AND "user".username = %s
        """
    sql1_account = '''
        SELECT c.FirstName, c.LastName, c.Email, u.UserID, c.Tier, c.MilesEarned, o.Offers
        FROM "user" u
        JOIN client c ON u.UserID = c.ClientID
        JOIN offer o ON c.Tier = o.Tier
        WHERE u.UserID = %s
        '''
    sql2_account = '''
        SELECT t.TicketID, 
    CASE 
        WHEN f.SourceAirport IS NOT NULL THEN CONCAT(c1.City, ' (', f.SourceAirport, ')')
        ELSE 'Flight not available'
    END as SourceCity, 
    CASE 
        WHEN f.DepartureTime IS NOT NULL THEN TO_CHAR(f.DepartureTime, 'DD-MM-YYYY HH24:MI')
        ELSE 'Flight not available'
    END as DepartureTime, 
    CASE 
        WHEN f.DestinationAirport IS NOT NULL THEN CONCAT(c2.City, ' (', f.DestinationAirport, ')')
        ELSE 'Flight not available'
    END as DestinationCity, 
    CASE 
        WHEN f.ArrivalTime IS NOT NULL THEN TO_CHAR(f.ArrivalTime, 'DD-MM-YYYY HH24:MI')
        ELSE 'Flight not available'
    END as ArrivalTime, 
    t.FlightCode, t.Class, t.Paid, t.Status,
    CASE 
        WHEN t.CheckIn = 1 THEN 'Yes'
        ELSE 'No'
    END as CheckIn,
    CASE 
        WHEN t.Baggage = 1 THEN 'Yes'
        ELSE 'No'
    END as Baggage,
    CASE 
        WHEN t.Class = 'Economy' AND f.Distance IS NOT NULL THEN f.Distance
        WHEN t.Class = 'Business' AND f.Distance IS NOT NULL THEN f.Distance * 2
        WHEN t.Class = 'First Class' AND f.Distance IS NOT NULL THEN f.Distance * 3
        ELSE NULL
    END as Miles
        FROM ticket t
        LEFT JOIN flight f ON t.FlightCode = f.FlightCode
        LEFT JOIN class p ON f.FlightCode = p.flightID
        LEFT JOIN cities c1 ON f.SourceAirport = c1.Code
        LEFT JOIN cities c2 ON f.DestinationAirport = c2.Code
        WHERE t.UserID = %s
        ORDER BY 
            CASE 
                WHEN (CASE WHEN f.DepartureTime IS NOT NULL THEN TO_CHAR(f.DepartureTime, 'DD-MM-YYYY HH24:MI') ELSE 'Flight not available' END) = 'Flight not available' THEN 0
                ELSE 1
            END DESC,
            f.DepartureTime DESC;
        '''
    sql1_bookflight = """
    SELECT f.FlightCode, CONCAT(c1.City, ' (', f.SourceAirport , ')'), 
            CONCAT(c2.City, ' (', f.DestinationAirport , ')'),  
            f.DepartureTime, f.ArrivalTime, f.Distance 
    FROM flight f
    JOIN cities c1 ON f.SourceAirport = c1.Code
    JOIN cities c2 ON f.DestinationAirport = c2.Code
    WHERE f.SourceAirport = %s AND f.DestinationAirport = %s AND DATE(f.DepartureTime) >= %s
    """
    sql2_bookflight = """
    SELECT Tier
    FROM client
    WHERE ClientID = %s
    """
    sql3_bookflight = """
    SELECT Capacity_Economy, Capacity_Business, Capacity_FirstClass
    FROM aircraft a JOIN flight f ON a.AircraftID = f.FlightCode
    WHERE f.SourceAirport = %s AND f.DestinationAirport = %s AND DATE(f.DepartureTime) >= %s
    """
    sql4_bookflight = """
    SELECT
        cl.Price_Economy,
        cl.Price_Business,
        cl.Price_FirstClass
    FROM 
    flight AS f
    JOIN 
    class AS cl ON f.FlightCode = cl.flightID
    WHERE 
        f.SourceAirport = %s AND f.DestinationAirport = %s AND DATE(f.DepartureTime) >= %s
    """
    sql5_bookflight = """
        SELECT Offers
        FROM offer
        WHERE Tier = %s
    """
    sql1_finishbooking = """
        INSERT INTO ticket(TicketID, UserID, PurchaseDate, FlightCode, Class, CheckIn, Baggage, Paid, Status, Request) 
        VALUES (%s, %s, %s, %s, %s, 0, %s, %s, %s, %s);
        """
    sql2_finishbooking = """
            UPDATE aircraft 
            SET Capacity_Economy = CASE WHEN %s = 'Economy' THEN Capacity_Economy - %s ELSE Capacity_Economy END,
                Capacity_Business = CASE WHEN %s = 'Business' THEN Capacity_Business - %s ELSE Capacity_Business END,
                Capacity_FirstClass = CASE WHEN %s = 'First Class' THEN Capacity_FirstClass - %s ELSE Capacity_FirstClass END
            WHERE AircraftID = %s
            """
    sql3_finishbooking = """
        UPDATE client 
        SET MilesEarned = MilesEarned + 
            CASE 
                WHEN %s = 'Economy' THEN %s * 1 * %s
                WHEN %s = 'Business' THEN %s * 2 * %s
                WHEN %s = 'First Class' THEN %s * 3 * %s
            END
        WHERE ClientID = %s;
        """
    sql4_finishbooking = """
        SELECT FirstName, LastName
        FROM client
        WHERE ClientID = %s
        """
    sql_cancel_client = 'UPDATE ticket SET Request = 1, Reason = %s WHERE TicketID = %s'
    sql_validate ="""
    SELECT client.FirstName, client.LastName, ticket.CheckIn
    FROM ticket JOIN client ON ticket.UserID = client.ClientID 
    WHERE ticket.TicketID = %s
    """
    sql_update_checkin = "UPDATE ticket SET CheckIn = 1 WHERE TicketID = %s"
    sql1_insert = """      
        INSERT INTO aircraft (AircraftID, AircraftName,Capacity,
        Capacity_Economy,Capacity_Business,Capacity_FirstClass) 
        VALUES (%s, %s, %s, %s, %s, %s )
    """
    sql2_insert = """      
        INSERT INTO flight (FlightCode, SourceAirport, DestinationAirport,DepartureTime,ArrivalTime,Distance)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    sql3_insert = """INSERT INTO class (flightID,Price_Economy,Price_Business,Price_FirstClass) VALUES (%s, %s, %s, %s)"""
    sql_flights = """
    SELECT a."AircraftName", f.FlightCode, a.Capacity, 
    a.Capacity_Economy, a.Capacity_Business, 
    a.Capacity_FirstClass, f.SourceAirport, 
    f.DestinationAirport, f.DepartureTime, 
    f.ArrivalTime, f.Distance, c.Price_Economy, 
    c.Price_Business, c.Price_FirstClass
    FROM aircraft a
    JOIN flight f ON a.AircraftID = f.FlightCode
    JOIN class c ON f.FlightCode = c.flightID
    """
    sql_offer = """
    SELECT * FROM offer
    ORDER BY 
        CASE 
            WHEN tier = 'Bronze' THEN 1
            WHEN tier = 'Silver' THEN 2
            WHEN tier = 'Gold' THEN 3
            ELSE 4
        END"""
    sql1_update_flight_em = "UPDATE class SET flightID = %s, Price_Economy =%s, Price_Business = %s, Price_FirstClass = %s WHERE flightID = %s"
    sql2_update_flight_em = "UPDATE flight SET FlightCode = %s, SourceAirport = %s, DestinationAirport = %s, DepartureTime = %s ,ArrivalTime = %s ,Distance = %s WHERE FlightCode = %s"
    sql3_update_flight_em = "UPDATE aircraft SET AircraftID = %s, AircraftName = %s, Capacity = %s, Capacity_Economy = %s , Capacity_Business = %s, Capacity_FirstClass = %s WHERE AircraftID = %s"
    sql1_delete_em = 'DELETE FROM aircraft WHERE AircraftID = %s'
    sql2_delete_em = 'DELETE FROM class WHERE flightID = %s'
    sql3_delete_em = 'DELETE FROM flight WHERE FlightCode = %s'
    sql_update_offer_em = "UPDATE offer SET Offers = %s WHERE Tier = %s"
    sql_customer_em = """
    SELECT c.FirstName || ' ' || c.LastName, c.Email, c.ClientID, t.TicketID, t.FlightCode, t.Reason, t.Class, f.Distance
    FROM client c
    JOIN ticket t ON c.ClientID = t.UserID
    JOIN flight f ON t.FlightCode = f.FlightCode
    WHERE t.Request = 1
    """
    sql_cancel_delete = "DELETE FROM ticket WHERE TicketID = %s"
    sql_delete_updatemiles = """
            UPDATE client
            SET MilesEarned = CASE 
                WHEN %s = 'Economy' THEN MilesEarned - %s
                WHEN %s = 'Business' THEN MilesEarned - 2 * %s
                WHEN %s = 'First Class' THEN MilesEarned - 3 * %s
                ELSE MilesEarned
            END;
            """
    sql_delete_update_decline = "UPDATE ticket SET Request = 0 WHERE TicketID = %s"
    sql_check_email = 'SELECT * FROM client WHERE Email = %s'
    sql_check_username = 'SELECT * FROM "user" WHERE username = %s'
    sql_update_capacity = """
            UPDATE aircraft
            SET 
                Capacity_Economy = CASE WHEN %s = 'Economy' THEN Capacity_Economy + 1 ELSE Capacity_Economy END,
                Capacity_Business = CASE WHEN %s = 'Business' THEN Capacity_Business + 1 ELSE Capacity_Business END,
                Capacity_FirstClass = CASE WHEN %s = 'First Class' THEN Capacity_FirstClass + 1 ELSE Capacity_FirstClass END
            WHERE AircraftID = %s;
            """
    sql_getflight_cancel = "SELECT FlightCode FROM ticket WHERE TicketID = %s"
    
@app.route('/')
@app.route('/index')
def homepage(): 
    Logger.log('Accessing homepage', 'info')
    if 'loggedin' in session:
        Logger.log('User is logged in', 'info')
        return render_template('indexSignedInClient.html')
    Logger.log('User is not logged in', 'info')
    return render_template('index.html')

@app.route('/get_departure_cities', methods=['GET'])
def get_departure_cities():
    conn = get_conn()

    cur = conn.cursor()
    
    cur.execute(SQL.sql_get_departure)
    cities = [row[0] for row in cur.fetchall()]
    
    # print(cities)
    close_db(cur,conn)
    return jsonify(cities)

@app.route('/get_destination_cities', methods=['GET'])
def get_destination_cities():
    departure_city = request.args.get('departure')
    Logger.log(f"Departure City: {departure_city}", 'info')
    
    conn = get_conn()

    cur = conn.cursor()
    
    # Convert city name to code
    cur.execute(SQL.sql1_get_destination, (departure_city,))
    departure_code = cur.fetchone()[0]
    
    cur.execute(SQL.sql2_get_destination, (departure_code,))
    cities = [row[0] for row in cur.fetchall()]
    
    Logger.log(f"Destination Cities: {cities}", 'info')
    return jsonify(cities)

@app.route('/get_flight_dates', methods=['GET'])
def get_flight_dates():
    departure_city = request.args.get('departure')
    destination_city = request.args.get('destination')
    conn = get_conn()

    cur = conn.cursor()
    
    # Convert departure city name to code
    cur.execute(SQL.sql1_get_destination, (departure_city,))
    departure_code = cur.fetchone()[0]
    
    # Convert destination city name to code
    cur.execute(SQL.sql1_get_destination, (destination_city,))
    destination_code = cur.fetchone()[0]
    
    # Get available flight dates
    cur.execute(SQL.sql_get_date, (departure_code, destination_code))
    dates = [row[0].strftime('%Y-%m-%d') for row in cur.fetchall()]  # Convert dates to string
    
    Logger.log(f"Available Flight Dates: {dates}", 'info')
    return jsonify(dates)

@app.route('/signIn', methods =['GET', 'POST'])
def login():
    msg = ''
    conn = get_conn()

    cur = conn.cursor()
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cur.execute(SQL.sql1_login, (username, password, ))
        account = cur.fetchone()
        
        if account:
            session['loggedin'] = True
            session['username'] = account[0]
            session['UserID'] = account[1]
            session.permanent = True
            
            
            # Check UserType and render appropriate template
            if account[3] == 'Client':
                cur.execute(SQL.sql2_login, (account[1], ))
                client_account = cur.fetchone()
                # Add additional handling for client_account here if needed

                Logger.log("Client " + username + " logged in.")
                close_db(cur,conn)
                return render_template('indexSignedInClient.html')

            elif account[3] == 'Employee':
                cur.execute(SQL.sql3_login, (account[1], ))
                employee_account = cur.fetchall()
                
                # Fetch all aircrafts, offers from the database
                cur.execute(SQL.sql_flights)
                aircrafts = cur.fetchall()
                
                cur.execute(SQL.sql_offer)
                offers = cur.fetchall()
                
                cur.execute(SQL.sql_customer_em)
                customers = cur.fetchall()
                
                Logger.log("Employee " + username + " logged in.")
                close_db(cur, conn)
                return render_template('employee_homepage.html', offers=offers, aircrafts=aircrafts, customers=customers, values = employee_account)

        else:
            msg = 'Incorrect username / password !'
            Logger.log("User " + username + " failed to log in.")
            close_db(cur,conn)
            return render_template('signIn.html', msg = msg)
    close_db(cur,conn)   
    return render_template('signIn.html')

@app.route('/check_email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data['email']

    conn = get_conn()

    cur = conn.cursor()

    # Query the database to check if the email exists
    cur.execute(SQL.sql_check_email, (email,))
    user = cur.fetchall()

    # Close the database connection
    close_db(cur, conn)
    
    # Return a JSON response
    if user:
        Logger.log('Email using for registration is already existed')
        return jsonify({'emailExists': True})
    else:
        Logger.log('Email using for registration is not existed')
        return jsonify({'emailExists': False})
     
@app.route('/check_username', methods=['POST'])
def check_username():
    data = request.get_json()
    username = data['username']

    conn = get_conn()

    cur = conn.cursor()

    # Query the database to check if the email exists
    cur.execute(SQL.sql_check_username, (username,))
    user = cur.fetchall()

    # Close the database connection
    close_db(cur, conn)
    
    # Return a JSON response
    if user:
        Logger.log('Username using for registration is already existed')
        return jsonify({'username': True})
    else:
        Logger.log('Username using for registration is not existed')
        return jsonify({'username': False})

@app.route('/signUp', methods =['GET', 'POST'])
def register():
    conn = get_conn()

    cur = conn.cursor()
    if (request.method == 'POST' and 'create_username' in request.form and 'create_password' in request.form and 'country' in request.form
    and 'birthdate' in request.form and 'gender' in request.form and 'mobile_number' in request.form    
    and 'email' in request.form and 'first_name' in request.form and 'last_name' in request.form):
        
        username = request.form['create_username']
        password = request.form['create_password']
        email = request.form['email']
        country = request.form['country']
        birthdate = request.form['birthdate']
        gender = request.form['gender']
        mobile_number = request.form['mobile_number']
        first_name = request.form['first_name']
        last_name = request.form['last_name']  
        
        # Generate a unique UserID
        user_id = generate_unique_id()
        
        cur.execute(SQL.sql1_register, (username, user_id, password, "Client"))
        
        # Insert the new client into the database
        cur.execute(SQL.sql2_register, (user_id, first_name,last_name,email,"Bronze",birthdate ,gender,mobile_number,country))
         
        cur.execute(SQL.sql3_register, (email, username))
        data = cur.fetchall()
        
        cur.execute(SQL.sql1_login, (username, password, ))
        account = cur.fetchone()
        session['loggedin'] = True
        session['username'] = account[0]
        session['UserID'] = account[1]
        session.permanent = True  
        
        Logger.log(f"User {username} registered successfully")
        close_db(cur, conn)
        return render_template('account.html', value = data)
    
    close_db(cur, conn)
    return render_template('signUp.html')
  
@app.route('/account', methods=['GET'])
def account_detail():
    conn = get_conn()

    cur = conn.cursor()
    if 'loggedin' in session:
        cur.execute(SQL.sql1_account, (session['UserID'],))
        data = cur.fetchall()
        
        cur.execute(SQL.sql2_account, (session['UserID'],))
        flights = cur.fetchall()
        
        Logger.log("User accessed account details")
        close_db(cur,conn) 
        return render_template('account.html', value=data, flights=flights)
    Logger.log("Session is over, go back to login")
    close_db(cur,conn) 
    return render_template("signIn.html")
    
@app.route('/logout')
def logout():
    # Remove data from session
    session.clear()
    print('loggedin' in session)
    Logger.log("User logged out.")
    # Redirect to home page
    return render_template('index.html')

@app.route('/logout_employee')
def employee_logout():
    # Remove data from employee session
    session.clear()
    print('loggedin' in session)
    Logger.log("Employee logged out.")
    # Redirect to home page
    return render_template('index.html')
    # Remove data from session
    session.clear()
    print('employee_loggedin' in session)
    Logger.log("Employee logged out.")
    # Redirect to employee login page
    return render_template('employee_login.html')

@app.route('/bookFlights')
def bookFlights(): 
    if 'loggedin' in session:
        Logger.log("User go to book flight page")
        return render_template('bookFlights.html')
    Logger.log("Session is over, go to login page")
    return render_template('signIn.html')

@app.route('/tiers')
def tiers(): 
    if 'loggedin' in session:
        Logger.log("User go to tier page")
        return render_template('tiers.html')
    Logger.log("Session is over, go to login page")
    return render_template('signIn.html')

@app.route('/popular')
def popular(): 
    if 'loggedin' in session:
        Logger.log("User go to popular page")
        return render_template('popular.html')
    Logger.log("Session is over, go to login page")
    return render_template('signIn.html')

@app.route('/availableFlights', methods=['POST'])
def availableFlights():
    conn = get_conn()

    cur = conn.cursor()
    
     # Get form data
    departure = request.form.get('von')
    destination = request.form.get('nach')
    date = request.form.get('datum')
    passengers = request.form.get('passagier')
    discount = request.form.get('flightCode')
    
    # Convert date to yy-mm-dd format
    date_in_correct_format = datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
    
    # Convert departure city name to code
    cur.execute(SQL.sql1_get_destination, (departure,))
    departure_code = cur.fetchone()[0]
    
    # Convert destination city name to code
    cur.execute(SQL.sql1_get_destination, (destination,))
    destination_code = cur.fetchone()[0]
    
    cur.execute(SQL.sql1_bookflight, (departure_code, destination_code, date_in_correct_format))
    flights = cur.fetchall()
    
    # Convert timestamps in flights from yy-mm-dd to mm-dd-yy format
    for i in range(len(flights)):
        flights[i] = list(flights[i])
        flights[i][3] = flights[i][3].strftime('%d-%m-%Y %H:%M')
        flights[i][4] = flights[i][4].strftime('%d-%m-%Y %H:%M')
        flights[i] = tuple(flights[i])
    
    cur.execute(SQL.sql2_bookflight, (session['UserID'],))
    tier = cur.fetchall()
    tier = tier[0][0]

    cur.execute(SQL.sql3_bookflight,(departure_code, destination_code, date_in_correct_format))
    capacity = cur.fetchall()
    
    cur.execute(SQL.sql4_bookflight,(departure_code, destination_code, date_in_correct_format))
    offer = cur.fetchall()
    
    cur.execute(SQL.sql5_bookflight, (tier,))
    code = cur.fetchall()
    code = code[0][0]
 
    ## Check the discount and tier and calculate the multiplier
    if discount == code and tier == 'Bronze':
        multiplier = 0.95 * int(passengers)
    elif discount == code and tier == 'Silver':
        multiplier = 0.93 * int(passengers)
    elif discount == code and tier == 'Gold':
        multiplier = 0.90 * int(passengers)
    else:
        multiplier = int(passengers)

    # Apply the multiplier to each value in offer
    offer = [[price * multiplier for price in prices] for prices in offer]
    offer = [tuple(prices) for prices in offer]
    
    
    passengers_list = [(passengers,0)]
    flights_offers = zip(flights, offer, capacity, passengers_list)
    
    Logger.log("User accessed available flights", 'info')
    close_db(cur,conn)
    return render_template('availableFlights.html', flights_offers=flights_offers)

@app.route('/payFlight', methods=['POST'])
def payFlight(): 
    if 'loggedin' in session:
        conn = get_conn()

        cur = conn.cursor()
        
        sql1 = '''
        SELECT c.FirstName, c.LastName, c.Email, u.UserID, c.Tier, c.MilesEarned, o.Offers
        FROM user u
        JOIN client c ON u.UserID = c.ClientID
        JOIN offer o ON c.Tier = o.Tier
        WHERE u.UserID = %s
        '''
        cur.execute(sql1, (session['UserID'],))
        data = cur.fetchall()

        Logger.log("User is paying flight")
        close_db(cur,conn) 
        return render_template('payFlight.html',value = data)
    Logger.log("Session is over, go to Sign In")
    return render_template('signIn.html')

@app.route('/Finish_Booking', methods=['POST'])
def finish_booking():
    if request.method == 'POST':
        conn = get_conn()

        cur = conn.cursor()
        
        flight_code = request.form.get('FlightCode')
        passengers = request.form.get('passengers')
        old_purchase_date = request.form.get('PurchaseDate')
        purchase_date = datetime.strptime(old_purchase_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        
        baggage = request.form.get('extraBaggage')
        distance = request.form.get('Distance')
        selected_class = request.form.get('selectedClass')
        finalPrice = request.form.get('finalPrice')
        userID = session['UserID']
        
        departure = request.form.get('Departure')
        departure_time = request.form.get('DepartureTime')
        destination = request.form.get('Destination')
        arrival_time = request.form.get('arrivalTime')
        
        ticket_ids = {} 
        for i in range(0, int(passengers)):
            ticket_id = request.form.get('TicketID' + str(i))
            ticket_ids['TicketID' + str(i)] = ticket_id  # Add the ticket_id to the dictionary

        for i in range(0, int(passengers)):
            cur.execute(SQL.sql1_finishbooking, (ticket_ids['TicketID' + str(i)], userID, purchase_date, flight_code, selected_class, int(baggage), finalPrice, "Operating", 0))
        
        cur.execute(SQL.sql2_finishbooking, (selected_class, passengers, selected_class, passengers, selected_class, passengers, flight_code))

        cur.execute(SQL.sql3_finishbooking, (selected_class, distance, passengers, selected_class, distance, passengers, selected_class, distance, passengers, userID))
         
        cur.execute(SQL.sql4_finishbooking, (userID,))
        user_data = cur.fetchone()

        first_name = user_data[0]
        last_name = user_data[1]

        # Generate a unique name for the text file using the passenger's name
        passenger_name = f"{first_name} {last_name}"
        file_name = f"Buchungsbestätigung von {passenger_name}.txt"

        email = []
         # Create and save the booking confirmation email content
        for i in range(int(passengers)):
            ticketid = ticket_ids['TicketID' + str(i)]
            email_content = """
            Subject: Booking Confirmation

            Dear {passenger_name},

            Thank you for booking your flight with BananaAirlines. Below are the details of your booking:
        
            Ticket ID : {ticketid}
            Buy Date : {purchase_date}
            Flight Code: {flight_code}
            Departure: {departure}
            Departure Time: {departure_time}
            Destination: {destination}
            Arrival Time: {arrival_time}
            Class: {selected_class}
            Total Price: {finalPrice}

            We look forward to welcoming you on board.

            Safe travels!

            Sincerely,
            BananaAirlines Team
            
            ////////////////////////////////////////////////////////////////////////
            """.format(
                ticketid = ticketid,
                purchase_date = purchase_date,
                departure = departure,
                arrival_time = arrival_time,
                passenger_name=passenger_name,
                flight_code=flight_code,
                departure_time=departure_time,
                destination=destination,
                selected_class=selected_class,
                finalPrice=finalPrice
            )
            email.append(email_content)

        for e in email:
            with open(file_name, "a") as file:
                file.write(e)
         
        Logger.log("Booking is finished! Go back to Homepage")
        close_db(cur, conn)
        return render_template('approved.html')
    close_db(cur, conn)
    return render_template('approved.html')

@app.route('/myFlights')
def myFlights():
    if 'loggedin' in session:
        conn = get_conn()

        cur = conn.cursor()
    
        cur.execute(SQL.sql1_myFlights, (session['UserID'],))
        data = cur.fetchall()
        
        Logger.log("User is seeing all current flights")
        close_db(cur,conn) 
        return render_template('myFlights.html',flights = data)
    Logger.log("Session is over, go back to Sign In")
    return render_template('signIn.html')

@app.route('/Cancel_Client', methods=['GET', 'POST'])
def Cancel_Client():
    if request.method == 'POST':
        conn = get_conn()

        cur = conn.cursor()
        
        # Get the cancellation reason from the form data
        cancellation_reason = request.form.get('cancle-reason-input')
        ticket_id = request.form.get('TicketID')
        
        cur.execute(SQL.sql_cancel_client, (cancellation_reason, ticket_id,))
        
        cur.execute(SQL.sql1_myFlights, (session['UserID'],))
        data = cur.fetchall()
        
        Logger.log(f"User has requested cancellation for ticket {ticket_id}")
        close_db(cur,conn) 
        return render_template('myFlights.html',flights = data)
        
@app.route('/checkIn')
def checkin():
    if 'loggedin' in session:
        Logger.log("User go to Check In Page")
        return render_template('checkIn.html')
    Logger.log("Session is over, go back to Sign In")
    return render_template('signIn.html')

@app.route('/validate_names', methods=['POST'])
def validate_names():
    conn = get_conn()

    cur = conn.cursor()
    bookingID = request.form['bookingID']
    
    cur.execute(SQL.sql_validate, (bookingID,))
    result = cur.fetchone()
    
    close_db(cur,conn)
    return jsonify({'firstName': result[0], 'lastName': result[1], 'alreadyCheckedIn': result[2]})

@app.route('/update_checkin', methods=['POST'])
def update_checkin():
    conn = get_conn()

    cur = conn.cursor()
    bookingID = request.form['bookingID']
    
    cur.execute(SQL.sql_update_checkin, (bookingID,))
    
    close_db(cur,conn)
    return jsonify({'success': True})

@app.route('/finish_checkin')
def finish_checkin():
    Logger.log("Checkin is finished!")
    return render_template('approved.html')

@app.route('/employee_insert', methods=['POST'])
def insert():
    conn = get_conn()

    cur = conn.cursor()
    if request.method == 'POST':
        
        data = request.get_json()
        # Insert a new record
        cur.execute(SQL.sql1_insert,
        (data['flightCodeInput'], data['aircraftInput'], data['capacityInput'], data['CapacityEconomy'], data['CapacityBusiness'], data['CapacityFirstClass']))
        
        cur.execute(SQL.sql2_insert, 
        (data['flightCodeInput'], data['sourceAirportInput'], data['destinationAirportInput'], data['departureTimeInput'], data['arrivalTimeInput'], data['distanceInput']))
        
        cur.execute(SQL.sql3_insert,
        (data['flightCodeInput'], data['priceEconomy'], data['priceBusiness'], data['priceFirst']))
        
        Logger.log(f"Flight {data['flightCodeInput']} added succesfully")
        close_db(cur,conn)
        return '', 204
    # Fetch all aircrafts, offers from the database
    cur.execute(SQL.sql_flights)
    aircrafts = cur.fetchall()
    
    cur.execute(SQL.sql_offer)
    offers = cur.fetchall()
    
    cur.execute(SQL.sql_customer_em)
    customers = cur.fetchall()
    
    close_db(cur, conn)
    return render_template('employee_homepage.html', offers=offers, aircrafts=aircrafts, customers=customers)

@app.route('/employee_update', methods=['POST'])
def update():
    conn = get_conn()

    cur = conn.cursor()
    if request.method == 'POST':
        data = request.get_json()
        
        aircraftname = data['aircraftname']
        new_aircraftId = data['new_aircraftId']
        old_aircraftId = data['old_aircraftId']
        capacity = int(data['capacity'])
        capacity_economy = int(data['capacity_economy'])
        capacity_business = int(data['capacity_business'])
        capacity_firstclass = int(data['capacity_firstclass'])
        departure = data['departure']
        departuretime = data['departuretime']
        destination = data['destination']
        arrivaltime = data['arrivaltime']
        distance = int(data['distance'])
        price_economy = int(data['price_economy'])
        price_business = int(data['price_business'])
        price_firstclass = int(data['price_firstclass'])
        
        cur.execute(SQL.sql1_update_flight_em,
        (new_aircraftId, price_economy, price_business, price_firstclass, old_aircraftId))
        
        cur.execute(SQL.sql2_update_flight_em,
        (new_aircraftId, departure, destination, departuretime, arrivaltime, distance, old_aircraftId))
        
        cur.execute(SQL.sql3_update_flight_em,
        (new_aircraftId, aircraftname,capacity,capacity_economy,capacity_business,capacity_firstclass, old_aircraftId))
        close_db(cur,conn)
        Logger.log(f"Employee edited flight {old_aircraftId}")
        return '', 204 
    
    # Fetch all aircrafts, offers from the database
    cur.execute(SQL.sql_flights)
    aircrafts = cur.fetchall()
    
    cur.execute(SQL.sql_offer)
    offers = cur.fetchall()

    cur.execute(SQL.sql_customer_em)
    customers = cur.fetchall()
    
    close_db(cur, conn)
    return render_template('employee_homepage.html', offers=offers, aircrafts=aircrafts, customers=customers)

@app.route('/employee_delete', methods=['POST'])
def employee_delete():
    conn = get_conn()

    cur = conn.cursor()
    if request.method == 'POST':
        data = request.get_json()
        aircraftId = data['aircraftId']
        
        cur.execute(SQL.sql1_delete_em, (aircraftId,))
        cur.execute(SQL.sql2_delete_em, (aircraftId,))
        cur.execute(SQL.sql3_delete_em, (aircraftId,))
        conn.commit()
        
        Logger.log("successfully deleted aircraft")
        conn.close()
        return '', 204 
    
    # Fetch all aircrafts, offers from the database
    cur.execute(SQL.sql_flights)
    aircrafts = cur.fetchall()
    
    cur.execute(SQL.sql_offer)
    offers = cur.fetchall()

    cur.execute(SQL.sql_customer_em)
    customers = cur.fetchall()
    
    close_db(cur, conn)
    return render_template('employee_homepage.html', offers=offers, aircrafts=aircrafts, customers=customers)
 
@app.route('/update_offer', methods=['POST'])
def update_offer():
    conn = get_conn()

    cur = conn.cursor()
    if request.method == 'POST':
        data = request.get_json()
        new_offer = data['newOffer']
        tier = data['tier']
        
        cur.execute(SQL.sql_update_offer_em, (new_offer, tier))
        
        Logger.log(f"successfully updated offer from {tier}")
        close_db(cur,conn)
        return '', 204 
    
    # Fetch all aircrafts, offers from the database
    cur.execute(SQL.sql_flights)
    aircrafts = cur.fetchall()
    
    cur.execute(SQL.sql_offer)
    offers = cur.fetchall()
    
    cur.execute(SQL.sql_customer_em)
    customers = cur.fetchall()
    
    close_db(cur, conn)
    return render_template('employee_homepage.html', offers=offers, aircrafts=aircrafts, customers=customers)

@app.route('/cancellationrequest', methods=['POST'])
def cancellation():
    conn = get_conn()

    cur = conn.cursor()

    if request.method == 'POST':
        data = request.get_json()
        response = data['response']
        ticket = data['ticket']
        selected_class = data['class']
        distance = data['distance']
        
        cur.execute(SQL.sql_getflight_cancel, (ticket,))
        result = cur.fetchall()
        if result:
            flight_code = result[0][0]  # Get the first FlightCode from the result

        
        if response == 1:
            cur.execute(SQL.sql_cancel_delete, (ticket,))
            cur.execute(SQL.sql_delete_updatemiles, (selected_class, distance, selected_class, distance, selected_class, distance))
            cur.execute(SQL.sql_update_capacity, (selected_class, selected_class, selected_class, flight_code))
        else:
            cur.execute(SQL.sql_delete_update_decline, (ticket,))
        
        print("successfully handle cancellation request")
        cur.execute(SQL.sql_flights)
        aircrafts = cur.fetchall()
        
        cur.execute(SQL.sql_offer)
        offers = cur.fetchall()

        cur.execute(SQL.sql_customer_em)
        customers = cur.fetchall()
        
        Logger.log(f"Ticket {ticket} is deleted succesfully")
        close_db(cur, conn)
        return render_template('employee_homepage.html', offers=offers, aircrafts=aircrafts, customers=customers)


if __name__ == '__main__':
    app.run(debug=True)