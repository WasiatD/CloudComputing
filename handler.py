from firebaseconfig import db
from pydantic import BaseModel
from typing import Optional
import datetime
import pytz


def add_data(user, data):
    try:
        flag = db.collection('user').document(user).collection('IOT').document(data['id'])
        flag = flag.get().to_dict()
        print(flag)
        if flag is not None:
            db.collection('user').document(user).collection('IOT').document(data['id']).collection('data').document('data').set({'suhu':data['suhu'], 'cahaya':data['cahaya'], 'kelembapan':data['kelembapan'], 'relay':data['relay']})
        else:
            db.collection('user').document(user).collection('IOT').document(data['id']).set({'nama':data['id']})
            db.collection('user').document(user).collection('IOT').document(data['id']).collection('data').document('data').set({'suhu':data['suhu'], 'cahaya':data['cahaya'], 'kelembapan':data['kelembapan'], 'relay':data['relay']})
    except Exception as e:
        raise e
    
class UpdateDataModel(BaseModel):
    id: str
    nama: Optional[str] = None
    lokasi: Optional[str] = None
    deskripsi: Optional[str] = None

def update_data(user, data: UpdateDataModel):
    try:
        doc_ref = db.collection('user').document(user).collection('IOT').document(data.id)

        update_data = {}
        if data.nama is not None:
            update_data['nama'] = data.nama
        if data.lokasi is not None:
            update_data['lokasi'] = data.lokasi
        if data.deskripsi is not None:
            update_data['deskripsi'] = data.deskripsi

        if update_data:
            doc_ref.update(update_data)
        else:
            raise Exception('No data to update')
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

def get_dataById(user, id):
    try:
        doc = db.collection('user').document(user).collection('IOT').document(id).collection('data').document('data')
        doc = doc.get()
        return doc.to_dict()
    except Exception as e:
        raise e

def get_profile(user,id):
    try:
        doc = db.collection('user').document(user).collection('IOT').document(id).collection('data').document('profile')
        data = doc.get()
        return data.to_dict()
    except Exception as e:
        raise e
    
# add data for notes (post)
def add_notes(user, data):
    try:
        utc = datetime.datetime.now(pytz.utc)

        data['date'] = utc.astimezone(pytz.timezone('Asia/Jakarta')).strftime('%Y-%m-%d %H:%M:%S')

        db.collection('user').document(user).collection('notes').document(data['id']).set({'title':data['title'], 'content':data['content'], 'date':data['date']})
    except Exception as e:
        raise e
    
# get notes data
def get_notes(user):
    try:
        collection_ref = db.collection('user').document(user).collection('notes')
        docs = collection_ref.stream()
        isi = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id
            isi.append(doc_data)

        return isi
    except Exception as e:
        raise e
    
# delete notes
def delete_notes(user, id):
    try:
        db.collection('user').document(user).collection('notes').document(id).delete()
    except Exception as e:
        raise e