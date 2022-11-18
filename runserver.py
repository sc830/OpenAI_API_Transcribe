#!/usr/bin/env python -B
import sys 
sys.dont_write_bytecode = True
from intro_to_flask import app

app.run(debug=True)
