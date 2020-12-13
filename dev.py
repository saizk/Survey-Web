import sys
import os

def init(app, env):
	os.system("FLASK_APP=%s FLASK_ENV=%s flask run" % (app, env))


if __name__== "__main__":
	cmd_args = [i for i in sys.argv[1:] if i.startswith("-")]
	str_args = [i for i in sys.argv[1:] if not i.startswith("-")]

	if "-r" in cmd_args:
		os.system("rm survey/db.sqlite")
		print("Previous database removed")

	app = str_args[0] if len(str_args) > 1 else "survey"
	env = str_args[1] if len(str_args) > 2 else "development"

	init(app, env)