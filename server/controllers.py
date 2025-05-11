# server/controllers.py

from flask import Blueprint, request, jsonify, abort
from models import Movie, Booking
from database import db

# Создаем blueprint для фильмов
movies_blueprint = Blueprint("movies", __name__)

# Создаем blueprint для бронирований
bookings_blueprint = Blueprint("bookings", __name__)

# ------------------ Эндпоинты для фильмов ------------------ #

@movies_blueprint.route("/", methods=["GET"])
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.to_dict() for movie in movies]), 200

@movies_blueprint.route("/", methods=["POST"])
def add_movie():
    data = request.get_json()
    if not data or "title" not in data:
        abort(400, description="Отсутствует название фильма")
    new_movie = Movie(title=data["title"], description=data.get("description", ""))
    db.session.add(new_movie)
    db.session.commit()
    return jsonify(new_movie.to_dict()), 201

@movies_blueprint.route("/<int:movie_id>/", methods=["PUT"])
def edit_movie(movie_id):
    data = request.get_json()
    movie = Movie.query.get_or_404(movie_id)
    if "title" in data:
        movie.title = data["title"]
    if "description" in data:
        movie.description = data["description"]
    db.session.commit()
    return jsonify(movie.to_dict()), 200

@movies_blueprint.route("/<int:movie_id>/", methods=["DELETE"])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    # Явно удаляем все бронирования, связанные с данным фильмом,
    # чтобы избежать нарушения внешнего ключа
    Booking.query.filter_by(movie_id=movie_id).delete()
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Фильм и связанные бронирования удалены"}), 200

# ------------------ Эндпоинты для бронирований ------------------ #

@bookings_blueprint.route("/", methods=["GET"])
def get_bookings_by_movie():
    """
    GET /api/bookings/?movie_id=<id>
    Возвращает список бронирований для указанного фильма в виде списка словарей.
    Каждый объект брони содержит ключи: "id", "movie_id" и "seat_id".
    """
    movie_id = request.args.get("movie_id", type=int)
    if movie_id is None:
        abort(400, description="Параметр movie_id обязателен")
    bookings = Booking.query.filter_by(movie_id=movie_id).all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

@bookings_blueprint.route("/", methods=["POST"])
def create_booking():
    """
    POST /api/bookings/
    Ожидает JSON с полями "movie_id" и "seats" (список идентификаторов мест).
    Создает бронирования для указанных мест, если они ещё не забронированы.
    Возвращает список созданных бронирований в виде словарей.
    """
    data = request.get_json()
    movie_id = data.get("movie_id")
    seats = data.get("seats")
    if not movie_id or not seats:
        abort(400, description="Отсутствует movie_id или список seats")
    created_bookings = []
    for seat in seats:
        # Проверяем, что для данного фильма место ещё не забронировано
        existing_booking = Booking.query.filter_by(movie_id=movie_id, seat_id=seat).first()
        if existing_booking:
            continue
        new_booking = Booking(movie_id=movie_id, seat_id=seat)
        db.session.add(new_booking)
        created_bookings.append(new_booking)
    db.session.commit()
    return jsonify([booking.to_dict() for booking in created_bookings]), 201

@bookings_blueprint.route("/<int:booking_id>/", methods=["DELETE"])
def cancel_booking(booking_id):
    """
    DELETE /api/bookings/<booking_id>/
    Отменяет бронирование по его идентификатору.
    """
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Бронь отменена"}), 200
