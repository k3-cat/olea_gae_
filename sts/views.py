from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect, render

from .europaea import append, new, push, records
from .europaea.database import Project, User


def hello(request):
    response = '欢迎使用olea'
    return HttpResponse(response)

PUSH_MAP = {
    'FY': push.fy,
    'KP': push.kp,
    'UJ': push.uj,
    'PY': push.py,
    'HQ': push.hq
}

APPEND_MAP = {
    'FY': append.fy,
    'KP': append.kp,
    'UJ': append.uj,
    'PY': append.py,
    'HQ': append.hq,
    'UP': append.up
}

SAFE_RANGE = {
    'FY': ('FY'),
    'KP': ('KP'),
    'PY': ('pu', 'PY'),
    'UJ': ('pu', 'hu'),
    'HQ': ('hu', 'HQ'),
    'UP': ('UP')
}

def push_(request):
    uid = request.COOKIES.get('uid', None)
    if not uid:
        return HttpResponseRedirect(f'/login?r={request.get_full_path()}')
    user = User(uid)
    if request.method == 'GET':
        i = request.GET['i'].split(',')
        proj = Project(i[0])
        if proj['ssc'] not in SAFE_RANGE[i[1]]:
            return HttpResponseRedirect('/q')
        if i[1] == 'UP':
            return render(request, 'finish.html', {'i': i[0]})
        elif i[1] in ('KP', 'UJ'):
            if not user.in_groups((i[1], 'nimda')):
                return HttpResponse('不是相应的用户组成员')
            response = PUSH_MAP[i[1]](proj)
            if isinstance(response, str):
                return HttpResponse(f'项目错误: {response}') # nessery return
    elif request.method == 'POST':
        i = request.POST['i']
        if user.in_groups(['nimda']):
            response = push.up(Project(i), request.POST['vu'])
            return HttpResponse(response)
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
        if len(i) > 2 and not user.in_groups(('ms', 'nimda')):
            return HttpResponseRedirect(f'/es?i={i[0]},{i[1]}')
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
        parm = {
            'i': {'p': i[0], 's': i[1]},
            'user1': user_info,
            'rows': rows,
            'empty': empty,
            'name': proj.name,
            'message': request.GET.get('m', None),
            'note': ''}
        if len(i) > 2:
            return render(request, 'ms.html', parm)
        else:
            parm['joined'] = (proj[f'staff.{i[1]}'] is not None
                              and user_info['uid'] in proj[f'staff.{i[1]}'])
            return render(request, 'es.html', parm)
    elif request.method == 'POST':
        i = request.POST['i'].split(',')
        proj = Project(i[0])
        opt = request.POST['opt']
        if len(i) > 2 and user.in_groups(('ms', 'nimda')):
            uid = request.POST['uid']
        OPT_MAP = {
            "F": proj['staff'].finish_job,
            'A': proj['staff'].add_staff,
            'R': proj['staff'].set_req,
            'E': proj['staff'].edit_job,
            'D': proj['staff'].del_staff
        }
        response = OPT_MAP[opt](i[1], uid, request.POST.get('data', None))
        proj.save()
        records.update_s_state(proj, i[1])
        records.update_m_process_info(proj)
        if proj['staff'].get_state(i[1]) == 0:
            PUSH_MAP[i[1]](proj)
            proj.save()
        if isinstance(response, str):
            return HttpResponseRedirect(f'/es?i={",".join(i)}&m={response}')
        return HttpResponseRedirect(f'/es?i={",".join(i)}')
    return HttpResponseRedirect('/q')


def new_projs(request):
    uid = request.COOKIES.get('uid', None)
    if not uid:
        return HttpResponseRedirect(f'/login?r={request.get_full_path()}')
    user = User(uid)
    if not user.in_groups(['nimda']):
        return HttpResponse('不是相应的用户组成员')
    if request.method == 'GET':
        return render(request, 'np.html', {'errors': 0})
    if request.method == 'POST':
        response = new.projects(request.POST['d'].split('\r\n'), request.POST['t'])
        return render(request, 'np.html', {'errors': response})
    return HttpResponseRedirect('/q')

def back(request):
    uid = request.COOKIES.get('uid', None)
    if not uid:
        return HttpResponseRedirect(f'/login?r={request.get_full_path()}')
    user = User(uid)
    if not user.in_groups(['nimda']):
        return HttpResponse('不是相应的用户组成员')
    i = request.GET['i'].split(',')
    proj = Project(i[0])
    if proj['ssc'] not in SAFE_RANGE[i[1]]:
        return HttpResponse('项目错误')
    records.update_m_process_info(proj)
    if i[1] in ('FY', 'KP', 'PY', 'UJ', 'HQ', 'UP'):
        if len(i) > 2:
            APPEND_MAP[i[1]](proj)
        records.update_s_state(proj, i[1])
    return HttpResponseRedirect('/q')


def login(request):
    uid = request.COOKIES.get('uid', None)
    if uid:
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return render(request, 'login.html', {'r': request.GET.get('r', None)})
    elif request.method == 'POST':
        name = request.POST['name']
        uid = User.find_uid(name)
        if not uid:
            return render(request, 'login.html', {'err': True})
        url = request.POST.get('r', None)
        if url:
            response = redirect(url)
        else:
            response = redirect('/')
        response.set_cookie('uid', uid, max_age=90*86400, httponly=True, secure=True)
        return response
    return HttpResponseRedirect('/q')


def quit_page(request):
    return HttpResponse('<script type="text/javascript">window.close()</script>')
