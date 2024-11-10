from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb.default.svc.cluster.local:27017")
client = MongoClient(mongo_uri)
db = client.health_records
records_collection = db.records

@app.route('/records', methods=['POST'])
def add_record():
    data = request.json
    record_id = records_collection.insert_one(data).inserted_id
    return jsonify({"status": "Record added", "record_id": str(record_id)}), 201

@app.route('/records/<patient_id>', methods=['GET'])
def get_records(patient_id):
    records = records_collection.find({"patient_id": patient_id})
    # Convert each record to make `_id` JSON serializable
    serialized_records = []
    for record in records:
        record['_id'] = str(record['_id'])  # Convert ObjectId to string
        serialized_records.append(record)
    return jsonify(serialized_records), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
