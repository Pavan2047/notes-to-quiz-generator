from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from utils.file_processor import FileProcessor
from utils.mcq_generator import MCQGenerator

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

file_processor = FileProcessor()
mcq_generator = MCQGenerator()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and text extraction"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from file
        extracted_text = file_processor.process_file(filepath)
        
        return jsonify({
            'success': True,
            'text': extracted_text,
            'filename': filename
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-mcq', methods=['POST'])
def generate_mcq():
    """Generate MCQs from extracted text"""
    try:
        data = request.get_json()
        notes_text = data.get('text', '')
        num_questions = data.get('num_questions', 5)
        
        if not notes_text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate MCQs using AI
        mcqs = mcq_generator.generate_mcqs(notes_text, num_questions)
        
        return jsonify({
            'success': True,
            'mcqs': mcqs
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-quiz', methods=['POST'])
def download_quiz():
    """Download MCQs as PDF or text"""
    try:
        data = request.get_json()
        mcqs = data.get('mcqs', [])
        format_type = data.get('format', 'text')
        
        # TODO: Implement PDF/text export
        return jsonify({
            'success': True,
            'message': 'Download feature coming soon'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000