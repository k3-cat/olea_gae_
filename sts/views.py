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
        'UJ': push.uj,
        'PY': push.py,
        'HQ': push.hq
    }

def push_(request):
    i = request.GET['i'].split(';')
    proj = Project(pid=i[0])
    if i[1] not in ('KP', 'UJ', 'LB'):
        return HttpResponse(False)
    if i[1] == 'LB':
        push.lb(proj, i[2], request.GET.get('vu'))
    else:
        response = PUSH_MAP[i[1]](proj, i[2])
        if not response:
            return HttpResponse(False)
        proj.save()
    records.update_process_info(proj)
    return HttpResponse(True)

def edit_staff(request):
    uid = request.COOKIES.get('uid', None)
    if not uid:
        return HttpResponseRedirect('/login')
    user = User(uid)
    user_info = user.info()
    if request.method == 'GET':
        i = request.GET['i'].split(',')
        proj = Project(i[0])
        req = proj[f'req.{i[1]}']
        rows = proj['staff'].detials(i[1])
        return render(request, 'es.html', {
            'i': f'{i[0]},{i[1]},{i[2]}',
            'user1': user_info,
            'edit': i[1] in user_info['groups'],
            'req': req,
            'rows': rows,
            'empty': ['']*(req-len(rows)),
            'name': proj.name,
            'note': ''})
    if request.method == 'POST':
        i = request.POST['i'].split(',')
        if i[1] not in user_info['group']:
            return HttpResponseRedirect(f'/es?i={i[0]},{i[1]},{i[2]}')
        proj = Project(i[0])
        # 验证项目状态
        opt = request.POST.get('opt', None) # finish & add & change req
        if opt[0] == "F":
            proj['staff'].finish_job(i[1], uid)
            if proj['staff'].get_state(i[1]) == 0:
                PUSH_MAP[i[1]](proj, i[2])
                records.update_process_info(proj)
        elif opt == 'A':
            proj['staff'].add_staff(i[1], uid, request.POST['job'])
        elif opt:
            proj['staff'].set_req(i[1], opt)
            records.update_req_display(proj, i[1], i[2])
        proj.save()
        records.update_state(proj, i[1], i[2])
        records.update_nickname_display(proj, i[1], i[2])
        return HttpResponseRedirect(f'/es?i={i[0]},{i[1]},{i[2]}')
    return HttpResponse(False)

def new_projs(request):
    uid = request.COOKIES.get('uid', None)
    if not uid:
        return HttpResponseRedirect('/login')
    user = User(uid)
    user_info = user.info()
    if 'nimda' not in user_info['groups']:
        return HttpResponse(False)
    if request.method == 'GET':
        return render(request, 'np.html')
    if request.method == 'POST':
        datas = request.POST['d'].split('|')
        type_ = request.POST['t']
        projs = new.proj(datas)
        if type_ == 'T':
            append.fy(projs)
        elif type_ in ('G', 'K'):
            append.kp(projs)
        return HttpResponse(True)
    return HttpResponse(False)

def create(request):
    i = request.POST['i'].split(',')
    proj = Project(i[0])
    if i[1] == 'KP':
        response = files.create(proj, i[1], i[2], 'doc')
    elif i[1] in ('MS', 'PY', 'HQ'):
        response = files.create(proj, i[1], i[2], 'folder')
    proj.save()
    return HttpResponse(response)

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        name = request.POST['name']
        user = User.find_uid(name)
        if not user:
            return render(request, 'login.html', {'err': True})
        response = redirect('/')
        response.set_cookie('uid', user.uid, max_age=366*86400)
        return response
    return HttpResponse(False)
