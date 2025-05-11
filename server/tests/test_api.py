# server/tests/test_api.py
import unittest
import json
from app import create_app
from database import db

class MoviesAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        # Используем базу данных SQLite в памяти для тестирования
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_movies_empty(self):
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])
    
    def test_create_movie(self):
        response = self.client.post("/api/movies/", json={
            "title": "Test Movie",
            "description": "Описание тестового фильма"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["title"], "Test Movie")
    
    def test_edit_movie(self):
        # Сначала создаем фильм
        res = self.client.post("/api/movies/", json={"title": "Old Title"})
        movie = json.loads(res.data)
        movie_id = movie["id"]

        # Затем редактируем его
        response = self.client.put(f"/api/movies/{movie_id}", json={"title": "New Title"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["title"], "New Title")

    def test_delete_movie(self):
        # Создаем фильм
        res = self.client.post("/api/movies/", json={"title": "Movie to Delete"})
        movie = json.loads(res.data)
        movie_id = movie["id"]

        # Удаляем фильм
        response = self.client.delete(f"/api/movies/{movie_id}")
        self.assertEqual(response.status_code, 200)
        # Проверяем, что список фильмов пустой
        res = self.client.get("/api/movies/")
        data = json.loads(res.data)
        self.assertEqual(len(data), 0)

if __name__ == "__main__":
    unittest.main()
