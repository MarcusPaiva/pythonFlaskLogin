from flask import *
from Database import *
import hashlib

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#Start Database
db = Database()
db.create_connection("db.sqlite3")
db.create_cursor()
db.create_table_user()

#Default route to Home Page
@app.route( "/" )
@app.route( "/home" )
def index():
	return render_template("index.html")

#Create a user route
@app.route("/user/new", methods=["POST"])
def new_user():
	user_name     = request.form["username"]
	user_email    = request.form["useremail"]
	# Encrypt user password. Security always!
	user_password = hashlib.md5( request.form["userpassword"].encode('utf-8') )

	create_response = db.add_new_user( user_name, user_email, user_password.hexdigest() )
	#I'm using the index page as a login and user creation platform
	if create_response:
		return render_template( "index.html", status="User created successfully! " )
	else:
		return render_template( "index.html", status="Oops! I can't create your login!" )

#Login route
@app.route("/user/login", methods=["POST"])
def login():
	user_email    = request.form["useremail"]
	# Encrypt user password. Security always!
	user_password = hashlib.md5( request.form["userpassword"].encode('utf-8') )

	user = db.login(user_email,user_password.hexdigest() )

	if user:
		#I'm using the index page as a login and user creation platform
		return render_template("index.html", user=user)
	else:
		#If has error on login call index and inform user that there was an error
		return render_template("index.html", status="User not found!")

if __name__ == "__main__":
    app.run( host = "0.0.0.0", debug=True )
