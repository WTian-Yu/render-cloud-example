import os
from flask import Flask, request, jsonify, abort
from models import setup_db, Movie, Actor
from flask_cors import CORS

from auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def welcome_page():
        return "Casting Agency Homepage"

    # Actors Routes
    
    
    @app.route('/actors')
    def get_actors():
        """
        returns status code 200 and json {"success": True, "actors": actors}
            where actors is the list of actors
            or appropriate status code indicating reason for failure
        """
        try:
            actors = [actor.format() for actor in Actor.query.all()]
            return jsonify({'success': True,
                            'actors': actors})
        except BaseException:
            abort(422)
    
    @app.route('/actors', methods=['POST'])
    def create_actor():
        """
        returns status code 200 and json {"success": True, "actor": actor}
            where actor an array containing only the newly created actor
            or appropriate status code indicating reason for failure
        """
        try:
            body = request.get_json()
            name = body.get("name", None)
            age = body.get("age", None)
            gender = body.get("gender", None)
            if(name is None or age is None or gender is None):
                abort(422)
            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()
            return jsonify({'success': True,
                            'actor': new_actor.format()})
        except BaseException:
            abort(422)
    
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def patch_actor(actor_id):
        """
        returns status code 200 and json {"success": True, "actor": actor}
            where actor an array containing only the updated actor
            or appropriate status code indicating reason for failure

        Keyword arguments:
        actor_id -- the existing actor id
        """
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if(actor is None):
                abort(404)
            body = request.get_json()
            name = body.get("name", None)
            age = body.get("age", None)
            gender = body.get("gender", None)
            if(name is not None):
                actor.name = name
            if(age is not None):
                actor.age = age
            if(gender is not None):
                actor.gender = gender
            actor.update()

            return jsonify({'success': True,
                            'actor': [actor.format()]})
        except BaseException:
            abort(422)
    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        """
        returns status code 200 and json {"success": True, "delete": id}
            where id is the id of the deleted record
            or appropriate status code indicating reason for failure
        """
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if(actor is None):
                abort(404)
            
            actor.delete()

            return jsonify({'success': True,
                            'delete': actor_id})
        except BaseException:
            abort(422)
    
    # Movies Routes
    
    
    @app.route('/movies')
    def get_movies():
        """
        returns status code 200 and json {"success": True, "movies": movies}
            where movies is the list of movies
            or appropriate status code indicating reason for failure
        """
        try:
            movies = [movie.format() for movie in Movie.query.all()]
            return jsonify({'success': True,
                            'movies': movies})
        except BaseException:
            abort(422)
    
    @app.route('/movies', methods=['POST'])
    def create_movie():
        """
        returns status code 200 and json {"success": True, "movie": movie}
            where movie an array containing only the newly created movie
            or appropriate status code indicating reason for failure
        """
        try:
            body = request.get_json()
            title = body.get("title", None)
            release_date = body.get("release_date", None)
            if(title is None or release_date is None):
                abort(422)
            new_movie = Movie(title=title, release_date=release_date)
            new_movie.insert()
            return jsonify({'success': True,
                            'movie': new_movie.format()})
        except BaseException:
            abort(422)
    
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def patch_movie(movie_id):
        """
        returns status code 200 and json {"success": True, "movie": movie}
            where movie an array containing only the updated movie
            or appropriate status code indicating reason for failure

        Keyword arguments:
        movie_id -- the existing movie id
        """
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if(movie is None):
                abort(404)
            body = request.get_json()
            title = body.get("title", None)
            release_date = body.get("release_date", None)
            
            if(title is not None):
                movie.title = title
            if(release_date is not None):
                movie.release_date = release_date
            
            movie.update()

            return jsonify({'success': True,
                            'movie': [movie.format()]})
        except BaseException:
            abort(422)
    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        """
        returns status code 200 and json {"success": True, "delete": id}
            where id is the id of the deleted record
            or appropriate status code indicating reason for failure
        """
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if(movie is None):
                abort(404)
            
            movie.delete()

            return jsonify({'success': True,
                            'delete': movie_id})
        except BaseException:
            abort(422)
    
    
    # Error Handling
    
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
