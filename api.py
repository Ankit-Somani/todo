from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import csv

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API', 'status': 'Incomplete'},
    'todo2': {'task': '?????', 'status': 'Incomplete'},
    'todo3': {'task': 'profit!', 'status': 'Incomplete'},
}

fields = ['task', 'status'] 
csv_file = "todo.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for data in TODOS:
            writer.writerow(data)
except IOError:
    print("I/O error")
    

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('status', type=int)



# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        # task = {'task': args['task']}
        TODOS[todo_id]['task'] = args['task']
        return TODOS[todo_id], 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task'], 'status': 'Incomplete'}
        
        return TODOS[todo_id], 201

class Status(Resource):
    def get(self, todo_id):
        return TODOS[todo_id]['status'], 201
    
    def put(self, todo_id):
        args = parser.parse_args()
        # task = {'task': args['task']}
        if(args['status']):
            TODOS[todo_id]['status'] = 'Complete'
        else:
            TODOS[todo_id]['status'] = 'Incomplete'
        return TODOS[todo_id], 201
##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(Status, '/todos/<todo_id>/status')

if __name__ == '__main__':
    app.run(debug=True)