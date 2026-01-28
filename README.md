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

### 3. migrate
```bash
python3 manage.py migrate
```

### 4. create admin
```bash
python3 manage.py createsuperuser
```

### 5. run server
```bash
python3 manage.py runserver
```