from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
db = SQL("sqlite:///data.db")

fname = "khushwinder"
lname = ""
place = ""
subject = ""
# datas = db.execute("""SELECT first,last,phone,subject,village,city,state
#                         FROM tper JOIN tadd ON tper.userID = tadd.userID
#                         JOIN tacad ON tper.userID = tacad.userID
#                         JOIN tusers ON tusers.id = tper.userID
#                         WHERE username ='khush@web'""")
datas = db.execute("""SELECT experience,age,phone,gender
                        FROM tper JOIN tadd ON tper.userID = tadd.userID
                        JOIN tacad ON tper.userID = tacad.userID
                        JOIN tusers ON tusers.id = tper.userID
                        WHERE tusers.id = ?""",'1')
# data = db.execute("""SELECT first,last,phone,subject,village,city,state
#                         FROM tper JOIN tadd ON tper.userID = tadd.userID
#                         JOIN tacad ON tper.userID = tacad.userID
#                         JOIN tusers ON tusers.id = tper.userID
#                         WHERE first LIKE ? AND last LIKE ? AND village LIKE ? AND subject LIKE ? """,
#                         "%" + fname + "%","%" + lname + "%","%" + place + "%","%" + subject + "%")
# data = db.execute('SELECT * FROM sper WHERE last LIKE '%{?}%'',last)
# db.execute("INSERT INTO sper(perID,first, last,father) VALUES(?,?,?,?)","2","mr. khush","mr. singh","mr jaspal" )
# query = """SELECT * FROM sper WHERE last LIKE %?%"""
# data = db.execute(query, last)
# patter = "%{0}%".format(first)
# cursor.execute("SELECT LastName FROM contacts WHERE phone LIKE %s", (pattern,))
# data = db.execute(
#     "SELECT * FROM sper WHERE first LIKE ? AND last LIKE ? ",
#     ("%{}%".format(first),),("%{}%".format(last),)
# for row in data:
#     print(row["first"])

print(datas[0])
# data = datas[0]
# for key in data:
    # print(key)
    
# age = 12.0
# if int(age) <13:
#     print(age)
    


# db.execute('SELECT * FROM sper WHERE last LIKE '%?%', (last,))

# password = generate_password_hash('12345',"sha256")
# print(check_password_hash('12345','sha256$HY3FqzVw$7cb16e4233778fdfdf57160b5fd75af223a1f43da7041a6cf72e61bf65439caa'))
