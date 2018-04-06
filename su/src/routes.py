import picoweb
import ujson as uj

json_content = b'application/json'

class Route:
    def __init__(self,db,cr):
        self.ROUTES = [
                 ("/calibrate",self.calibrate),
             ]
        # Database reference
        self.db = db
        # Coroutine object reference for state variables
        self.cr = cr


    def calibrate(req, resp):
        if req.method == "GET":
            yield from picoweb.start_response(resp, content_type=json_content)
            self.cr.load.calibrate(5)
            yield from resp.awrite("{'calib': True}")

        else:
            yield from picoweb.start_response(resp, content_type=json_content,status="501")
            yield from resp.awrite("{'bool': False}")