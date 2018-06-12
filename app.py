from dash import Dash
import os
import flask
from flask_app import flask_app

app = Dash('app', server=flask_app, url_base_pathname='/demo')
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = False


app.css.append_css({
    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
})

