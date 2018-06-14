from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
import fabric

app = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.empData

@app.route('/addEmployee', methods = ['POST'])
def addEmployee():
    try:
        json_data = request.json['info']
        empId = json_data['empId']
        empName = json_data['name']
        empAge = json_data['age']
        empGender = json_data['gender']

        db.Employees.insert_one(
            {
            'empId': empId,
            'name':empName,
            'age':empAge,
            'gender':empGender
            })

        return jsonify(status='OK',message='Inserted successfully')

    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@app.route('/')
def showIndex():
    return render_template('index.html')

@app.route('/getEmployee', methods=['POST'])
def getEmployee():
    try:
        employeeId = request.json['id']
        employee = db.Employees.find_one({'_id':ObjectId(employeeId)})
        employeeDetail = {
                'empId':employee['empId'],
                'name':employee['name'],
                'age':employee['age'],
                'gender':employee['gender'],
                'id':str(employee['_id'])
                }
        return json.dumps(employeeDetail)
    except Exception, e:
        return str(e)

@app.route('/updateEmployee',methods=['POST'])
def updateEmployee():
    try:
        employeeInfo = request.json['info']
        employeeId = employeeInfo['id']
        empId = employeeInfo['empId']
        name = employeeInfo['name']
        age = employeeInfo['age']
        gender = employeeInfo['gender']

        db.Employees.update_one({'_id':ObjectId(employeeId)},{'$set':{'empId':empId, 'name':name,'age':age,'gender':gender}})
        return jsonify(status='OK',message='Updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@app.route("/getEmployeeList",methods=['POST'])
def getEmpList():
    try:
        employees = db.Employees.find()

        employeeList = []
        for employee in employees:
            print employee
            employeeItem = {
                    'empId':employee['empId'],
                    'name':employee['name'],
                    'age':employee['age'],
                    'gender':employee['gender'],
                    'id': str(employee['_id'])
                    }
            employeeList.append(employeeItem)
    except Exception,e:
        return str(e)
    return json.dumps(employeeList)

@app.route("/deleteEmployee",methods=['POST'])
def deleteEmployee():
    try:
        employeeId = request.json['id']
        db.Employees.remove({'_id':ObjectId(employeeId)})
        return jsonify(status='OK',message='Deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

if __name__ == "__main__":
    app.run(debug = True)
