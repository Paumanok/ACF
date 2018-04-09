import utime
# Debug sleep for when using RX TX as gpio for rfid
# since the repl won't be availble after being
# reconfigured
utime.sleep(5)

import picoweb
import acf_network as w
import coroutines as c
import tinyDB
import routes

db = tinyDB.TinyDB()

cr = c.Coroutines(db,DBG=True)

r = routes.Routes(db,cr)

funcs = [cr.networkRoutine,cr.petRoutine,cr.dispenseRoutine]

app = picoweb.WebApp(__name__,r.ROUTES)

while cr.net.isConnected() == False:
    pass

app.run(debug=True, host=cr.net.wlan.ifconfig()[0], func_list=funcs)
