from .rethink import Rethink
from .sso import Sso
import datetime


class Event(Rethink):
    def __init__(self, user_id = None, calendar_id = None, id = None):
        super(self).__init__(table = "event")
        self.user_id = user_id
        self.calendar_id = calendar_id
        self.id = None
        self.accepted_confirm = [True, False, None]

    def get_all(self):
        if self.calendar_id is None:
            return [False, "Internal Error", 500]
        ret = list(
            self.r.filter(
                {
                    "calendar_id": self.calendar_id
                }
            ).run(self.conn)
        )
        return [True, ret, None]

    def new(self, name, users_id, users_email, date_start, date_end, description):
        if self.user_id is None or self.calendar_id is None:
            return [False, "Internal Error: 000", 500]
        if not isinstance(name, str) and name is not None and len(name) < 56:
            return [False, "Name should be a string(56)", 400]
        if not isinstance(description, str) and description is not None and len(description) < 56:
            return [False, "Description should be a string(56)", 400]
        data = {
                "user_id": self.user_id,
                "calendar_id": self.calendar_id,
                "name": str(name),
                "date_start": self.r.epoch_time(date_start),
                "date_end": self.r.epoch_time(date_end),
                "creation": self.r.expr(datetime.now(self.r.make_timezone('+00:00'))),
                "description": str(description),
                "users": {}
        }
        i = 0
        while i < len(users_email):
            user_email = users_email[i]
            user_id = Sso().user_by_email(user_email)
            if user_id[0] is False:
                return [False, "Internal Error: 001", 500]
            data["users"][user_id[1]['id']] = {
                "email": user_email,
                "confirm": False,
                "invited_by": self.user_id
            }
            i += 1
        res = dict(self.r.insert([data]).run(self.conn))
        id = res["generated_keys"][0]
        ret = self.set_id(id)
        return ret

    def set_id(self, id):
        if self.calendar_id is None:
            return [False, "Internal Error: 002", 500]
        if not isinstance(id, str):
            return [False, "Event id should be a string", 400]
        ret = list(
            self.r.filter(
                {
                    "calendar_id": self.calendar_id,
                    "id": id
                }
            ).run(self.conn)
        )
        if len(ret) == 0:
            return [False, "Invalid event id", 404]
        if len(ret) > 1:
            return [False, "Internal Error: 003", 500]
        ret = ret[0]
        self.id = id
        return [True, ret, None]


    def invite(self, user_email):
        if self.id is None or self.user_id is None or self.calendar_id is None:
            return [False, "Internal Error: 004", 500]
        ret = list(
            self.r.filter(
                {
                    "calendar_id": self.calendar_id,
                    "id": self.id
                }
            ).run(self.conn)
        )
        if len(ret) == 0:
            return [False, "Invalid event id", 404]
        if len(ret) > 1:
            return [False, "Internal Error: 005", 500]
        users = ret[0]['users']
        user_id = Sso().user_by_email(user_email)
        if user_id not in users.keys():
            users[user_id] = {
                "email": user_email,
                "confirm": False,
                "invited_by": self.user_id
            }
        ret = self.r.filter(
            {
                "calendar_id": self.calendar_id,
                "id": self.id
            }
        )
        ret.update({'users': users}).run(self.conn)
        ret = self.set_id(self.id)
        return ret

    def update(self, name, description, date_start, date_end):
        if self.id is None or self.calendar_id is None:
            return [False, "Internal Error: 006", 500]
        if not isinstance(name, str) and name is not None and len(name) < 56:
            return [False, "Name should be a string(56)", 400]
        if not isinstance(description, str) and description is not None and len(description) < 56:
            return [False, "Description should be a string(56)", 400]
        if date_start is None or date_end is None:
            return [False, "Date start and Date end are mandatory", 400]
        update = {}
        if name is not None:
            update["name"] = name
        if description is not None:
            update["description"] = name
        ret = self.r.filter(
            {
                "calendar_id": self.calendar_id,
                "id": self.id
            }
        )
        ret.update(update).run(self.conn)
        ret.update(
            {
            "date_start": self.r.epoch_time(date_start),
            "date_end": self.r.epoch_time(date_end)
            }
        ).run(self.conn)
        ret = self.set_id(self.id)
        return ret

    def confirm(self):
        if self.id is None or self.user_id is None or self.calendar_id is None:
            return [False, "Internal Error: 007", 500]
        ret = list(
            self.r.filter(
                {
                    "calendar_id": self.calendar_id,
                    "id": self.id
                }
            ).run(self.conn)
        )
        if len(ret) == 0:
            return [False, "Invalid event id", 404]
        if len(ret) > 1:
            return [False, "Internal Error: 008", 500]
        users = ret[0]['users']
        if self.user_id not in users.keys():
            return [False, "User not invited", 404]
        users[user_id] = {
            "confirm": True,
        }
        ret = self.r.filter(
            {
                "calendar_id": self.calendar_id,
                "id": self.id
            }
        )
        ret.update({'users': users}).run(self.conn)
        ret = self.set_id(self.id)
        return ret
