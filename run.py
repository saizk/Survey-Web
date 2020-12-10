import sys
import os

def init(app, env):
	os.system("export FLASK_APP=%s" % app)
	os.system("export FLASK_ENV=%s" % env)
	os.system("flask run")

if __name__==__main__:
	app, env = sys.argv[1], sys.argv[2]
	init(app, env)
