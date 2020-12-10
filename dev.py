import sys
import os

def init(app, env):
	os.system("FLASK_APP=%s FLASK_ENV=%s flask run" % (app, env))

def db_init(user, id, db):
	#  os.system("sudo mysql")
	# ...
	#  os.system("mysql -u %(user)s -D %(db)s -p" % {user:user, db:db))


	#  os.system("python")
	#  from survey import db, create_app
	#  db.create_all(app=create_app())

	pass

if __name__== "__main__":
	app = sys.argv[1] if len(sys.argv) > 1 else "survey"
	env = sys.argv[2] if len(sys.argv) > 2 else "development"
	init(app, env)
	
	db_init("survey", "waDBlog", "Survey")
