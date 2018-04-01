import picoweb
import ujson as uj

json_content = b'application/json'

class Route:
    def __init__(self,db):
        self.ROUTES = [
                 ("/checkin",self.checkin),
             ]
        self.db = db

    def checkin(req, resp):
        if req.method == "GET":
            yield from picoweb.start_response(resp, content_type=json_content)
            config = self.db.getConfigs()
            yield from resp.awrite("{'test':'response'}")

        else:
            yield from picoweb.start_response(resp, content_type=json_content,status="501")
            yield from resp.awrite("{'test':'failure'}")
