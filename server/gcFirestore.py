##################################################
import sys
# Flask
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
# Date/Time parser
from datetime import datetime
from dateutil.parser import parse
# Google Cloud
from firebase_admin import credentials, firestore, initialize_app
##################################################

# Show detailed error description
DEBUG = True

# Google Cloud initialization
gcCredentials = credentials.Certificate( '/Users/dariuszkorzun/Documents/GitHub/bigdatacampv1/bigdatacampdb-10512eaf8a21.json' )
gcApplication = initialize_app( gcCredentials )
gcFirestore = firestore.client()
# Get reference to a collection
gcCollection = gcFirestore.collection( 'bigdataproducts' )

# Create an instance of Flask application
flaskApplication = Flask( __name__ )
flaskApplication.config.from_object( __name__ )

# Create response variable
responseData = {}
# ________________________________________________
# Register view functions

# DELETE Product from Firestore Database
# Accept only POST requests
@flaskApplication.route( '/documents/delete', methods=['POST'] )
def deleteProduct():
    # Read data passed from a web form
    requestData = request.get_json()
    # Get reference to a document in a collection and delete it
    # Returns deletion time that we assign to variable
    try:
        deletionTime = parse( gcCollection.document( requestData ).delete().ToJsonString() )
    except:
        responseData[ 'response' ] = 'Firestore connection error! \n' + str( sys.exc_info()[0] ) + '\n' + str( sys.exc_info()[1] )
    else:
        responseData[ 'response' ] = 'Product deleted!'
    # Send response back
    return jsonify( responseData )

# UPDATE Product in Firestore Database
# Accept only POST requests
@flaskApplication.route('/documents/update', methods=['POST'])
def updateProduct():
    # Read data passed from a web form
    requestData = request.get_json()
    # Get reference to a document in a collection and update its content
    try:
        gcCollection.document(requestData.get( 'productname' )).update({
            'fullname': requestData.get( 'fullname' ),
            'category':  requestData.get( 'category' ) if( isinstance(( requestData.get( 'category' )), list) == True ) else [  requestData.get( 'category' ) ],
            'subcategory': requestData.get( 'subcategory' ) if( isinstance(( requestData.get( 'subcategory' )), list) == True ) else [  requestData.get( 'subcategory' ) ],
            'type': requestData.get( 'type' ) if( isinstance(( requestData.get( 'type' )), list) == True ) else [  requestData.get( 'type' ) ],
            'developer': requestData.get( 'developer' ),
            'website': requestData.get( 'website' ),
            'documentation': requestData.get( 'documentation' ),
            'created': parse( requestData.get( 'created' ) ),
            'modified': firestore.SERVER_TIMESTAMP
        })
    except:
        responseData[ 'response' ] = 'Firestore connection error! \n' + str( sys.exc_info()[0] ) + '\n' + str( sys.exc_info()[1] )
        print("Unexpected error:", sys.exc_info()[0])
    else:
        responseData[ 'response' ] = 'Product updated!'
    # Send response back
    return jsonify( responseData )

# INSERT Product into Firestore Database
# Accept only POST requests
@flaskApplication.route( '/documents/add', methods=['POST'] )
def insertProduct():
    # Read data passed from a web form
    requestData = request.get_json()
    # Get reference to a document in a collection and update its content
    try:
        gcCollection.document(requestData.get( 'productname' )).set({
            'fullname': requestData.get( 'fullname' ),
            'category':  requestData.get( 'category' ) if( isinstance(( requestData.get( 'category' )), list) == True ) else [  requestData.get( 'category' ) ],
            'subcategory': requestData.get( 'subcategory' ) if( isinstance(( requestData.get( 'subcategory' )), list) == True ) else [  requestData.get( 'subcategory' ) ],
            'type': requestData.get( 'type' ) if( isinstance(( requestData.get( 'type' )), list) == True ) else [  requestData.get( 'type' ) ],
            'developer': requestData.get( 'developer' ),
            'website': requestData.get( 'website' ),
            'documentation': requestData.get( 'documentation' ),
            'created': firestore.SERVER_TIMESTAMP,
            'modified': firestore.SERVER_TIMESTAMP
        })
    except:
        responseData[ 'response' ] = 'Firestore connection error! \n' + str( sys.exc_info()[0] ) + '\n' + str( sys.exc_info()[1] )
    else:
        responseData[ 'response' ] = 'Product added!'
    # Send response back
    return jsonify( responseData )

# READ Products from Firestore Database
# Accept only GET requests
@flaskApplication.route('/documents', methods=['GET'])
def readProduct():
    response_object = {'status': 'success'}
    bigdataproducts = gcFirestore.collection('bigdataproducts')
    bigdatacategories = gcFirestore.collection(u'dictionary').document(u'bigdataproducts').get().to_dict()
    bdccategories =  bigdatacategories['category']
    bdcdeveloper = bigdatacategories['developer']

    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)

        #timeZone = { 'CEST' : gettz( 'Europe/Warsaw' )}

        bigdataproducts.document(post_data.get( 'productname' )).set({
            'fullname': post_data.get( 'fullname' ),
            'category':  post_data.get( 'category' ) if( isinstance(( post_data.get( 'category' )), list) == True ) else [  post_data.get( 'category' ) ],
            'subcategory': post_data.get( 'subcategory' ) if( isinstance(( post_data.get( 'subcategory' )), list) == True ) else [  post_data.get( 'subcategory' ) ],
            'type': post_data.get( 'type' ) if( isinstance(( post_data.get( 'type' )), list) == True ) else [  post_data.get( 'type' ) ],
            'developer': post_data.get( 'developer' ),
            'website': post_data.get( 'website' ),
            'documentation': post_data.get( 'documentation' ),
            'created': parse(post_data.get( 'created' )),
            'modified': parse(post_data.get( 'modified'))
            #'created': parse(post_data.get( 'created' ) + ' CET', tzinfos=timeZone),
            #'modified': parse(post_data.get( 'modified' ) + ' CET', tzinfos=timeZone)
        })

        response_object['message'] = 'Product added!'
        return jsonify(response_object)
    else:
        all_docs = {}
        bdpcategories = {}

        #for doc in bigdataproducts.list_documents():
            #print(type(doc))
            #print(doc.id, ' : ', doc.path)

        for doc in bigdataproducts.stream():
            all_docs[doc.id] = doc.to_dict()
            print(doc.id)

            coll = bigdataproducts.document(doc.id).collections()
            for collection in coll:
                for entry in collection.stream():
                    print( entry.id )
                    for key, value in entry.to_dict().items():
                        print(key, ' : ', value)
                        print('---')

            for key, value in doc.to_dict().items():
                print(key, ' : ', value)
                print('---')
        print(all_docs)
        return render_template('gcDocuments.html', all_docs=all_docs, bdccategories=bdccategories, bdcdeveloper=bdcdeveloper )

if __name__ == '__main__':
    flaskApplication.run(host='127.0.0.1')


#dictionary_ref = db.collection('dictionary').document(u'bigdataproducts')

# enable CORS
#CORS(app, resources={r'/*': {'origins': '*'}})

#bigdatacategories = db.collection(u'dictionary').document(u'bigdataproducts').get().to_dict()
#bdccategories =  bigdatacategories['category']
#bdcdeveloper = bigdatacategories['developer']
