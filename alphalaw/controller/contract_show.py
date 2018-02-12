# -*- coding: utf-8 -*-
"""
    alphalaw.controller.contract_show
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    업로드된 계약서를 보여준다.
"""


import os
from flask import request, current_app, send_from_directory \
                , render_template, session, url_for
from sqlalchemy import or_

from alphalaw.database import dao
from alphalaw.model.contract import Contract
from alphalaw.controller.login import login_required
from alphalaw.alphalaw_blueprint import alphalaw
from alphalaw.alphalaw_logger import Log


def sizeof_fmt(num):
    """파일 사이즈를 일기 편한포맷으로 변경해주는 함수"""
    
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def get_contract_info(contract_id):
    """업로드된 계약서 관련 정보(다운로드 폴더, 파일명, 전체 파일 경로 등)을 얻는다.
       내부 함수인 __get_download_info()에 사용된다.
    """
    
    contract = dao.query(Contract).filter_by(id=contract_id).first()
    download_folder = \
        os.path.join(current_app.root_path, 
                     current_app.config['UPLOAD_FOLDER'])
    download_filepath = os.path.join(download_folder, 
                                     contract.filename)
    
    return (download_folder, contract.filename, 
            download_filepath, contract.comment)


def __get_download_info(contract_id, prefix_filename=''):
    contract_info = get_contract_info(contract_id)
    
    download_folder = contract_info[0]
    original_filename = contract_info[1]
    download_filename = prefix_filename + original_filename

    return send_from_directory(download_folder, 
                               download_filename, 
                               as_attachment=True, 
                               mimetype='text/plain')
    
    
@alphalaw.route('/contract/download/<contract_id>')
@login_required
def download_contract(contract_id):
    return __get_download_info(contract_id)



@alphalaw.route('/contract/', defaults={'page': 1})
@alphalaw.route('/contract/page/<int:page>')
@login_required
def show_all(page=1):    
    
    user_id = session['user_info'].id
    per_page = current_app.config['PER_PAGE']
    
    contract_count = dao.query(Contract).count()
    pagination = Pagination(page, per_page, contract_count)
    
    if page != 1:
        offset = per_page * (page - 1)
    else:
        offset = 0
    
    contract_pages = dao.query(Contract). \
                        filter_by(user_id=user_id). \
                        order_by(Contract.upload_date.desc()). \
                        limit(per_page). \
                        offset(offset). \
                        all()
    
    return render_template('list.html',
        pagination=pagination,
        contracts=contract_pages,
        sizeof_fmt=sizeof_fmt) 


@alphalaw.route('/contract/search', methods=['POST'])
@login_required
def search_contract():    
    search_word = request.form['search_word'];
    
    if (search_word == ''):
        return show_all();
    
    user_id = session['user_info'].id
    
    contracts=dao.query(Contract).filter_by(user_id=user_id). \
               filter(or_(Contract.filename_orig.like("%" + search_word + "%"), 
                          Contract.upload_date.like("%" + search_word + "%"))). \
               order_by(Contract.upload_date.desc()).all()    
       
    return render_template('list.html', contracts=contracts, sizeof_fmt=sizeof_fmt)


from math import ceil


class Pagination(object):
    
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num