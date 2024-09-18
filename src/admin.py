import os
from flask_admin import Admin  # Importa la clase Admin de flask_admin
from flask_admin.contrib.sqla import ModelView  # Importa la clase ModelView para manejar vistas de modelos
from models import db, User, Character, Planet, Vehicle, Favorite  # Importa los modelos de la base de datos

# Función para configurar el administrador
def setup_admin(app):
    # Establece una clave secreta para la aplicación
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    # Configura un tema para el panel de administración
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
  
    # Crea una instancia de la clase Admin para manejar el panel
    admin = Admin(app, name='StarWars Blog Admin', template_mode='bootstrap3')
    
    # Añade vistas para cada modelo en el panel de administración
    admin.add_view(ModelView(User, db.session))        # Vista para el modelo User
    admin.add_view(ModelView(Character, db.session))   # Vista para el modelo Character
    admin.add_view(ModelView(Planet, db.session))      # Vista para el modelo Planet
    admin.add_view(ModelView(Vehicle, db.session))     # Vista para el modelo Vehicle
    admin.add_view(ModelView(Favorite, db.session))    # Vista para el modelo Favorite
