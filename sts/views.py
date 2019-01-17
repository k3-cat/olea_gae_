from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect, render

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

SAFE_RANGE = {
    'FY': ('FY'),
    'KP': ('KP'),
    'PY': ('pu', 'PY'),
    'UJ': ('pu', 'hu'),
    'HQ': ('hu', 'HQ'),
    'LB': ('UP')
}

def push_(request):
    uid = request.COOKIES.get('uid', None)
    if not uid:
        return HttpResponseRedirect(f'/login?r={request.get_full_path()}')
    user = User(uid)
    user_info = user.info()
    if request.method == 'GET':
        i = request.GET['i'].split(',')
        if i[1] not in ('KP', 'UJ', 'LB'):
            return HttpResponse(False)
        proj = Project(i[0])
        if proj['ssc'] not in SAFE_RANGE[i[1]]:
            return HttpResponse('<script type="text/javascript">window.close()</script>')
        if i[1] == 'LB':
            return render('finish.html', {'i': i})
        else:
            if i[1] not in user_info['groups'] and 'nimda' not in user_info['groups']:
                return HttpResponse('<script type="text/javascript">window.close()</script>')
            response = PUSH_MAP[i[1]](proj)
        if not response:
            return HttpResponse(False)
        records.update_m_process_info(proj)
        return HttpResponse('<script type="text/javascript">window.close()</script>')
    if request.method == 'POST':
        i = request.POST['i'].split(',')
        if 'nimda' not in user_info['groups']:
            return HttpResponseRedirect('<script type="text/javascript">window.close()</script>')
        response = push.lb(Project(i[0]), request.POST.get('vu'))
        records.update_m_process_info(proj)
        return HttpResponse(True)
    proj.save()
    return HttpResponse('<script type="text/javascript">window.close()</script>')


def edit_staff(request):
    uid = request.COOKIES.get('uid', None)
    if not uid:
        return HttpResponseRedirect(f'/login?r={request.get_full_path()}')
    user = User(uid)
    user_info = user.info()
    if request.method == 'GET':
        i = request.GET['i'].split(',')
        proj = Project(i[0])
        if proj['ssc'] not in SAFE_RANGE[i[1]]:
            return HttpResponse('<script type="text/javascript">window.close()</script>')
        req = proj[f'req.{i[1]}']
        rows = proj['staff'].detials(i[1])
        return render(request, 'es.html', {
            'i': f'{i[0]},{i[1]}',
            'user1': user_info,
            'edit': i[1] in user_info['groups'],
            'req': req,
            'rows': rows,
            'empty': ['']*(req-len(rows)),
            'name': proj.name,
            'note': ''})
    if request.method == 'POST':
        i = request.POST['i'].split(',')
        if i[1] not in user_info['groups']:
            return HttpResponseRedirect(f'/es?i={i[0]},{i[1]}')
        proj = Project(i[0])
        opt = request.POST.get('opt', None) # finish & add & change req
        if opt[0] == "F":
            proj['staff'].finish_job(i[1], uid)
        elif opt == 'A':
            proj['staff'].add_staff(i[1], uid, request.POST['job'])
        elif opt:
            proj['staff'].set_req(i[1], opt)
        if proj['staff'].get_state(i[1]) == 0:
            PUSH_MAP[i[1]](proj)
            proj.save()
            records.update_m_process_info(proj)
            return HttpResponse('<script type="text/javascript">window.close()</script>')
        proj.save()
        records.update_s_state(proj, i[1])
        records.update_m_process_info(proj)
        return HttpResponseRedirect(f'/es?i={i[0]},{i[1]}')
    return HttpResponse('<script type="text/javascript">window.close()</script>')


def new_projs(request):
    uid = request.COOKIES.get('uid', None)
    if not uid:
        return HttpResponseRedirect(f'/login?r={request.get_full_path()}')
    user = User(uid)
    user_info = user.info()
    if 'nimda' not in user_info['groups']:
        return HttpResponse(False)
    if request.method == 'GET':
        return render(request, 'np.html')
    if request.method == 'POST':
        items = request.POST['d'].split('\r\n')
        type_ = request.POST['t']
        projs = new.proj(items)
        if type_ == 'T':
            append.fy(projs)
        elif type_ in ('G', 'K'):
            append.kp(projs)
        return HttpResponse(True)
    return HttpResponse('<script type="text/javascript">window.close()</script>')

def manage_staff(request):
    uid = request.COOKIES.get('uid', None)
    if not uid:
        return HttpResponseRedirect(f'/login?r={request.get_full_path()}')
    user = User(uid)
    user_info = user.info()
    if 'ms' not in user_info['groups'] and 'nimda' not in user_info['groups']:
        return HttpResponse(False)
    if request.method == 'GET':
        i = request.GET['i'].split(',')
        proj = Project(i[0])
        if proj['ssc'] not in SAFE_RANGE[i[1]]:
            return HttpResponse('<script type="text/javascript">window.close()</script>')
        req = proj[f'req.{i[1]}']
        rows = proj['staff'].detials(i[1])
        return render(request, 'ms.html', {
            'i': f'{i[0]},{i[1]}',
            'user1': user_info,
            'edit': i[1] in user_info['groups'],
            'req': req,
            'rows': rows,
            'empty': ['']*(req-len(rows)),
            'name': proj.name,
            'note': ''})
    if request.method == 'POST':
        i = request.POST['i'].split(',')
        proj = Project(i[0])
        opt = request.POST.get('opt', None) # finish & add & change req
        if opt[0] == "F":
            proj['staff'].finish_job(i[1], request.POST['uid'])
        elif opt == 'A':
            proj['staff'].add_staff(i[1], request.POST['uid'], request.POST['job'])
        elif opt:
            proj['staff'].set_req(i[1], opt)
        if proj['staff'].get_state(i[1]) == 0:
            PUSH_MAP[i[1]](proj)
            proj.save()
            records.update_m_process_info(proj)
            return HttpResponse('<script type="text/javascript">window.close()</script>')
        proj.save()
        records.update_s_state(proj, i[1])
        records.update_m_process_info(proj)
        return HttpResponseRedirect(f'/ms?i={i[0]},{i[1]}')
    return HttpResponse('<script type="text/javascript">window.close()</script>')

def update_info(request):
    uid = request.COOKIES.get('uid', None)
    if not uid:
        return HttpResponseRedirect(f'/login?r={request.get_full_path()}')
    user = User(uid)
    user_info = user.info()
    if 'nimda' not in user_info['groups']:
        return HttpResponse(False)
    i = request.GET['i'].split(',')
    proj = Project(i[0])
    records.update_m_process_info(proj)
    if i[1] != '':
        records.update_s_state(proj, i[1])
    return HttpResponse('<script type="text/javascript">window.close()</script>')


def create(request):
    i = request.GET['i'].split(',')
    proj = Project(i[0])
    if i[1] == 'KP':
        response = files.create(proj, i[1], 'doc')
    elif i[1] in ('UJ', 'PY', 'HQ'):
        response = files.create(proj, i[1], 'folder')
    return HttpResponse(response)

def login(request):
    uid = request.COOKIES.get('uid', None)
    if uid:
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return render(request, 'login.html', {'r': request.GET['r']})
    if request.method == 'POST':
        name = request.POST['name']
        user = User.find_uid(name)
        if not user:
            return render(request, 'login.html', {'err': True})
        url = request.POST.get('r', None)
        if url:
            response = redirect(url)
        else:
            response = redirect('/')
        response.set_cookie('uid', user.uid, max_age=90*86400)
        return response
    return HttpResponse('<script type="text/javascript">window.close()</script>')
