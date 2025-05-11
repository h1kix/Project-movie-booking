import unittest
from unittest.mock import patch
from controllers import MovieController

class TestMovieController(unittest.TestCase):

    @patch("controllers.requests.get")
    def test_get_movies_success(self, mock_get):
        # Имитируем успешный ответ сервера с одним фильмом
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": 1, "title": "Фильм 1", "description": "Описание"}]
        
        controller = MovieController()
        movies = controller.get_movies()
        
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]["title"], "Фильм 1")

if __name__ == "__main__":
    unittest.main()
