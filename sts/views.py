import json

from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect

from .europaea import append, files, new, push, records
from .europaea.database import Project, User


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
        uid = request.COOKIES.get('uid', None)
        if not uid:
            root = False
        else:
            user = User(uid)
            root = user.is_root()
        pid = request.GET.get('p')
        proj = Project(pid)
        sc = request.GET.get('s')
        req = proj[f'req.{sc}']
        rows = proj['staff'].detials(sc)
        return render(request, 'es.html', {
            'pid': pid,
            'sc': sc,
            'row': request.GET.get('r'),
            'user1': {
                'uid': uid,
                'root': root},
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
        uid = request.COOKIES.get('uid', None)
        if not uid:
            return HttpResponseRedirect('/login')
        if opt[0] == "F":
            proj['staff'].finish_job(info[1], uid)
            if proj['staff'].get_state(info[1]) == 0:
                PUSH_MAP[info[1]](proj, info[2])
                records.update_process_info(proj)
        elif opt == 'A':
            proj['staff'].add_staff(info[1], uid, request.POST['job'])
        elif opt:
            proj[f'req.{info[1]}'] = int(opt)
        records.update_state(proj, info[1], info[2])
        proj.save()
        return HttpResponseRedirect(f'/r/es?p={info[0]}&s={info[1]}&r={info[2]}')
    return HttpResponse(False)

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

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        nickname = request.POST['nickname']
        user = User.find_uid(nickname)
        if not user:
            return render(request, 'login.html', {'err': True})
        response = redirect('/')
        response.set_cookie('uid', user.uid, max_age=366*86400)
        return response
    return HttpResponse(False)
