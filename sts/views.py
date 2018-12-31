import json

from django.shortcuts import render
from django.http import HttpResponse

from .forms import GForm, TForm
from .europaea import records, files, push, new, append
from .europaea.database import Project


def hello(request):
    response = f'hello\n\n{str(request.body)}'
    return HttpResponse(response)

PUSH_MAP = {
        'FY': push.fy,
        'KP': push.kp,
        'SJ': push.sj,
        'PY': push.py,
        'HQ': push.hq
    }

def push_(request):
    body = json.loads(request.body)
    proj = Project(pid=body['pid'])
    sc = body['sc']
    row = body['row']
    PUSH_MAP[sc](proj, row)
    proj.save()
    records.update_process_info(proj)
    return HttpResponse(True)

def finish(request):
    proj = Project(pid=request.GET.get('pid'))
    row = request.GET.get('row')
    push.lb(proj, row, request.GET.get('vid_url'))
    return True

def edit_staff(request):
    if request.method == 'POST':
        proj = Project(pid=request.GET.get('pid'))
        sc = request.GET.get('sc')
        row = request.GET.get('row')
        if sc == 'FY':
            form = TForm(request.POST)
        elif sc in ('KP', 'PY', 'SJ', 'HQ'):
            form = GForm(request.POST)
        records.update_state(proj, sc, row)
    return render(request, 'es.html', {'city': 'abbc'})

def new_projs(request):
    body = json.loads(request.body)
    type_ = body['type']
    inos = body['inos']
    titles = body['titles']
    urls = body['urls']
    projs = new.proj(inos, titles, urls)
    if type_ == 'T':
        append.fy(projs)
    elif type_ in ('G', 'K'):
        append.kp(projs)
    return HttpResponse(True)

def create(request):
    body = json.loads(request.body)
    proj = Project(pid=body['pid'])
    sc = body['sc']
    row = body['row']
    if sc == 'KP':
        response = files.create(proj, sc, row, 'doc')
    elif sc in ('MS', 'PY', 'HQ'):
        response = files.create(proj, sc, row, 'folder')
    return HttpResponse(response)
