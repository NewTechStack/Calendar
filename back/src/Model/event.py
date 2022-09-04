from Controller.basic import check
from Object.event import Event

def event_init(cn, nextc):
    cn.private["event"] = Event(
        user_id=cn.private["calendar"].user_id,
        calendar_id=cn.private["calendar"].id
    )
    err = [True, {}, None]
    return cn.call_next(nextc, err)

def event_get(cn, nextc):
    err = cn.private["event"].get_all()
    return cn.call_next(nextc, err)

def event_new(cn, nextc):
    err = cn.private["event"].new()
    return cn.call_next(nextc, err)

def event_by_id(cn, nextc):
    err = check.contain(cn.rt, ["event"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = cn.private["event"].set_id(cn.rt["event"])
    return cn.call_next(nextc, err)

def event_update(cn, nextc):
    err = cn.private["event"].update()
    return cn.call_next(nextc, err)

def event_confirm(cn, nextc):
    err = cn.private["event"].confirm()
    return cn.call_next(nextc, err)

def event_invite(cn, nextc):
    err = cn.private["event"].invite()
    return cn.call_next(nextc, err)
