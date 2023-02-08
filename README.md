# Best practices python
The below repository is present on Knoldus Public Github and contains the multi-module python project with best practices and standards implemented.


### Clone
```
git clone <repo_name>
```

### 1.Create a new virtual environment by choosing a Python interpreter and making a ./venv directory to hold it(you can also use  anaconda/any other methods available):
```bash
python3 -m venv ./venv
```
### 2.Activate the virtual environment:
```bash
source ./venv/bin/activate
```

### 3.Next,Copy all the files to the virtual envoirment directory you just created:


### Record the dependencies for the project

### Python requirments
Python 3.8

### First, update the pip library
```
$python -m pip install --upgrade pip
```
### install requirments
```
pip install -r requirements.txt 
```



#### Usage/Run

### Remove the .gitkeep file present inside Rasa_app/data/Input_data & Rasa_app/data/Entity_extracted_data (If it is present)

###  on local
```
$python3 app.py
```

### Check the app through Postman(the app will run on localhost:8000)

GET: Check whether the server is running or not
```
http://localhost:8000/ping

```

POST: Input a .pdf as a body through postman
```
http://localhost:8000/invocations

```

### Logfile is stored in logs directory according in (yyyy-mm-dd) format


### on Docker

### docker build 
```
docker build -t <image_name> .

```
### docker run
```
docker run -t <image_name> .
```

### Check Code Quality

```
$pre-commit run --all-files

```


