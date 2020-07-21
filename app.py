from flask import Flask, render_template,url_for,request,jsonify
import pymysql,pymysql.cursors
import flask
from des import DesKey
import hashlib



app=Flask(__name__)



KEY="workindi"
key=DesKey(KEY.encode("utf-8"))

@app.route('/')
def index():
    return "Workindia Assesment"




@app.route('/app/agent',methods=["POST"])
def app_agent():
    if(flask.request.method=="POST"):
        try:
            connection=pymysql.connect(host='localhost',user='root',password='',db='workindia')
            cursor=connection.cursor()
            sql="insert into agents values (%s,%s)"
            passwd = str(hashlib.md5(request.form["password"].encode()).hexdigest())
            cursor.execute(sql,(request.form["agent_id"],passwd))
            connection.commit() 
            d={"status":"Account Created"}
            return jsonify(Response_Data=d),200
        except:
            d={"status":"Failed"}
            return jsonify(Response_Data=d),400
        
    



@app.route('/app/agent/auth',methods=["POST"])
def app_agent_auth():
    try:
        connection=pymysql.connect(host='localhost',user='root',password='',db='workindia')
        cursor=connection.cursor()
        passwd = str(hashlib.md5(request.form["password"].encode()).hexdigest())
        sql = "select * from agents where id=%s and passwd=%s"
        cursor.execute(sql,(request.form["agent_id"],passwd))
        result = list(cursor.fetchall())
        if(len(result)==0):
            d={"status":"Failure"}
            return jsonify(d),401
        else:
            d={"status":"success","agent_id":result[0][0]}
            return jsonify(Response_data=d),200
    except:
        d={"status":"Failure"}
        return jsonify(Response_data=d),401
        





@app.route('/app/sites/list',methods=["GET"])
def app_sites_list():
    connection=pymysql.connect(host='localhost',user='root',password='',db='workindia')
    cursor=connection.cursor()
    agent_id=request.args["agentid"]
    sql = "select * from todo where id=%s order by due_date"
    cursor.execute(sql,(agent_id))
    columns = cursor.description 
    result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
    return jsonify(result)
    
     



   
@app.route('/app/sites',methods=["POST"])
def app_sites():
    try:
        connection=pymysql.connect(host='localhost',user='root',password='',db='workindia')
        cursor=connection.cursor()
        agent_id=request.args["agentid"]
        sql = "insert into todo values (%s,%s,%s,%s,%s)"
        cursor.execute(sql,(agent_id,request.form["title"],request.form["description"],request.form["category"],request.form["due_date"]))
        connection.commit()
        d={"status":"success"}
        return jsonify(d),200
    except:
        d={"status":"failure"}
        return jsonify(d),401
 
    
    
if __name__=="__main__":
    app.run(use_reloader=False,debug=True)