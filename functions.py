
from base64 import b64encode


def obtener_id(nombre, dir=None):
  if dir: cambiar = "%s:%s" % (nombre, dir)
  else: cambiar = nombre
  id = b64encode(cambiar.encode()).decode('utf-8')
  return id[:22]