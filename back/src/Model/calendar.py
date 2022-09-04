from Controller.basic import check
from Object.calendar import Calendar

def calendar_init(cn, nextc):
    cn.private["calendar"] = Calendar(user_id = cn.private["sso"].user["id"])
    err = [True, {}, None]
    return cn.call_next(nextc, err)

def calendar_get(cn, nextc):
    err = cn.private["calendar"].get_all()
    return cn.call_next(nextc, err)

def calendar_new(cn, nextc):
    err = check.contain(cn.pr, ["name"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = cn.private["calendar"].new(name = cn.pr["name"])
    return cn.call_next(nextc, err)

def calendar_by_id(cn, nextc):
    err = check.contain(cn.rt, ["calendar"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = cn.private["calendar"].set_id(id = cn.rt["calendar"])
    return cn.call_next(nextc, err)

def calendar_update(cn, nextc):
    err = check.contain(cn.pr, ["name", "options"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = cn.private["calendar"].update(cn.pr["name"], cn.pr["options"])
    return cn.call_next(nextc, err)
