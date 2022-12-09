from flask import  Flask,jsonify, abort, make_response,redirect,request, url_for
from flask_httpauth  import HTTPBasicAuth
auth =HTTPBasicAuth()
app = Flask(__name__)

task = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@auth.get_password
def get_password(username):
    if username == 'username':
        return 'password'
    return None


@auth.error_handler
def notaut():
    return make_response(jsonify('Error, False to log in'),401)


@app.route('/')
def main():
    return 'Work'

@app.route('/takev', methods=['GET'])
@auth.login_required
def takev():
    return jsonify(task)


@app.route('/task/<int:id>', methods=['GET'])
def takeId(id):
    for el in task:
        if el['id'] == id:
            return jsonify(el)
    abort(404)

@app.errorhandler(404)
def notFound(error):
    return make_response('Error',404)


@app.route('/add/<string:title>/<string:description>/<int:done>',methods=['POST'])
def Add(title,description,done):
    try:
        task.append(
            {
                'id': task[-1]['id'] + 1,
                'title':title,
                'description':description,
                'done': True if done ==1 else False
            }
        )
    except Exception as E:
        return make_response(E,404)
    return jsonify(task),201


@app.route('/add',methods=['POST'])
def addJ():
    if not request.json or not 'title' in request.json:
        abort(400)
    task.append(
        {
            'id':task[-1]['id'] + 1,
            'title':request.json['title'],
            'description':request.json.get('description',''),
            'done':False

        }
    )
    return jsonify(task),201


@app.route('/remove/<int:id>',methods=['DELETE'])
def remove(id):
    try:
        for i in task:
            if i['id'] == id:
                task.remove(i)
    except:
        abort(404)
    return jsonify(task)


@app.route('/update/<int:id>',methods=['PUT'])
def update(id):
    for i in task:
        if i['id'] == id:
            i['title'] = request.json['title']
            i['description'] = request.json['description']
    return jsonify(task)


@app.route('/accept/<int:id>', methods=['PUT'])
def accept(id):
    for i in task:
        if i['id'] == id:
            i['done'] = True
    return jsonify(task)

if __name__=='__main__':
    app.run(debug=True)