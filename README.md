### BananaAirlines – University Project

This project is an airline booking website originally built on MariaDB, now migrated to PostgreSQL for cloud hosting with [Supabase](https://supabase.com/) and [Render](https://render.com/).

**Live Demo:** [https://bananaairlines.onrender.com/](https://bananaairlines.onrender.com/)     

---

#### 🗄️ Data Model

The data model is designed to support a full-featured airline booking system. Key tables include:

- **aircraft**: Stores aircraft details and capacities for each class.
- **cities**: Contains all supported cities and their airport codes.
- **offer**: Defines tier-based offers (Bronze, Silver, Gold).
- **user**: Handles authentication and user types (client or employee).
- **employee**: Stores employee information, linked to the user table.
- **client**: Stores client information, linked to the user table and their tier.
- **flight**: Contains all flight schedules, source/destination, and times.
- **class**: Stores pricing for each flight and class.
- **ticket**: Represents bookings, including status, check-in, and payment.

All relationships are enforced with foreign keys. The schema is defined in [`sql/bananaairlines.sql`](sql/bananaairlines.sql) and is compatible with PostgreSQL/Supabase.

![alt text](https://github.com/goviet2002/BananaAirlines/tree/main/sql/dataModel.png)

---

#### 🐍 Python Automation

- Python scripts (see [`sql/create_flight.py`](sql/create_flight.py)) are used to generate large numbers of flights, aircraft, and classes with realistic random data.
- These scripts output SQL files (e.g., `flights.sql`, `aircrafts.sql`, `classes.sql`) that can be loaded into the PostgreSQL database.

---

#### 💻 Running Locally
- You can still run the project locally with PostgreSQL or MariaDB (in old commmits)
- To use PostgreSQL: load the schema into your database (e.g., Supabase), and update the connection settings in `app.py` to match your environment.

#### 📝 Features

- **User Registration & Login:** With email and username uniqueness checks.
- **Flight Booking:** Dynamic selection of available destinations and dates, with tier-based discounts.
- **Booking Confirmation:** Generates a confirmation file for each booking.
- **Flight Management:** Employees can add, edit, or remove flights and manage tier offers.
- **Cancellation & Check-in:** Users can cancel bookings or check in online.
- **Tier System:** Bronze, Silver, and Gold tiers with different offers and discounts.

![alt text](https://github.com/goviet2002/BananaAirlines/blob/e406b9695f86b95e452532eb1d4ba29d0dd494f9/static/images/overview/main.png)
![alt text](https://github.com/goviet2002/BananaAirlines/blob/05a2c72bef380e427b55377787d117a12c86b3d8/static/images/overview/tier.png)

If you don't have an account, you can create it by clicking the Sign Up button and filling in your personal information. You cannot create a new account if the registered Email has already existed.

![alt text](https://github.com/goviet2002/BananaAirlines/blob/37acba087a9aa2e22d92e92d46289ddfb122f938/static/images/overview/login.png)
![alt text](https://github.com/goviet2002/BananaAirlines/blob/37acba087a9aa2e22d92e92d46289ddfb122f938/static/images/overview/signup.png)

You can then book flights! By choosing the departure only the available destinations will appear and you can also only choose the available date. Discounts can also be applied based on your current tier. The flight can only be booked if the remaining seats are larger than the number of tickets you want to book.

![alt text](https://github.com/goviet2002/BananaAirlines/blob/37acba087a9aa2e22d92e92d46289ddfb122f938/static/images/overview/chooseflight.png)
![alt text](https://github.com/goviet2002/BananaAirlines/blob/37acba087a9aa2e22d92e92d46289ddfb122f938/static/images/overview/availableflight.png)
![alt text](https://github.com/goviet2002/BananaAirlines/blob/37acba087a9aa2e22d92e92d46289ddfb122f938/static/images/overview/checkdetailflight.png)

![alt text](https://github.com/goviet2002/BananaAirlines/blob/37acba087a9aa2e22d92e92d46289ddfb122f938/static/images/overview/myaccount.png)
![alt text](https://github.com/goviet2002/BananaAirlines/blob/37acba087a9aa2e22d92e92d46289ddfb122f938/static/images/overview/myflight.png)

![alt text](https://github.com/goviet2002/BananaAirlines/blob/37acba087a9aa2e22d92e92d46289ddfb122f938/static/images/overview/checkin.png)

After booking all the flights will be displayed in the account details or my flights and you will receive a booking confirmation through an external file. You can cancel the flight by giving the reason or you can do check-in.

![alt text](https://github.com/goviet2002/BananaAirlines/blob/37acba087a9aa2e22d92e92d46289ddfb122f938/static/images/overview/cf.png)
![alt text](https://github.com/goviet2002/BananaAirlines/blob/37acba087a9aa2e22d92e92d46289ddfb122f938/static/images/overview/checkedin.png)

#### 👨‍💻 Employee Access

- Employees can log in with the default account (`admin_boss` / `123`) to manage flights and customer requests.

![alt text](https://github.com/goviet2002/BananaAirlines/blob/37acba087a9aa2e22d92e92d46289ddfb122f938/static/images/overview/employee1.png)
![alt text](https://github.com/goviet2002/BananaAirlines/blob/37acba087a9aa2e22d92e92d46289ddfb122f938/static/images/overview/employee2.png)
