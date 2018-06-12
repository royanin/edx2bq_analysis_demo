from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
from flask_app import flask_app

@flask_app.route('/')
def index():
    session['check'] = 'Nothing really'
    return render_template("index.html")
