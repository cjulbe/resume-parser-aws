#!/usr/bin/env python3
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
    file_path = f"/tmp/{filename}"
    file.save(file_path)

    parsed_data = parse_resume(file_path)

    # Clean up temp file
    if os.path.exists(file_path):
        os.remove(file_path)

    s3_key = f"resumes/{os.path.splitext(filename)[0]}.json"
    s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=str(parsed_data))

    return jsonify({'status': 'success', 's3_key': s3_key})

