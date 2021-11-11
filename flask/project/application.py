from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from addi import login_required
from tempfile import mkdtemp

app = Flask(__name__)

db = SQL("sqlite:///data.db")
sb = SQL("sqlite:///stddata.db")

app.config["TEMPLATES_AUTO_RELOAD"] = False

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def welcome():
   return render_template("welcome.html")

@app.route('/sregister', methods=['GET','POST'])
def sregister():
   if request.method == 'GET':
      return render_template ("studentform.html")
   else:
      username = request.form.get("username")
      phone = request.form.get("phone")
      confirm_password = request.form.get("cpass")
      password = request.form.get("pass")
      first = request.form.get("fname")
      last = request.form.get("lname")
      father = request.form.get("fathername")
      age = request.form.get("age")
      village = request.form.get("village")
      city = request.form.get("city")
      state = request.form.get("state")

      usernames = sb.execute("SELECT username FROM susers")

      if not phone or not username or not password:
         return render_template("studentform.html", error = "please fill all the login information",
                                          username=username, phone=phone, password=password, confirm_password=confirm_password,
                                          first=first,last=last,father=father,age=age, village=village,city=city,state=state)

      for name in usernames:
         if username in name["username"]:
            return render_template("studentform.html" , error="this username is already taken please enter anothere username",
                                          username=username, phone=phone, password=password, confirm_password=confirm_password,
                                          first=first,last=last,father=father,age=age, village=village,city=city,state=state)

      val = valid_password(password)
      if val != True:
           return render_template("studentform.html" , error= val ,
                                          username=username, phone=phone, password=password, confirm_password=confirm_password,
                                          first=first,last=last,father=father,age=age, village=village,city=city,state=state)

      if confirm_password != password:
         return render_template("studentform.html", error = "passwords do not match",
                                          username=username, phone=phone, password=password, confirm_password=confirm_password,
                                          first=first,last=last,father=father,age=age, village=village,city=city,state=state)


      if not first or not last or not father or not age or not village or not city or not state:
         return render_template("studentform.html", error = "please fill the entire form ",
                                          username=username, phone=phone, password=password, confirm_password=confirm_password,
                                          first=first,last=last,father=father,age=age, village=village,city=city,state=state)

      if len(phone) != 10:
         return render_template("studentform.html", error = "please fill the correct phone number",
                                          username=username, phone=phone, password=password, confirm_password=confirm_password,
                                          first=first,last=last,father=father,age=age, village=village,city=city,state=state)


      sb.execute("INSERT INTO susers (username, phone, password) VALUES(?,?,?)",username, phone, generate_password_hash(password, "sha256"))
      current_id = sb.execute("SELECT userID FROM susers WHERE username = ?",username)
      sb.execute("INSERT INTO sper (userID,first, last, father, age ) VALUES(?,?,?,?,?)",current_id[0]["userID"],first, last,father,age)
      sb.execute("INSERT INTO sadd (userID,village, city, state) VALUES(?,?,?,?)",current_id[0]["userID"],village.strip("village,-, VILLAGE,Village ").lower(),
                                                                                                city,state)
      return redirect('/slogin')

@app.route('/tregister', methods=['GET','POST'])
def tregister():
   if request.method == 'GET':
      return render_template("teacherform.html")
   else :
      username = request.form.get("username")
      phone = request.form.get("phone")
      confirm_password = request.form.get("cpass")
      password = request.form.get("pass")
      usernames = db.execute("SELECT username FROM tusers")
      subjects = request.form.get("subjects")
      quali = request.form.get("quali")
      exper = request.form.get("experience")

      first = request.form.get("fname")
      last = request.form.get("lname")
      father = request.form.get("fathername")
      gender = request.form.get("radio")
      age = request.form.get("age")
      village = request.form.get("village")
      city = request.form.get("city")
      state = request.form.get("state")

      if not phone or not username or not password:
         return render_template("teacherform.html", error = "please fill all the login information",
                                       username=username, phone=phone, password=password, confirm_password=confirm_password,
                                       subjects=subjects, quali=quali,exper=exper, first=first,last=last,father=father,age=age, village=village,city=city,state=state)

      for name in usernames:
         if username in name["username"]:
            return render_template("teacherform.html", error = "this username is already taken, type another one!",
                                       username=username, phone=phone, password=password, confirm_password=confirm_password,
                                       subjects=subjects, quali=quali,exper=exper, first=first,last=last,father=father,age=age, village=village,city=city,state=state)

      val = valid_password(password)
      if val != True:
         return render_template("teacherform.html", error = val,
                                       username=username, phone=phone, password=password, confirm_password=confirm_password,
                                       subjects=subjects, quali=quali,exper=exper, first=first,last=last,father=father,age=age, village=village,city=city,state=state)


      if confirm_password != password:
         return render_template("teacherform.html", error = "passwords do not match",
                                       username=username, phone=phone, password=password, confirm_password=confirm_password,
                                       subjects=subjects, quali=quali,exper=exper, first=first,last=last,father=father,age=age, village=village,city=city,state=state)



      if not first or not last or not father or not age or not village or not city or not state or not subjects:
         return render_template("teacherform.html", error = "please fill the entire form ",
                                       username=username, phone=phone, password=password, confirm_password=confirm_password,
                                       subjects=subjects, quali=quali,exper=exper, first=first,last=last,father=father,age=age, village=village,city=city,state=state)

      if len(phone) != 10:
         return render_template("teacherform.html", error = "please fill the entire form ",
                                       username=username, phone=phone, password=password, confirm_password=confirm_password,
                                       subjects=subjects, quali=quali,exper=exper, first=first,last=last,father=father,age=age, village=village,city=city,state=state)

      db.execute("INSERT INTO tusers (username, phone, password) VALUES(?,?,?)",username, phone, generate_password_hash(password, "sha256"))
      current_id = db.execute("SELECT id FROM tusers WHERE username = ?",username)
      db.execute("INSERT INTO tacad (userID,subject, qualifications, experience) VALUES(?,?,?,?)",current_id[0]["id"],subjects, quali,exper)
      db.execute("INSERT INTO tper (userID,first, last, father, age, gender) VALUES(?,?,?,?,?,?)",current_id[0]["id"],first, last,father,age,gender)
      db.execute("INSERT INTO tadd (userID,village, city, state) VALUES(?,?,?,?)",current_id[0]["id"],village.strip("village,-, VILLAGE,Village ").lower()
                                                                                                                  , city,state)
      return redirect('/tlogin')

@app.route('/alogin')
def alogin():
   return render_template("sign.html")

@app.route('/slogin', methods=['GET','POST'])
def slogin():

   session.clear()
   if request.method == 'GET':
      return render_template("stdlogin.html")
   else:
      username = request.form.get("username")
      password = request.form.get("pass")
      if not username:
         return render_template("stdlogin.html", error="please enter a username")
      if not password:
         return render_template("stdlogin.html", error = "please enter your password")

      data = sb.execute("SELECT * FROM susers WHERE username = ?", username)
      if len(data) != 1 :
         return render_template("stdlogin.html", error = "invalid username")

      if not check_password_hash(data[0]["password"], password):
         return render_template("stdlogin.html", error = "invalid password", username=username)

      session["user_id"] = data[0]["userID"]
      return redirect('/home')

@app.route('/tlogin', methods=['GET','POST'])
def tlogin():
   session.clear()
   if request.method == 'POST':
      username = request.form.get("username")
      password = request.form.get("pass")

      if not username or not password:
         return render_template("tlogin.html",error = "Please enter a valid username or password", username = username)

      data = db.execute("SELECT * FROM tusers WHERE username = ?",username)
      if len(data) != 1 :
         return render_template("tlogin.html", error = "Invalid Username")
      if not check_password_hash(data[0]["password"], password):
         return render_template("tlogin.html", error = "Invalid password")
      session["user_id"] = data[0]["id"]
      return redirect('/home')
   else:
      return render_template('tlogin.html')

@app.route('/tprofile', methods=['GET','POST'])
def tprofile():
   if request.method == 'POST':
      first = request.form.get("first")
      last = request.form.get("last")
      phone = request.form.get("phone")
      # current_password = request.form.get("cupass")
      confirm_password = request.form.get("cpass")
      password = request.form.get("pass")
      subjects = request.form.get("subject")
      quali = request.form.get("qualifications")
      exper = request.form.get("exper")
      father = request.form.get("father")
      gender = request.form.get("radio")
      age = request.form.get("age")
      village = request.form.get("village")
      city = request.form.get("city")
      state = request.form.get("state")
      if first:
         db.execute("UPDATE tper SET first = ? WHERE userID = ? ",first,session["user_id"])
      if last:
         db.execute("UPDATE tper SET last = ? WHERE userID = ? ",last,session["user_id"])
      if subjects:
         db.execute("UPDATE tacad SET subject= ? WHERE userID = ? ",subjects,session["user_id"])
      if quali:
         db.execute("UPDATE tacad SET qualifications = ? WHERE userID = ? ",quali,session["user_id"])
      if father:
         db.execute("UPDATE tper SET father = ? WHERE userID = ? ",father,session["user_id"])
      if village:
         db.execute("UPDATE tadd SET village = ? WHERE userID = ? ",village,session["user_id"])
      if city:
         db.execute("UPDATE tadd SET city = ? WHERE userID = ? ",city,session["user_id"])
      if state:
         db.execute("UPDATE tadd SET state = ? WHERE userID = ? ",state,session["user_id"])
      if exper:
         db.execute("UPDATE tacad SET experience = ? WHERE userID = ? ",exper,session["user_id"])
      if age:
         db.execute("UPDATE tper SET age = ? WHERE userID = ? ",age,session["user_id"])
      if gender:
         db.execute("UPDATE tper SET gender = ? WHERE userID = ? ",gender,session["user_id"])
      if len(phone) != 10:
         return render_template('tprofile.html', error = "Plese enter a valid phone number")
      if phone:
         db.execute("UPDATE tusers SET phone = ? WHERE id = ? ",phone,session["user_id"])

      # text_data = db.execute("""SELECT first,last,subject,qualifications,father,village,city,state
      #                   FROM tper JOIN tadd ON tper.userID = tadd.userID
      #                   JOIN tacad ON tper.userID = tacad.userID
      #                   JOIN tusers ON tusers.id = tper.userID
      #                   WHERE tusers.id = ?""",'4')
      # num_data = db.execute("""SELECT phone,experience,age,gender
      #                   FROM tper JOIN tadd ON tper.userID = tadd.userID
      #                   JOIN tacad ON tper.userID = tacad.userID
      #                   JOIN tusers ON tusers.id = tper.userID
      #                   WHERE tusers.id = ?""",'4')


      # text = text_data[0]
      # num = num_data[0]

      # return render_template("tprofile.html",data = text, num = num )
      return redirect('/tprofile')
   else:

      text_data = db.execute("""SELECT first,last,subject,qualifications,father,village,city,state
                        FROM tper JOIN tadd ON tper.userID = tadd.userID
                        JOIN tacad ON tper.userID = tacad.userID
                        JOIN tusers ON tusers.id = tper.userID
                        WHERE tusers.id = ?""",'4')

      num_data = db.execute("""SELECT phone,experience,age,gender
                        FROM tper JOIN tadd ON tper.userID = tadd.userID
                        JOIN tacad ON tper.userID = tacad.userID
                        JOIN tusers ON tusers.id = tper.userID
                        WHERE tusers.id = ?""",'4')


      text = text_data[0]
      num = num_data[0]

      return render_template("tprofile.html",text = text, num = num )

@app.route('/home')
@login_required
def home():
   return render_template("home.html")

@app.route('/find', methods=['GET','POST'])
@login_required
def find():
   if request.method == 'POST':
      fname = request.form.get("tname")
      lname = request.form.get("lname")
      subject = request.form.get("tsubject")
      place = request.form.get("tplace")
      if fname or lname or subject or place:
         # per_data = db.execute("SELECT * FROM tper WHERE first LIKE ? AND last LIKE ?"
         datas = db.execute("""SELECT first,last,phone,subject,village,city,state
                        FROM tper JOIN tadd ON tper.userID = tadd.userID
                        JOIN tacad ON tper.userID = tacad.userID
                        JOIN tusers ON tusers.id = tper.userID
                        WHERE first LIKE ? AND last LIKE ? AND village LIKE ? AND subject LIKE ? """,
                        "%" + fname + "%","%" + lname + "%","%" + place + "%","%" + subject + "%")
      return render_template("find.html" ,fname = fname,lname = lname,subject = subject, place = place, datas = datas )
   else:
      return render_template("find.html")
# current_id = db.execute("SELECT id FROM tusers WHERE username ='kaali' ")
# print(current_id[0]["id"])
def valid_password(password):
   spl_char = ['@','#','%','^','&','*','(',')','_','+','=','-','!','/','`','~']
   if len(password) < 8 or len(password) > 25:
      string = "length of password must be between 8 and 25"
      return string
   if not any(char.isdigit() for char in password):
      string = "password must contain a digit"
      return string
   if not any(char.isupper() for char in password):
      string = "Password must contain upper digit"
      return string
   if not any(char in spl_char for char in password):
      string = "password must contain a special character"
      return string

   return True
