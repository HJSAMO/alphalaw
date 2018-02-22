# -*- coding: utf-8 -*-
"""
    alphalaw.controller.contract_viewer
    contract = dao.query(Contract).filter_by(id=contract_id).first()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


from datetime import datetime
import os
import uuid

from PIL import Image
from flask import request, redirect, url_for, current_app, render_template, \
                    session
from werkzeug.utils import secure_filename
from wtforms import Form, FileField, TextField, TextAreaField, HiddenField, \
                    validators

from alphalaw.alphalaw_blueprint import alphalaw
from alphalaw.alphalaw_logger import Log
from alphalaw.controller.login import login_required
from alphalaw.database import dao
from alphalaw.model.contract import Contract
import requests
import json

@alphalaw.route('/contract/viewer/<contract_id>')
@login_required
def contract_viewer(contract_id):
    contract = dao.query(Contract).filter_by(id=contract_id).first()
    
    es_url = 'http://192.168.0.200:9201/test_idx/fulltext/' + contract.filename
    es_request_header = {'Content-Type': 'application/json; charset=utf-8'}
    
    r = requests.get(url=es_url, headers=es_request_header)
    es_contract = r.json().get("_source")
      
    return render_template('contractviewer.html', contract=es_contract)
