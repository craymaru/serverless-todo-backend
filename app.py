from chalice import Chalice

app = Chalice(app_name='serverless-todo-backend')


@app.route('/')
def index():
    return {'hello': 'world'}
