from flask import Flask,jsonify,request
import psycopg2
import socket,sys

#get host details, 
HOST = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST)

#get connection to db
PG_USER = "postgres"
PG_PASSWORD = "postgres"

#delete the emp_table and create a new one. 
conn = psycopg2.connect("host=db user={0} password={1}".format(PG_USER,PG_PASSWORD))
cur = conn.cursor()

cur.execute("CREATE TABLE empl (id serial PRIMARY KEY, emp_name varchar, age integer, designation varchar);")
cur.close()


#Create a flask app
f_app = Flask('__name__')

#GET employees

@f_app.route('/employees/',methods=['GET'])
def get_all_employees():
    print("hello")
    emps_cur = conn.cursor()
    emps_cur.execute("SELECT * FROM empl")
    res_tup = emps_cur.fetchall()
    emps_cur.close()
    
    return jsonify({"result":res_tup})
    

#GET an employee
@f_app.route("/employees/<string:emp_name>/",methods=['GET'])
def get_emp_det(emp_name):
    emps_cur = conn.cursor()
    emps_cur.execute("SELECT * FROM empl WHERE id='{0}'".format(emp_name))
    res_tup = emps_cur.fetchall()

    return jsonify({'result':res_tup})

#POST an emp, taking only three attributes of an employee

@f_app.route("/emp_add/",methods=['POST'])
def add_emp():
    req_data = request.get_json()
    n_emp_name = req_data["emp_name"]
    n_emp_age = int(req_data["age"])
    n_emp_desg = req_data["designation"]

    emps_cur = conn.cursor()
    emps_cur.execute("INSERT INTO empl (emp_name,age,designation) VALUES (%s,%s,%s)",(n_emp_name,n_emp_age,n_emp_desg))
    emps_cur.execute("SELECT * FROM empl WHERE emp_name='{0}'".format(n_emp_name))
    res_tup = emps_cur.fetchall()
    emps_cur.close()
    if len(res_tup) != 0:
        return jsonify({"result":res_tup})
    else:
        return jsonify({"result":"POST failed"})

#PUT/UPDATE an emp
@f_app.route("/emp_update/<string:e_id>",methods=['PUT'])
def update_emp_det(e_id):
    req_data = request.get_json()
    n_emp_id = e_id
    n_emp_name = req_data["emp_name"]
    n_emp_age = int(req_data["age"])
    n_emp_desg = req_data["designation"]

    emps_cur = conn.cursor()
    emps_cur.execute("SELECT * FROM empl WHERE id='{0}'".format(n_emp_id))
    res_tup = emps_cur.fetchall()
    if res_tup:
        emps_cur.execute("UPDATE empl SET emp_name = '{0}',age = {1},designation = '{2}' WHERE id={3}".format(n_emp_name,n_emp_age,n_emp_desg,n_emp_id))
        emps_cur.execute("SELECT * FROM empl WHERE id='{0}'".format(n_emp_id))
        f_res = emps_cur.fetchall()
        
        return jsonify({"result":f_res})

    else:
        emps_cur.execute("INSERT INTO empl (emp_name,age,designation) VALUES (%s,%s,%s)",(n_emp_name,n_emp_age,n_emp_desg))
        emps_cur.execute("SELECT * FROM empl WHERE emp_name='{0}'".format(n_emp_name))
        f_res = emps_cur.fetchall()

        return jsonify({"result":f_res})
    

#DELETE an emp
@f_app.route("/emp_del/<string:e_id>",methods=['DELETE'])
def delete_emp(e_id):
    n_emp_id = e_id
    emps_cur = conn.cursor()
    emps_cur.execute("DELETE FROM empl WHERE id='{0}'".format(n_emp_id))

    return jsonify({"result":"Successfull Deleted"})




f_app.run(host=HOST_IP,port=5000)
