from ..requests import get_quotes
from flask import render_template
from . import main

@main.route('/')
def index():
    quotes = get_quotes()
    
    return render_template('index.html', quotes=quotes)