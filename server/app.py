import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

from firebase_admin import credentials, firestore, initialize_app

# Initialize Firestore DB
cred = credentials.Certificate('/Users/dariuszkorzun/Documents/GitHub/bigdatacampv1/bigdatacampdb-10512eaf8a21.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('bigdataproducts')
dictionary_ref = db.collection('dictionary').document(u'bigdataproducts')

Products = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def remove_product(product_id):
    for product in Products:
        if product['id'] == product_id:
            Products.remove(product)
            return True
    return False


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/products', methods=['GET', 'POST'])
def products():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        Products.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Product added!'
        return jsonify(response_object)
    else:
        #response_object['products'] = Products
        documents = todo_ref.stream()
        all_todos = {}
        for doc in documents:
            all_todos[doc.id] = doc.to_dict()
        print(all_todos)
        return jsonify(all_todos), 200

@app.route('/dictionaries', methods=['GET', 'POST'])
def dictionaries():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        Products.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Product added!'
        return jsonify(response_object)
    else:
        #response_object['products'] = Products
        documents = dictionary_ref.get()
        #all_dictionaries = {}
        #for doc in documents:
        #    all_dictionaries[doc.id] = doc.to_dict()
        print(f'{documents.to_dict()}')
        return (f'{documents.to_dict()}')

@app.route('/products/<product_id>', methods=['PUT', 'DELETE'])
def single_product(product_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_product(product_id)
        Products.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Product updated!'
    if request.method == 'DELETE':
        remove_product(product_id)
        response_object['message'] = 'Product removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
