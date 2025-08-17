#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from src.converter import LandUnitsConverter

app = Flask(__name__, template_folder='templates', static_folder='static')
DB_PATH = os.path.join(os.path.dirname(__file__), '..','database','land_units.db')
converter = LandUnitsConverter(DB_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['GET','POST'])
def convert_view():
    if request.method=='POST':
        value = float(request.form['value'])
        res = converter.convert(value, request.form['from_unit'], request.form['to_unit'], request.form.get('region') or None)
        return render_template('conversion.html', result=res)
    units = converter.list_units()
    return render_template('convert.html', units=units)

@app.route('/api/convert', methods=['POST'])
def api_convert():
    data = request.get_json(force=True)
    res = converter.convert(float(data['value']), data['from_unit'], data['to_unit'], data.get('region'))
    return jsonify(res)

if __name__=='__main__':
    app.run(port=5000, debug=True)
