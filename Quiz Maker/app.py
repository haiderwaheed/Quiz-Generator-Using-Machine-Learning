# Imports
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from fpdf import FPDF
from dotenv import load_dotenv
import os, pdfplumber, docx, csv, google.generativeai as genai

# Set API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Dynamically create folders storing uploads and results
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULTS_FOLDER'] = 'results/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt', 'docx'}

# Check if the file extension is allowed
def file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Extract all text from uploaded file
def extract_text(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    # Extract from PDF
    if ext == 'pdf':
        with pdfplumber.open(file_path) as pdf:
            text = ''.join([page.extract_text() for page in pdf.pages])
        return text
    # Extract from DOCX
    elif ext == 'docx':
        doc = docx.Document(file_path)
        text = ' '.join([para.text for para in doc.paragraphs])
        return text
    # Extract from TXT
    elif ext == 'txt':
        with open(file_path, 'r') as file:
            return file.read()
    return None

# Send quiz generation prompt to Gemini
def generate_questions_gemini(input_text, num_questions):
    prompt = f"""
    You are an AI assistant whos job it is to generate multiple choice questions as part of a quiz for the user based on the following text:
    '{input_text}'
    Generate exactly {num_questions} questions from the text. Each question should have:
    - A clear question
    - Four answer options (labeled A, B, C, D)
    - The correct answer clearly indicated
    it must follow this exact Format:
    ## MCQ
    [Question] [question #:] [insert question here]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Correct Answer: [correct option]
    """
    response = model.generate_content(prompt).text.strip()
    print(response)
    return response

# Generate TXT of generate quiz
def save_as_txt(mcqs, filename):
    results_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    with open(results_path, 'w') as f:
        f.write(mcqs)
    return results_path

# Generate PDF of generated quiz
def save_as_pdf(mcqs, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for mcq in mcqs.split("## MCQ"):
        if mcq.strip():
            pdf.multi_cell(0, 10, mcq.strip())
            pdf.ln(5)  # Add line break

    pdf_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    pdf.output(pdf_path)
    return pdf_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])

# Create questions for quiz
def generate_mcqs():
    # Error handling if no file chosen
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    # Check, secure, and upload the file
    if file and file_allowed(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Call extract text function
        text = extract_text(file_path)
        if text:
            # Generate specified number of questions
            num_questions = int(request.form['num_questions'])
            mcqs = generate_questions_gemini(text, num_questions)
            # Save the generated quiz to a file
            txt_filename = f"{filename.rsplit('.', 1)[0]}_AI-quiz.txt"
            pdf_filename = f"{filename.rsplit('.', 1)[0]}_AI-quiz.pdf"
            save_as_txt(mcqs, txt_filename)
            save_as_pdf(mcqs, pdf_filename)
            # Display and allow downloading
            return render_template('results.html', mcqs=mcqs, txt_filename=txt_filename, pdf_filename=pdf_filename)
    return "Invalid file format"

# Download generated quiz
@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

# Python main
if __name__ == "__main__":
    # Do not create uploads folder if it already exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    # Do not create results folder if it already exists
    if not os.path.exists(app.config['RESULTS_FOLDER']):
        os.makedirs(app.config['RESULTS_FOLDER'])
    app.run(debug=True)