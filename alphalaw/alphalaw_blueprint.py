# -*- coding: utf-8 -*-
"""
    alphalaw.blueprint
    ~~~~~~~~~~~~~~~~~~
    alphalaw 어플리케이션에 적용할 blueprint 모듈.
"""


from flask import Blueprint
from alphalaw.alphalaw_logger import Log

alphalaw = Blueprint('alphalaw', __name__,
                     template_folder='../templates', static_folder='../static')

Log.info('static folder : %s' % alphalaw.static_folder)
Log.info('template folder : %s' % alphalaw.template_folder)