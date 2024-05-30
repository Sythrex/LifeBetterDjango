# Comandos

### Crea el entorno virtual
python -m venv env

### Activa el entorno virtual
.\env\Scripts\activate

### Ejecuta las instalaciones de los requerimientos
pip install -r requirements.txt

### Aplica las migraciones
python manage.py migrate

### Crea un usuario
python manage.py createsuperuser

### Ejecuta la APP
python manage.py runserver