from cs50 import SQL

db = SQL("sqlite:///stddata.db")

first = ""
last ="SiNgH"
data = db.execute("SELECT * FROM sper WHERE last LIKE ?",last)
# db.execute("INSERT INTO sper(perID,first, last,father) VALUES(?,?,?,?)","2","mr. khush","mr. singh","mr jaspal" )
print(data)