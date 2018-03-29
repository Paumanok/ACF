import mfrc522
import picoweb
import load_sensor
import easydriver_esp
import acf_network as w
import coroutines as c
import tinyDB
import routes

db = tinyDB.TinyDB()

r = routes.Route(db)

cr = c.Coroutines(db)

while cr.net.isConnected() == False:
    pass

funcs = [cr.networkRoutine]

app = picoweb.WebApp(__name__,r.ROUTES)

app.run(debug=True, host=cr.net.wlan.ifconfig()[0], func_list=funcs)
