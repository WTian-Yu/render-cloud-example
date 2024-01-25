import os
import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

casting_assistant_auth_header = {
    'Authorization': os.environ['CASTING_ASSISTANT_TOKEN']
}

casting_director_auth_header = {
    'Authorization': os.environ['CASTING_DIRECTOR_TOKEN']
}

executive_producer_auth_header = {
    'Authorization': os.environ['EXCEUTIVE_PRODUCER_TOKEN']
}

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        
        setup_db(self.app, self.database_path)

        self.new_actor = {
            "name": "A new actor",
            'age': 35,
            'gender': 'Female',
        }
        
        self.new_movie = {
            "title": "title",
            'release_date': "2024-10-21T21:30:00.000Z",
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    # For actors testing
    
    
    # get actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_401_if_get_actors_not_include_header(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
    def test_422_if_get_actors_page_invalid(self):
        res = self.client().get("/actors?page=1000", headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    # POST actors
    def test_post_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_401_if_post_new_actors_not_include_headers(self):
        res = self.client().post('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
    def test_401_if_post_new_actors_without_permission(self):
        res = self.client().post('/actors', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        
    def test_422_if_create_new_actor_input_invalid(self):
        res = self.client().post("/actors", json={}, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    # PATCH actors
    def test_patch_new_actor(self):
        res = self.client().patch('/actors/6', json=self.new_actor, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_401_if_patch_new_actor_not_include_headers(self):
        res = self.client().patch('/actors/6', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
    def test_422_if_patch_actor_id_invalid(self):
        res = self.client().patch("/actors/1000", json=self.new_actor, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    # DELETE actors
    def test_delete_actor(self):
        res = self.client().delete('/actors/5', headers=casting_director_auth_header)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 5)
        self.assertEqual(actor, None)

    def test_401_if_delete_actor_not_include_headers(self):
        res = self.client().delete('/actors/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
    def test_422_if_delete_actor_does_not_exist(self):
        res = self.client().delete("/actors/1000", headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    # For movies testing
    
    
    # get movies
    def test_get_movies(self):
        res = self.client().get('/movies', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_401_if_get_movies_without_headers(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
    def test_422_if_get_movies_page_invalid(self):
        res = self.client().get("/movies?page=1000", headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    # POST movies
    def test_post_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_401_if_post_new_movie_without_headers(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
    def test_422_if_create_new_movie_input_invalid(self):
        res = self.client().post("/movies", json={}, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    # PATCH movies
    def test_patch_new_movie(self):
        res = self.client().patch('/movies/13', json=self.new_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_401_if_patch_new_movie_without_headers(self):
        res = self.client().patch('/movies/13', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
    def test_422_if_patch_movie_id_invalid(self):
        res = self.client().patch("/movies/1000", json=self.new_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    # DELETE movies
    def test_delete_movie(self):
        res = self.client().delete('/movies/12', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 12).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 12)
        self.assertEqual(movie, None)

    def test_401_if_delete_movie_without_headers(self):
        res = self.client().delete('/movies/12')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
    def test_422_if_delete_movie_does_not_exist(self):
        res = self.client().delete("/movies/1000", headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()