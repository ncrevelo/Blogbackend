import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Añadir el directorio raíz del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print("PYTHONPATH:", sys.path)  # Mensaje de depuración

# Esto cargará las variables de entorno desde .env
load_dotenv()

# Verificar si DATABASE_URL está cargada
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

print(f'DATABASE_URL: {database_url}')  # Mensaje de depuración

# Configurar Alembic para usar la URL de la base de datos desde las variables de entorno
config = context.config
config.set_main_option('sqlalchemy.url', database_url)

# Interpretar el archivo de configuración de logging config, si existe.
fileConfig(config.config_file_name)

# Añadir aquí el target metadata para 'autogenerate' support
try:
    from app.models import Base  # Asegúrate de que esta importación sea correcta y que 'app' esté en tu PYTHONPATH
    print("Modelos importados correctamente")  # Mensaje de depuración
except ImportError as e:
    print("Error al importar modelos:", e)  # Mensaje de depuración
    raise e

target_metadata = Base.metadata

# Función para ejecutar migraciones en modo 'offline'
def run_migrations_offline():
    """Ejecutar migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

# Función para ejecutar migraciones en modo 'online'
def run_migrations_online():
    """Ejecutar migraciones en modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# Determina si Alembic debe correr en modo 'offline' o 'online'
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
