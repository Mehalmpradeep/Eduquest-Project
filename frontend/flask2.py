from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Mock OCR function that simulates text extraction from a file
def mock_ocr(file):
    return {"status": "success", "text": "Extracted text from the file."}

@app.route("/process_input", methods=["POST"])
def process_input():
    """Handles file uploads and text input."""
    try:
        # Ensure that either file or text is uploaded
        if "file" not in request.files and "text" not in request.form:
            return jsonify({"error": "No file or text uploaded"}), 400

        # If file is uploaded
        if "file" in request.files:
            file = request.files["file"]
            
            if file.filename == '':
                return jsonify({"error": "No file selected"}), 400

            # Secure the filename and simulate OCR
            filename = secure_filename(file.filename)
            ocr_result = mock_ocr(file)
            
            return jsonify({
                "message": "File processed by OCR",
                "file_name": filename,
                "ocr_text": ocr_result["text"]
            }), 200

        # If text is entered
        if "text" in request.form and request.form["text"].strip():
            text = request.form["text"].strip()
            return jsonify({"message": "Text received and forwarded for processing", "text": text}), 200

        return jsonify({"error": "No valid input provided"}), 400
    
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run()