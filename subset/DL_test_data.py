#  https://python-overpy.readthedocs.io/en/latest/example.html#basic-example
import overpy

api = overpy.Overpass ( )

result = api.query ("[out:xml];(node(47.5272,7.5421,47.5996,7.6373);<;);out meta;")

