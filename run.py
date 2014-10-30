from app import app
from sys import argv

if len(argv) > 1 and argv[1] == '-d':
    debug = True
else:
    debug  = False

print debug

app.run(debug=debug)

