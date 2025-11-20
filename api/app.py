#!/usr/bin/env python3
import json
import os
import boto3
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from resume_parser import parse_resume
from flask_cors import CORS

def load_bucket():
    try:
        with open("/etc/resume_bucket_name", "r") as f:
            return f.read().strip()
    except:
        return None


S3_BUCKET = load_bucket()
s3_client = boto3.client('s3')

app = Flask(__name__)
CORS(app) # enables Cross-Origin Resource Sharing (CORS) 

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    
    try:
        file_path = f"/tmp/{filename}"
        file.save(file_path)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    try:
        parsed_data = parse_resume(file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to parse resume: {str(e)}"}), 400

    s3_key = f"resumes/{os.path.splitext(filename)[0]}.json"
    s3_client.put_object(
        Bucket=S3_BUCKET, 
        Key=s3_key, 
        Body=json.dumps(parsed_data).encode("utf-8"), #Body parameter requires a bytes object
        ContentType="application/json" # for S3 to know it contains valid JSON
        )

    return jsonify({'status': 'success', 's3_key': s3_key})

