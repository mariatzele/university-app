# University Management App
TODO

### How do I get set up? 

## Set up database connection settings
Copy the `.example.env` to a file called `.env` with the correct values to connect to the database

## Initialise / Migrate your database
There are 2 files in the migrations folder. You need to execute them in order.
This will set up your database and load dummy data into it.
You can do this using the `mysql` tool by opening a connection to the database
and from the shell running:

*If you want to create a new database*
```
>> create database <YOUR_DATABASE_NAME>
>> use database <YOUR_DATABASE_NAME>
```
of if you already have a database you want to use
```
>> use <YOUR_DATABASE_NAME>
```

It is recommended that you create a new database to avoid
affecting any other data you may already have in your current database.

With your database in use (using the `database use` command) you can then run:
```
>> source migrations/1_init.sql;
>> source migrations/2_dummy_data.sql;
```
This assumes that you opened the terminal inside the root of this project folder.

## Set up the python environment
This assumes you already have `venv`. It usually comes with python 
Using the terminal, on MacOS/Linux systems, from inside this project directory run:
```
source venv/bin/activate
```

If using windows, you will need to run (Command Prompt):
```
.venv\Scripts\activate
```

If using PyCharm it should automatically detect the `.venv` directory and will show a banner which you can click
to use the `.venv` configuration.

Install the dependencies:
```
pip install -r requirements.txt
```

# Running the code
To start the application you can run:
```
python src/main.py
```

# Running the tests
To run all the test files under the `tests/` directory you can run:
```
python -m unittest discover -s tests -p "*_test.py"
```