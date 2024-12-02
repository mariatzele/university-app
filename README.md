# University Management App
TODO

### How do I get set up? 
Copy the `.example.env` to a file called `.env` with the correct values to connect to the database

Set up venv environment
On MacOS/Linux you can run:
```
python3 -m venv venv
```

On Windows you can run:
```
python -m venv venv
```

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