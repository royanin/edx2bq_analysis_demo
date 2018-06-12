from flask import render_template, flash, redirect, url_for, request, g, json, jsonify, send_from_directory
from flask_app import flask_app

@flask_app.route('/')
def index():
    return render_template("index.html")
