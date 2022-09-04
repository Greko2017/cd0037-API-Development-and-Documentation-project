# Flask - Route Decorator and Pagination - Pagination in Flask
# www.example.com/entrees?page=1

@app.route('/entrees', methods=['GET'])
def get_entrees():
 page = request.args.get('page', 1, type=int)
 
# Demo - Route decorator and pagination | "plants" database - Implementing Pagination

from flask import Flask, jsonify, request
from models import setup_db, Plant

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    @app.route('/plants', methods=['GET','POST'])
    #@cross_origin
    def get_plants():
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]
        return jsonify({
            'success': True,
            'plants':formatted_plants[start:end],
            'total_plants':len(formatted_plants)
            })

    return app
	
from flask import Flask, jsonify, request, abort
from models import setup_db, Plant

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    @app.route('/plants', methods=['GET','POST'])
    #@cross_origin
    def get_plants():
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]
        return jsonify({
            'success': True,
            'plants':formatted_plants[start:end],
            'total_plants':len(formatted_plants)
            })

    @app.route('/plants/<int:plant_id>')
    def get_specific_plant(plant_id):
        plant = Plant.query.filter(Plant.id==plant_id).one_or_none()
        if plant is None:
            abort(404)
        else:   
            return jsonify({
                'success': True,
                'plant': plant.format()
            })

    return app
	
from flask import Flask, jsonify, request, abort
from models import setup_db, Plant

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    @app.route('/plants', methods=['GET','POST'])
    #@cross_origin
    def get_plants():
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]
        return jsonify({
            'success': True,
            'plants':formatted_plants[start:end],
            'total_plants':len(formatted_plants)
            })

    @app.route('/plants/<int:plant_id>')
    def get_specific_plant(plant_id):
        plant = Plant.query.filter(Plant.id==plant_id).one_or_none()
        if plant is None:
            abort(404)
        else:   
            return jsonify({
                'success': True,
                'plant': plant.format()
            })

    return app
    
# Lesson 3: Flask Error Handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404
# Lesson 4: Testing in Flask
class AppNameTestCase(unittest.TestCase):
    """This class represents the ___ test case"""

    def setUp(self):
        """Executed before each test. Define test variables and initialize app."""
        self.client = app.test_client
        pass

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_given_behavior(self):
        """Test _____________ """
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    pass
    # unittest.main()

# Lesson 5: Documentation Examples
# https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/tree/master/5_API_Doc_Review

# The API documentation that I wrote includes the following:

# Getting started
# Base URL
# Error handling
# Endpoints

# lesson 5: Project Documentation
# Project Title

# Description of project and motivation
# Screenshots (if applicable), with captions
# Code Style if you are following particular style guides
# Getting Started

# Prerequisites & Installation, including code samples for how to download all pre-requisites
# Local Development, including how to set up the local development environment and run the project locally
# Tests and how to run them
# API Reference. If the API documentation is not very long, it can be included in the README

# Deployment (if applicable)

# Authors

# Acknowledgements