from .rethink import Rethink
import datetime

class Calendar(Rethink):
    def __init__(self, user_id = None):
        super().__init__(table = "calendar")
        self.user_id = user_id
        self.id = None
        self.accepted_view = ["day", "week", "month"]

    def get_all(self):
        if self.user_id is None:
            return [False, "Internal Error: 009", 500]
        ret = list(
            self.r.filter(
                {
                    "user_id": self.user_id,
                }
            ).run(self.conn)
        )
        if len(ret) == 0:
            if self.new("Default")[0] is False:
                return [False, "Internal Error: 010", 500]
            return self.get_all()
        return [True, ret, None]

    def new(self, name):
        if self.user_id is None:
            return [False, "Internal Error", 500]
        if not isinstance(name, str):
            return [False, "Name should be a string", 400]
        data = {
                "user_id": self.user_id,
                "name": str(name),
                "options": {
                    "view": "week"
                },
                "date": str(datetime.datetime.utcnow())
        }
        res = dict(self.r.insert([data]).run(self.conn))
        id = res["generated_keys"][0]
        ret = self.set_id(id)
        return ret

    def set_id(self, id):
        if self.user_id is None:
            return [False, "Internal Error: 011", 500]
        if not isinstance(id, str):
            return [False, "Calendar id should be a string", 400]
        ret = list(
            self.r.filter(
                {
                    "user_id": self.user_id,
                    "id": id
                }
            ).run(self.conn)
        )
        if len(ret) == 0:
            return [False, "Invalid calendar id", 404]
        if len(ret) > 1:
            return [False, "Internal Error: 012", 500]
        ret = ret[0]
        self.id = id
        return [True, ret, None]

    def update(self, name, options):
        if self.id is None or self.user_id is None:
            return [False, "Internal Error: 013", 500]
        if not isinstance(name, str) and name is not None and len(name) < 56:
            return [False, "Name should be a string(56)", 400]
        if not isinstance(options, dict) and options is not None:
            return [False, "Options should be a dictionnary", 400]
        update = {}
        if name is not None:
            update["name"] = name
        if "view" in options:
            if options["view"] not in self.accepted_view:
                return [False, f"Invalid view options, view should be in {self.accepted_view}", 404]
            update["options"] = {}
            update["options"]["view"] = options["view"]
        ret = self.r.filter(
            {
                "user_id": self.user_id,
                "id": self.id
            }
        ).update(update).run(self.conn)
        ret = self.set_id(self.id)
        return ret
