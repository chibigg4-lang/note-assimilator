import os
import base64
from flask import Flask
from flask_restful import Api, Resource, reqparse
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
app = Flask(__name__)
api = Api(app)

os.makedirs("uploads", exist_ok=True)
note_args = reqparse.RequestParser('Authorization', location='Json')
note_args.add_argument('student_id', type=int, required=True, help="Missing student ID")
note_args.add_argument('image_base64', type=str, required=True, help="Missing image data")

class MathNoteExtractor(Resource):
    def post(self):
        args = note_args.parse_args() 
        student_id = args['student_id']
        b64_string = args['image_base64']
        try:
            image_data = base64.b64decode(b64_string)
            if image_data.startswith(b'%PDF-'):
                # Convert PDF bytes directly to PIL Images in memory
                images = convert_from_bytes(image_data, dpi=300)
                
                if not images:
                    return {"error": "The uploaded PDF is empty"}, 400
                       
                filename = f"uploads/note_{student_id}.png"
                images[0].save(filename, 'PNG')
                message = "PDF converted and saved as PNG successfully!"

            # 3. If it's already a JPG
            elif image_data.startswith(b'\xff\xd8\xff'):
                filename = f"uploads/note_{student_id}.jpg"
                with open(filename, "wb") as file:
                    file.write(image_data)
                message = "JPG saved successfully!"

            # 4. If it's already a PNG
            elif image_data.startswith(b'\x89PNG\r\n\x1a\n'):
                filename = f"uploads/note_{student_id}.png"
                with open(filename, "wb") as file:
                    file.write(image_data)
                message = "PNG saved successfully!"
                
            else:
                return {"error": "Unsupported format. Please upload a PDF, JPG, or PNG."}, 400

            return {"message": message, "file_path": filename}, 201
            
        except Exception as e:
            return {"error": f"Failed to process file: {str(e)}"}, 400
        
api.add_resource(MathNoteExtractor, '/api/extract-note')

if __name__ == '__main__':
    app.run(port=5050, debug=True)