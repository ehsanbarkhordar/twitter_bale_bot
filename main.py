from controller.twitter_bot import updater
from db.base import create_tables

if __name__ == '__main__':
    create_tables()
    updater.run()
