# # from flask import Flask, request, jsonify
# # import cv2
# # from paddleocr import PaddleOCR
# # import numpy as np
# # app = Flask(__name__)
# # ocr = PaddleOCR(use_angle_cls=True)

# # @app.route('/extract_text', methods=['POST'])
# # def extract_text():
# #     if 'file' not in request.files:
# #         return jsonify({'error': 'No file part'})

# #     file = request.files['file']

# #     if file.filename == '':
# #         return jsonify({'error': 'No selected file'})

# #     if file:
# #         # Read the image file
# #         img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

# #         # Extract text using PaddleOCR
# #         result = ocr.ocr(img)

# #         # Extracted text
# #         print(result)

# #         return jsonify({'extracted_text':result})

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=5000, debug=True)
# from flask import Flask, request, jsonify
# import cv2
# from paddleocr import PaddleOCR
# import numpy as np

# app = Flask(__name__)
# ocr = PaddleOCR(use_angle_cls=True)

# @app.route('/extract_text', methods=['POST'])
# def extract_text():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'})

#     file = request.files['file']

#     if file.filename == '':
#         return jsonify({'error': 'No selected file'})

#     if file:
#         img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

#         result = ocr.ocr(img)
#         print(result)

#         return jsonify({'extracted_text': result})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, request, jsonify
import cv2
import numpy as np
import fitz  # PyMuPDF
from io import BytesIO
from paddleocr import PaddleOCR

app = Flask(__name__)
ocr = PaddleOCR(use_angle_cls=True)

def extract_text_from_image(img):
    result = ocr.ocr(img)
    return result

def extract_text_from_pdf(pdf_bytes):
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ''
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    return text

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        if file.filename.endswith('.pdf'):
            pdf_bytes = file.read()
            text = extract_text_from_pdf(pdf_bytes)
            return jsonify({'extracted_text': text})
        else:
            img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
            result = extract_text_from_image(img)
            return jsonify({'extracted_text': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
