import os
import base64
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

os.makedirs("uploads", exist_ok=True)
note_args = reqparse.RequestParser(location='Json')
note_args.add_argument('student_id', type=int, required=True, help="Missing student ID")
note_args.add_argument('image_base64', type=str, required=True, help="Missing image data")
class MathNoteExtractor(Resource):
    def post(self):
        args = note_args.parse_args() 
        student_id = args['student_id']
        b64_string = args['image_base64']
        try:
            image_data = base64.b64decode(b64_string)
            filename = f"uploads/note_{student_id}.jpg"
            with open(filename, "wb") as file:
                file.write(image_data)
            return {"message": "Image saved successfully!", "file_path": filename}, 201
        except Exception as e:
            return {"error": f"Failed to decode image: {str(e)}"}, 400
api.add_resource(MathNoteExtractor, '/api/extract-note')

if __name__ == '__main__':
    app.run(port=5050, debug=True)
