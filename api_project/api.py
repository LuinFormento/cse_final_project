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

@app.route("/clients", methods=["GET"])
def get_clients():
    cur = mysql.connection.cursor()
    query = """
        select * from clients"""

    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return make_response(jsonify(data), 10)

if __name__ == "__main__":
    app.run(debug=True)