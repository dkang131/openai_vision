# app.py
from flask import Flask, request, jsonify
import json, os, uuid
from model.upload_vision import describing_image  # Corrected import

app = Flask(__name__)

@app.route('/vision_desc', methods=['POST'])
def vision_desc():
    """
    Handles image uploads and uses OpenAI Vision to describe the image.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    unique_id = uuid.uuid4()
    filename_base = os.path.splitext(file.filename)[0]
    output_filename = f"{filename_base}_{unique_id}.json"

    if file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = f"temp_statement_{unique_id}{os.path.splitext(file.filename)[1]}"  # Keep original extension
        try:
            file.save(image_path)
            print(f"Image saved to: {image_path}") #Confirm saved path

            describing_result = describing_image(image_path)  # No json.loads here

            if not describing_result:
                os.remove(image_path) #Clean up before error
                return jsonify({"error": "Failed to analyze image with OpenAI Vision"}), 500

            try:
                with open(output_filename, "w") as f:
                    json.dump({"description": describing_result}, f, indent=4)  # Wrap in JSON format
                print(f"Data saved to: {output_filename}")  # Logging

                os.remove(image_path) #Clean up after success
                return jsonify({"message": f"Image processed successfully. Data saved to {output_filename}"}), 200

            except Exception as e:
                print(f"Error saving to JSON file: {e}")
                os.remove(image_path) #Clean up after error
                return jsonify({"error": f"Failed to save data to JSON file: {e}"}), 500

        except Exception as e: #Catch saving issues
             print(f"Error processing image: {e}")
             return jsonify({"error": f"Failed to process image: {e}"}), 500


    else:
        return jsonify({"error": "Unsupported file type. Please upload a PNG, JPG, or JPEG."}), 400


if __name__ == '__main__':
    app.run(debug=True)