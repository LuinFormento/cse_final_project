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


@app.route("/edit/<int:client_id>", methods=["GET", "POST"])
def edit_client(client_id):
    cur = mysql.connection.cursor()
    
    if request.method == "POST":
        new_client_name = request.form["new_client_name"]
        new_client_from_date = request.form["new_client_from_date"]
        new_kpi_avg_billable_rate = request.form["new_kpi_avg_billable_rate"]
        new_kpi_billing_to_date = request.form["new_kpi_billing_to_date"]
        new_kpi_client_project_count = request.form["new_kpi_client_project_count"]
        
        cur.execute("""
            UPDATE clients 
            SET 
                client_name = %s, 
                client_from_date = %s, 
                kpi_avg_billable_rate = %s, 
                kpi_billing_to_date = %s, 
                kpi_client_project_count = %s 
            WHERE 
                client_id = %s
        """, (
            new_client_name,
            new_client_from_date,
            new_kpi_avg_billable_rate,
            new_kpi_billing_to_date,
            new_kpi_client_project_count,
            client_id
        ))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('show_clients'))
    
    # Fetch existing client details to pre-fill the edit form
    cur.execute("SELECT * FROM clients WHERE client_id = %s", (client_id,))
    client_data = cur.fetchone()
    cur.close()
    
    return render_template('edit.html', client=client_data)

@app.route("/delete/<int:client_id>")
def delete_client(client_id):
    cur = mysql.connection.cursor()
    
    cur.execute("DELETE FROM clients WHERE client_id = %s", (client_id,))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('show_clients'))

@app.route("/clients/<int:client_id>")
def show_single_client(client_id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM clients WHERE client_id = %s", (client_id,))
    client_data = cur.fetchone()
    cur.close()

    return render_template('single_client.html', client=client_data)

@app.route("/clients/<string:client_name>")
def show_single_client_by_name(client_name):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM clients WHERE client_name = %s", (client_name,))
    client_data = cur.fetchone()
    cur.close()

    return render_template('single_client.html', client=client_data)

if __name__ == "__main__":
    app.run(debug=True)

