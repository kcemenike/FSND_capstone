from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from src.api import application
from src.database.models import db

migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
