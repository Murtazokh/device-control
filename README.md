# device-control

## quick setup

### 1. setup venv
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. install dependencies
```bash
pip install -r requirements.txt
```

### 3. setup .env file
```bash
cp .env.example .env

# generate a secret key and add it to .env
```

### 4. migrate
```bash
python3 manage.py migrate
```

### 5. create admin
```bash
python3 manage.py createsuperuser
```

### 6. run server
```bash
python3 manage.py runserver
```