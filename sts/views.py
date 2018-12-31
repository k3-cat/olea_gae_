import json

from django.shortcuts import render
from django.http import HttpResponse

from .forms import SForm
from .europaea import records, files, push, new, append
from .europaea.database import Project


def hello(request):
    response = f'hello\n\n{request.body}'
    return HttpResponse(response)

PUSH_MAP = {
        'FY': push.fy,
        'KP': push.kp,
        'SJ': push.sj,
        'PY': push.py,
        'HQ': push.hq
    }

def push_(request):
    proj = Project(pid=request.GET.get('p'))
    sc = request.GET.get('s')
    row = request.GET.get('r')
    PUSH_MAP[sc](proj, row)
    proj.save()
    records.update_process_info(proj)
    return HttpResponse(True)

def finish(request):
    proj = Project(pid=request.GET.get('p'))
    row = request.GET.get('r')
    push.lb(proj, row, request.GET.get('vu'))
    return True

def edit_staff(request):
    if request.method == 'POST':
        proj = Project(pid=request.GET.get('p'))
        sc = request.GET.get('s')
        row = request.GET.get('r')
        form = SForm(request.POST)
        records.update_state(proj, sc, row)
    return render(request, 'es.html', {'city': 'abbc'})

def new_projs(request):
    body = json.loads(request.body)
    type_ = body['t']
    inos = body['is']
    titles = body['ts']
    urls = body['us']
    projs = new.proj(inos, titles, urls)
    if type_ == 'T':
        append.fy(projs)
    elif type_ in ('G', 'K'):
        append.kp(projs)
    return HttpResponse(True)

def create(request):
    body = json.loads(request.body)
    proj = Project(pid=body['p'])
    sc = body['s']
    row = body['r']
    if sc == 'KP':
        response = files.create(proj, sc, row, 'doc')
    elif sc in ('MS', 'PY', 'HQ'):
        response = files.create(proj, sc, row, 'folder')
    return HttpResponse(response)
