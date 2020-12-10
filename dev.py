import sys
import os

def init(app, env):
	os.system("FLASK_APP=%s FLASK_ENV=%s flask run" % (app, env))

if __name__== "__main__":
	app = sys.argv[1] if len(sys.argv) > 1 else "survey"
	env = sys.argv[2] if len(sys.argv) > 2 else "development"
	init(app, env)
