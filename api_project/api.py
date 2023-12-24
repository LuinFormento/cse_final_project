from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "11082017"
app.config["MYSQL_DB"] = "employees_fees"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/clients", methods=["GET"])
def get_clients():
    data = data_fetch("""select * from clients""")
    return make_response(jsonify(data), 200)

@app.route("/clients/<int:id>", methods=["GET"])
def get_client_by_id(id):
    data = data_fetch("""SELECT * FROM clients where client_id= {}""".format(id))
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)