import sqlite3

import click
from flask import current_app, g
from flask.cli import cli, with_appcontext

def get_db():
    """create connection to the database, store the connection in g, to be reused"""

    if 'db' not in g:
        # create a Connection object that represents the database
        g.db = sqlite3.connect(
            # current_app is the proxy to the app object as it is created in a factory
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # return row's as dictionaries
        g.db.row_factory = sqlite3.Row
    
    # return the connection object
    return g.db

# https://stackoverflow.com/questions/57455431/flask-official-tutorial-what-is-e-in-close-dbe-none
# e is an error object
def close_db(e=None):
    """close the db connection if it is set"""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """ initiate the database"""

    # get database connection object
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        # create cursor and execute script to initiate database
        db.executescript(f.read().decode('utf8'))

# use the click command line to initiate the database, can be called using: flask init-db
@click.command('init-db')
@with_appcontext
def init_db_commmand():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialzed the database.')

def init_app(app):
    """ registers the close_db and init_db_command functions with the app, given the app is created with a factory function and the app instance isn't available """

    # Call the close_db connection function when cleaning up after a request
    app.teardown_appcontext(close_db)

    # add init_db_command function to the flask command
    app.cli.add_command(init_db_commmand)