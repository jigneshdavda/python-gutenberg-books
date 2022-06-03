from app import app
import sys

sys.dont_write_bytecode = True
app.run(host='127.0.0.1', port=5000, debug=True)