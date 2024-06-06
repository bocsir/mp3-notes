from flask import Flask, request, jsonify
import os
import json
from getNotes import getNotes

app = Flask(__name__)

if not os.path.exists('uploads'):
    os.makedirs('uploads')

# bind function to URL endpoint
@app.route('/api/audio', methods=['POST'])
def process_audio():
    # check if a file was sent from client
    if 'file' not in request.files:
        return jsonify({'error': 'No file sent'}), 400
    
    # save file to uploads folder
    file = request.files['file']
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # send file path to conversion function to get notes, return to client
    try: 
        notes = getNotes(file_path)
        # ensure # not replaced with unicode
        response = app.response_class(
            response=json.dumps({'notes': notes}, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )
        return response    
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__': 
    app.run(debug=True, port=5000)