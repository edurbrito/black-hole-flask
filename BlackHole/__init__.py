from flask import Flask
import config as cfg

app = Flask(__name__)
app.config.from_object(cfg.Config)

import BlackHole.views
