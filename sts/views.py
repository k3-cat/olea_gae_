import json

from django.shortcuts import render
from django.http import HttpResponse

from .europaea import records, files, push, new, append
from .europaea.database import Project


def hello(request):
    return HttpResponse("hello")

def do_push(request):
    body = json.loads(request.body)
    sc = body['sc']
    row = body['row']
    proj = Project(pid=body['pid'])
    if sc == 'FY':
        push.fy(proj, row)
    elif sc == 'KP':
        push.kp(proj, row)
    elif sc == 'MS':
        push.sj(proj, row)
    elif sc == 'PY':
        push.py(proj, row)
    elif sc == 'HQ':
        push.hq(proj, row)
    elif sc == 'LB':
        push.lb(proj, row, body['vid_url'])
    proj.save()
    records.update_process_info(proj)
    return HttpResponse('True')

def edit_staff(request):
    body = json.loads(request.body)
    row = body['row']
    proj = Project(pid=body['pid'])
    return HttpResponse('empty')

def new_projs(request):
    body = json.loads(request.body)
    type_ = body['type']
    inos = body['inos']
    titles = body['titles']
    urls = body['urls']
    projs = new.new_proj(inos, titles, urls)
    if type_ == 'T':
        append.fy(projs)
    elif type_ in ('G', 'K'):
        append.kp(projs)
    return HttpResponse('True')

def create(request):
    body = json.loads(request.body)
    sc = body['sc']
    row = body['row']
    proj = Project(pid=body['pid'])
    if sc == 'KP':
        responce = files.create(proj, sc, row, 'doc')
    elif sc in ('MS', 'PY', 'HQ'):
        responce = files.create(proj, sc, row, 'folder')
    return HttpResponse(responce)
