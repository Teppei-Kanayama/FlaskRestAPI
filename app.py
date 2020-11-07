from typing import Dict

from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class Student(Resource):

    def get(self, name: str) -> Dict[str, str]:
        return dict(student=name)


api.add_resource(Student, '/student/<string:name>')
app.run(port=5000)
