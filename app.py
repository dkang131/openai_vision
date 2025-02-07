from flask import Flask, request, jsonify
import json, os, uuid
from vision.upload_vision import describing_image


app = Flask(__name__)

@app.route('/vision_desc', methods = ['POST'])

def vision_desc():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    print(request.files)

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    unique_id = uuid.uuid4() 
    filename_base = os.path.splitext(file.filename)[0]  
    output_filename = f"{filename_base}_{unique_id}.json"

    if file.filename.lower().endswith(('.png','.jpg','.jpeg')):
        image_path = f"temp_statement_{unique_id}.png"
        file.save(image_path)
        describing_result_json = describing_image(image_path)
        os.remove(image_path)
    else:
        return jsonify ({"error": "Unsupported file type. Please upload a PNG, JPG, or PDF."}), 400
    
    if not describing_result_json:
        return jsonify ({"error": "Failed to analyze image with OpenAI Vision"}), 500
    
    try:
        describing_result = json.loads(describing_result_json)
    except json.JSONDecodeError:
        return jsonify ({"error": "Invalid JSON from OpenAI Vision"}), 500
    
    try:
        with open(output_filename, "w") as f:
            json.dump(describing_result, f, indent=4)
        return jsonify ({"message": f"Image processed successfully. Data saved to {output_filename}"}), 200
    except Exception as e:
        print (f"Error saving to JSON file: {e}")
        return jsonify({"error": f"Failed to save data to JSON file: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)