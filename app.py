import os
import io
import copy
import json
import requests
import urllib.parse
from enum import Enum
import uvicorn
from fastapi import FastAPI, Query, Form, File, UploadFile
import logging
import datetime
from pydantic import BaseModel
from typing import Optional
import models

app = FastAPI()

logging.basicConfig(
    handlers=[
        logging.FileHandler(filename='log.log', encoding='utf-8', mode='a+')
    ],
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y%m%d.%H%M%S'
)

pcloud_url = "https://api.pcloud.com"

def clean_path(path):
    if (path is not None and path[:1] != '/'):
        return '/' + path
    else:
        return path

@app.post('/login')
async def login_controller(request: models.Login):
    url = 'userinfo'
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/folder/create')
async def folder_create_controller(request: models.FolderCreate):
    url = 'createfolderifnotexists'
    request.path = clean_path(request.path)
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/folder/list')
async def folder_list_controller(request: models.Folder):
    url = 'listfolder'
    path = clean_path(path)
    if (request.folderid is None and request.path is None):
        request.path = '/'
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/folder/rename')
async def folder_rename_controller(request: models.FolderUpdate):
    url = 'renamefolder'
    request.path = clean_path(request.path)
    request.topath = clean_path(request.topath)
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/folder/copy')
async def folder_copy_controller(request: models.FolderUpdate):
    url = 'copyfolder'
    request.path = clean_path(request.path)
    request.topath = clean_path(request.topath) 
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/folder/delete')
async def folder_delete_controller(request: models.Folder):
    url = 'deletefolderrecursive'
    request.path = clean_path(request.path)
    if (request.path is not None and request.path == '/'):
        return "You can't delete root folder by path"
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/file/upload')
async def file_upload_controller(
    file: UploadFile = File(...),
    auth: str = Form(...),
    path: Optional[str] = Form(None),
    folderid: Optional[str] = Form(None),
    nopartial: Optional[str] = Form(None),
    progresshash: Optional[str] = Form(None),
    renameifexists: Optional[str] = Form(None),
    mtime: Optional[str] = Form(None),
    ctime: Optional[str] = Form(None)):
    url = 'uploadfile'
    request = {
        'auth': auth,
        'path': path,
        'folderid': folderid,
        'filename': file.filename,
        'nopartial': nopartial,
        'progresshash': progresshash,
        'renameifexists': renameifexists,
        'mtime': mtime,
        'ctime': ctime
    }
    request['path'] = clean_path(request['path'])
    pbody = {k: v for k, v in request.items() if v is not None}
    files = {'': (file.filename, file.file)}
    response = requests.post(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}', files=files)
    return response.json()

@app.post('/file/stat')
async def file_stat_controller(request: models.File):
    url = 'stat'
    request.path = clean_path(request.path)
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/file/rename')
async def file_rename_controller(request: models.FileUpdate):
    url = 'renamefile'
    request.path = clean_path(request.path)
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/file/copy')
async def file_copy_controller(request: models.FileUpdate):
    url = 'copyfile'
    request.path = clean_path(request.path)
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/file/delete')
async def file_delete_controller(request: models.File):
    url = 'deletefile'
    request.path = clean_path(request.path)
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/share/create')
async def share_create_controller(request: models.Share):
    url = 'sharefolder'
    request.path = clean_path(request.path)
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/share/list')
async def share_list_controller(request: models.ShareList):
    url = 'listshares'
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/share/update')
async def share_update_controller(request: models.ShareList):
    url = 'changeshare'
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.post('/share/delete')
async def share_delete_controller(request: models.ShareList):
    url = 'removeshare'
    pbody = {k: v for k, v in dict(request).items() if v is not None}
    response = requests.get(f'{pcloud_url}/{url}?{urllib.parse.urlencode(pbody)}')
    return response.json()

@app.get('/values')
async def values_controller():
    return 'Api is running'

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8085, reload=True) # uvicorn app:app --port=8083 --reload
    # app.run(host='0.0.0.0') # flask run