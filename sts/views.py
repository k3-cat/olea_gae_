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
        proj = Project(i[0])
        if proj['ssc'] not in SAFE_RANGE[i[1]]:
            return HttpResponseRedirect('/q')
        if i[1] == 'LB':
            return render('finish.html', {'i': i})
        elif i[1] in ('KP', 'UJ'):
            if i[1] not in user_info['groups'] and 'nimda' not in user_info['groups']:
                return HttpResponse(False)
            response = PUSH_MAP[i[1]](proj)
            if not response:
                return HttpResponse(False)
    elif request.method == 'POST':
        i = request.POST['i'].split(',')
        if 'nimda' in user_info['groups']:
            response = push.lb(Project(i[0]), request.POST['vu'])
            return HttpResponse(True)
    proj.save()
    return HttpResponseRedirect('/q')


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
            return HttpResponseRedirect('/q')
        req = proj[f'req.{i[1]}']
        if req is None:
            rows = []
            empty = []
        else:
            rows = proj['staff'].detials(i[1])
            empty = ['']*(req-len(rows))
        return render(request, 'es.html', {
            'i': {'p': i[0], 's': i[1]},
            'user1': user_info,
            'joined': proj[f'staff.{i[1]}'] is not None and user_info['uid'] in proj[f'staff.{i[1]}'],
            'req': req,
            'rows': rows,
            'empty': empty,
            'name': proj.name,
            'note': ''})
    elif request.method == 'POST':
        i = request.POST['i'].split(',')
        if i[1] not in user_info['groups']:
            return HttpResponseRedirect(f'/es?i={i[0]},{i[1]}')
        proj = Project(i[0])
        opt = request.POST['opt']
        if opt == "F":
            proj['staff'].finish_job(i[1], uid)
        elif opt == 'A':
            proj['staff'].add_staff(i[1], uid, request.POST['data'])
        elif opt == 'R':
            proj['staff'].set_req(i[1], request.POST['data'])
        elif opt == 'E':
            proj['staff'].edit_job(i[1], uid, request.POST['data'])
        elif opt == 'D':
            proj['staff'].del_staff(i[1], uid)
        proj.save()
        records.update_s_state(proj, i[1])
        records.update_m_process_info(proj)
        if proj['staff'].get_state(i[1]) == 0:
            PUSH_MAP[i[1]](proj)
            return HttpResponseRedirect('/q')
        return HttpResponseRedirect(f'/es?i={i[0]},{i[1]}')
    return HttpResponseRedirect('/q')


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
    return HttpResponseRedirect('/q')

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
            return HttpResponseRedirect('/q')
        req = proj[f'req.{i[1]}']
        if req is None:
            rows = []
            empty = []
        else:
            rows = proj['staff'].detials(i[1])
            empty = ['']*(req-len(rows))
        return render(request, 'ms.html', {
            'i': {'p': i[0], 's': i[1]},
            'user1': user_info,
            'req': req,
            'rows': rows,
            'empty': empty,
            'name': proj.name,
            'note': ''})
    elif request.method == 'POST':
        i = request.POST['i'].split(',')
        proj = Project(i[0])
        opt = request.POST['opt']
        if opt == "F":
            proj['staff'].finish_job(i[1], request.POST['uid'])
        elif opt == 'A':
            proj['staff'].add_staff(i[1], request.POST['uid'], request.POST['data'])
        elif opt == 'R':
            proj['staff'].set_req(i[1], request.POST['data'])
        elif opt == 'E':
            proj['staff'].edit_job(i[1], request.POST['uid'], request.POST['data'])
        elif opt == 'D':
            proj['staff'].del_staff(i[1], request.POST['uid'])
        proj.save()
        records.update_s_state(proj, i[1])
        records.update_m_process_info(proj)
        if proj['staff'].get_state(i[1]) == 0:
            PUSH_MAP[i[1]](proj)
            return HttpResponseRedirect('/q')
        return HttpResponseRedirect(f'/ms?i={i[0]},{i[1]}')
    return HttpResponseRedirect('/q')

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
    if i[1] in ('FY', 'KP', 'PY', 'UJ', 'HQ'):
        records.update_s_state(proj, i[1])
    return HttpResponseRedirect('/q')


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
        return render(request, 'login.html', {'r': request.GET.get('r', None)})
    elif request.method == 'POST':
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
    return HttpResponseRedirect('/q')


def quit_page(request):
    return HttpResponse('<script type="text/javascript">window.close()</script>')
