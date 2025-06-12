from urllib3 import PoolManager
from json import dumps, loads

PoolManager().request(
    'POST',
    "http://192.168.2.100/json/state",
    dumps({"on": not loads(PoolManager().request('GET', "http://192.168.2.100/json/state").data.decode('utf-8')).get("on", False)})
)
