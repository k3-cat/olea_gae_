import json

from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect

from .europaea import append, files, new, push, records
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
    if request.method == 'GET':
        pid = request.GET.get('p')
        proj = Project(pid)
        sc = request.GET.get('s')
        row = request.GET.get('r')
        rows = proj[f'staff'].detials(sc)
        req = proj[f'req.{sc}']
        return render(request, 'es.html', {
            'pid': pid,
            'sc': sc,
            'row': row,
            'user1': {
                'uid': 'K3', # request.COOKIES.get('uid'),
                'root': False},
            'req': req,
            'rows': rows,
            'empty': ['']*(req-len(rows)),
            'name': proj.name,
            'note': ''})
    if request.method == 'POST':
        info = request.POST['info'].split(';')
        proj = Project(info[0])
        # 验证项目状态
        opt = request.POST.get('opt', None) # finish & add & change req
        job = request.POST.get('job', None)
        if opt[0] == "F":
            proj['staff'].finish_job(sc, name)
            if proj['staff'].get_state(sc) == 0:
                PUSH_MAP[sc](proj, row)
                records.update_process_info(proj)
        elif opt == 'A':
            uid =
            proj['staff'].add_staff(sc, uid, job)
        elif opt:
            proj[f'req.{sc}'] = int(opt)
        records.update_state(proj, sc, row)
        proj.save()
        return HttpResponseRedirect(f'/es?p={info[0]}&s={info[1]}&r={info[2]}')

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
    proj.save()
    return HttpResponse(response)
