from firebaseconfig import db


def add_data(user, id, data,timestamp):
    try:
        db.collection('user').document(user).collection('IOT').document(id).set({'id': id})
        db.collection('user').document(user).collection('IOT').document(id).collection('data').document(timestamp).set(data)
    except Exception as e:
        raise e

def add_prediction(user ,base64_str, predicted_class_name):
    try:
        db.collection('user').document(user).collection('prediction').add({
                'image': base64_str,
                'predicted_class': predicted_class_name
            })
    except Exception as e:
        raise e

def get_predictions(user):
    try:
        predictions = []
        docs = db.collection('user').document(user).collection('prediction').stream()
        for doc in docs:
            predictions.append(doc.to_dict())
        return predictions
    except Exception as e:
        raise e

def getListIot(user):
    try:
        collection_ref = db.collection('user').document(user).collection('IOT')
        docs = collection_ref.stream()
        isi = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id
            isi.append(doc_data)

        return isi
    except Exception as e:
        raise e

def get_data_by_id(user, id):
    try:
        doc = db.collection('user').document('user').collection('IOT').document(id).collection('data')
        docs = doc.stream()
        isi = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id
            isi.append(doc_data)

        return isi
    except Exception as e:
        raise e