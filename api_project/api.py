from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "11082017"
app.config["MYSQL_DB"] = "employees_fees"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

def data_fetch(query):
    cur = mysql.connection.cursor()
    query = """
        select * from clients"""

    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/")
def home_page():
    return render_template('home.html')


@app.route("/clients", methods=["GET"])
def show_clients():
    clients_data = data_fetch("""select * from clients""")
    return render_template('clients.html', clients=clients_data)

@app.route("/add")
def add_client():
    return render_template('add.html')

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        client_name = request.form["client_name"]
        client_from_date = request.form["client_from_date"]
        kpi_avg_billable_rate = request.form["kpi_avg_billable_rate"]
        kpi_billing_to_date = request.form["kpi_billing_to_date"]
        kpi_client_project_count = request.form["kpi_client_project_count"]


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO clients (client_name, client_from_date, kpi_avg_billable_rate, kpi_billing_to_date, kpi_client_project_count) VALUES (%s, %s, %s, %s, %s)", (client_name, client_from_date, kpi_avg_billable_rate, kpi_billing_to_date, kpi_client_project_count))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('show_clients'))

# @app.route("/clients", methods=["GET"])
# def get_clients():
#     data = data_fetch("""select * from clients""")
#     return make_response(jsonify(data), 200)

# @app.route("/clients/<int:id>", methods=["GET"])
# def get_client_by_id(id):
#     data = data_fetch("""SELECT * FROM clients where client_id= {}""".format(id))
#     return make_response(jsonify(data), 200)

# @app.route("/clients/<int:id>/clientaddress", methods=["GET"])
# def get_client_address_by_client(id):
#     data = data_fetch(
#         """
#     SELECT line1_number_building, line2_number_street, line3_area_locality, town_city, state_province, country_code
#         FROM clients
#         INNER JOIN client_addresses
#         ON clients.client_id = client_addresses.client_id 
#         INNER JOIN addresses
#         ON client_addresses.address_id = addresses.address_id 
#         WHERE clients.client_id = {}
#     """.format(
#             id
#         )
#     )
#     return make_response(
#         jsonify({"client_id": id, "count": len(data), "client's address": data}), 200
#     )

if __name__ == "__main__":
    app.run(debug=True)

