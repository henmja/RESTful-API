!pip install psycopg2
!pip install flask
!pip install flask_restful

import psycopg2
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

#Opprett bruker:
def createUser(cur, userID, userName, mail, pw):
    cur.execute("""INSERT INTO "Users" (id, brukernavn, epost, passord) VALUES (%s, %s, %s, %s)""",(str(userID), userName, mail, pw))

#Hent spesifikk bruker:
#def getUser(cur, userID):
#    cur.execute('select * from "Users" where id = %s',(str(userID)))

#Slett spesifikk bruker:
def delUser(cur, userID):
    cur.execute('DELETE FROM "Users" WHERE id = %s',(str(userID)))

#Hent alle brukere:
def getAll(cur):
    cur.execute('select * from "Users"')

def main():
    conn = psycopg2.connect("dbname=UserDB user=postgres password=test")

    cur = conn.cursor()

    class CreateUser(Resource):
        def post(self):
            par = request.get_json()
            createUser(cur,par[0], par[1], par[2], par[3])
            return {'you sent': par}, 201

    class DelUser(Resource):
        def post(self,num):
            par = request.get_json()
            delUser(cur,int(par))
            return {'Deleted user number ':num}, 201

    class Users(Resource):
        def get(self):
            getAll(cur)
            rows = cur.fetchall()
            return rows

    class UserID(Resource):
        def get(self,num):
            getAll(cur)
            rows = cur.fetchall()
            i = 0
            for row in rows:
                if row[0]==num:
                    return row
                else:
                    if i==len(rows)-1:
                        return 'Non-existent user!'
                i+=1
    api.add_resource(CreateUser, '/users')
    api.add_resource(Users, '/users')
    api.add_resource(UserID, '/users/<int:num>')
    api.add_resource(DelUser, '/users/<int:num>')
    app.run(debug=False)

    cur.close()

    conn.close()

if __name__ == "__main__":
    main()