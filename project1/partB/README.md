# PartA

This is partA for the programming excercise 1 of the course PLH417. It implements a genetic algorithm to solve the WHPP problem.


### Prequisites

* Python version 3.6+.

#### Creating a virtual environment for the project (not required!)

##### Windows

Generate virtual environment:
```
python -v venv venv
```

Activating environment:
```
call venv\Scripts\activate.bat
```

##### Linux

Generate virtual environment:
```
python3 -v venv venv
```

Activating environment:
```
source venv\Scripts\activate
```

### Installing packages and running

Install packages:
```
pip install -r requirements.txt
```
_Note_ you might need to use pip3 command on some linux distributions.

Run base script:
```
python genetic_algorithm.py
```
Use `--help` to see options

Optionaly regenerate report results:
```
python generate_results.py
```