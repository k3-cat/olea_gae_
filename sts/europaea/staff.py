from . import sheets, records


def edit_req(proj, sc, req):
    proj.staff[sc]['req'] = int(req)
    proj.save()
    return True

def add(proj, sc, name, job):
    pass

def finish_job(proj, sc, name):
    pass
