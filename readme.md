# Comandos

### Crea el entorno virtual
python -m venv env

### Activa el entorno virtual
.\env\Scripts\activate

### Ejecuta las instalaciones de los requerimientos(no agregar ya que está en los documentos)
pip install -r requirements.txt

### apis
pip install django
pip install transbank-sdk
pip install djangorestframework


## FullCalendar
npm install fullcalendar
npm install moment jquery

### Aplica las migraciones
python manage.py migrate

### Crea un usuario
python manage.py createsuperuser

### Ejecuta la APP
python manage.py runserver
