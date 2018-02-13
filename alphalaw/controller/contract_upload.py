# -*- coding: utf-8 -*-
"""
    alphalaw.controller.contract_upload
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    파일 업로드 모듈.
    계약서를 서버의 upload 디렉토리에 저장함.
"""


import os
from flask import request, redirect, url_for, current_app, render_template, \
                    session
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
from PIL import Image
from wtforms import Form, FileField, TextField, TextAreaField, HiddenField, \
                    validators

from alphalaw.database import dao
from alphalaw.model.contract import Contract
from alphalaw.controller.login import login_required
from alphalaw.alphalaw_logger import Log
from alphalaw.alphalaw_blueprint import alphalaw

import requests
import json
import tika
tika.TikaClientOnly = True
from tika import parser


ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'docx'])


def __allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@alphalaw.route('/contract/upload')
@login_required
def upload_contract_form():
    """ 계약서파일을 업로드 하기 위해 업로드폼 화면으로 전환시켜주는 함수 """
    
    form = ContractUploadForm(request.form)
    
    return render_template('upload.html', form=form)


@alphalaw.route('/contract/upload', methods=['POST'])
@login_required
def upload_contract():
    """ Form으로 파일과 변수들을 DB에 저장하는 함수. """

    form = ContractUploadForm(request.form)
        
    # HTTP POST로 요청이 오면 사용자 정보를 등록
    if form.validate():  
        #: Session에 저장된 사용자 정보를 셋팅
        user_id = session['user_info'].id
        username = session['user_info'].username     
        
        #: Form으로 넘어온 변수들의 값을 셋팅함
        upload_date = datetime.today()
        
        #: 업로드되는 파일정보 값들을 셋팅한다.
        upload_contract = request.files['contract']
        filename = None
        filesize = 0
        filename_orig = upload_contract.filename
    
        try:
            #: 파일 확장자 검사
            if upload_contract and __allowed_file(upload_contract.filename):
                
                ext = (upload_contract.filename).rsplit('.', 1)[1]
    
                #: 업로드 폴더 위치는 얻는다.
                upload_folder = \
                    os.path.join(current_app.root_path, 
                                 current_app.config['UPLOAD_FOLDER'])
                #: 유일하고 안전한 파일명을 얻는다.   
                filename = \
                    secure_filename(username + 
                                    '_' + 
                                    str(uuid.uuid4()) +
                                    "." + 
                                    ext)
                
                upload_contract.save(os.path.join(upload_folder, 
                                               filename))
                
                filesize = \
                    os.stat(upload_folder + filename).st_size
                
            else:
                raise Exception("File upload error : illegal file.")
    
        except Exception as e:
            Log.error(str(e))
            raise e
        
        try :
            tika_url = 'http://192.168.0.199:9998/tika'
            es_url = 'http://192.168.0.200:9201/test_idx/fulltext/' + filename
            es_request_header = {'Content-Type': 'application/json; charset=utf-8'}
            
            tika_parsed = parser.from_file(os.path.join(upload_folder, filename), tika_url)
            es_data = {
                'title': filename,
                'text': tika_parsed['content']
                }
            
            r = requests.post(url=es_url, data=json.dumps(es_data), headers=es_request_header)
            Log.debug(r)
            
        except Exception as e:
            Log.error(e)
            raise e
    
        try :
            #: 계약서에 대한 정보 DB에 저장
            contract = Contract(user_id, 
                          filename_orig, 
                          filename, 
                          filesize, 
                          upload_date
                          )
            dao.add(contract)
            dao.commit()
    
        except Exception as e:
            dao.rollback()
            Log.error("Upload DB error : " + str(e))
            raise e
    
        return redirect(url_for('.show_all'))
    else:
        return render_template('upload.html', form=form)


@alphalaw.route('/contract/update/<contract_id>', methods=['POST'])
@login_required
def update_contract(contract_id):
    """ 계약서 업로드 화면에서 사용자가 수정한 내용을 DB에 업데이트 한다. """

    form = ContractUploadForm(request.form)

    if form.validate(): 
        
        try :
            #: 변경전 원래의 contract 테이블 값을 읽어 온다.
            contract = dao.query(Contract).filter_by(id=contract_id).first()
            dao.commit()
    
        except Exception as e:
            dao.rollback()
            Log.error("Update DB error : " + str(e))
            raise e
    
        return redirect(url_for('.show_all'))
    else:
        return render_template('upload.html', contract=contract, form=form)



@alphalaw.route('/contract/update/<contract_id>')
@login_required
def update_contract_form(contract_id):
    """ 업로드폼에서 입력한 값들을 수정하기 위해 DB값을 읽어와 업로드폼 화면으로 전달한다. """
    
    contract = dao.query(Contract).filter_by(id=contract_id).first()
    form = ContractUploadForm(request.form, contract)
        
    return render_template('upload.html', contract=contract, form=form)



@alphalaw.route('/contract/remove/<contract_id>')
@login_required
def remove(contract_id):
    """ DB에서 해당 데이터를 삭제하고 관련된 파일을 함께 삭제한다."""

    user_id = session['user_info'].id
    
    try:
        contract = dao.query(Contract).filter_by(id=str(contract_id)).first()
        
        dao.delete(contract)
        dao.commit()

        upload_folder = os.path.join(current_app.root_path, 
                                     current_app.config['UPLOAD_FOLDER'])
        os.remove(upload_folder + str(contract.filename))

    except Exception as e:
        dao.rollback()
        Log.error("Contract remove error => " + contract_id + ":" + user_id + \
                  ", " + str(e))
        raise e
    
    return redirect(url_for('.show_all'))


class ContractUploadForm(Form):
    """계약서 등록 화면에서 계약서 파일을 검증함"""
    
    contract = FileField('Contract')