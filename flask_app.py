from flask import Flask, request, jsonify
from summarizer import text_summarize
from GetText import extract_text_from_pdf

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    input_method = request.form.get('input_method')
    text_input = request.form.get('text_input')
    uploaded_pdf_file = request.files.get('uploaded_pdf_file')

    # If text
    if input_method == "text" and text_input:
        summary = text_summarize(text_input)
        return jsonify({'summary': summary})

    # If pdf
    elif input_method == "pdf" and uploaded_pdf_file:
        text_from_pdf = extract_text_from_pdf(uploaded_pdf_file)
        summary = text_summarize(text_from_pdf)
        return jsonify({'summary': summary})

    return jsonify({'error': 'No text provided for summarization.'}), 400

if __name__ == "__main__":
    app.run(debug=True)
