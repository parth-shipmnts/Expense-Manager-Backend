﻿# initialize all other modules and start the app
# use 'python startup.py' to start the app

import wtforms_json
from ExpenseManager import app, models
from ExpenseManager.Views import *
from ExpenseManager.seed_database import seed_postgres
from flask_cors import CORS
import os
#wtform json config
wtforms_json.init()

#seed database
seed_postgres()

#allowing cross origing requests
CORS(app)

if __name__ == '__main__':
    app.run('0.0.0.0', int(os.environ.get('PORT')), debug=True)
