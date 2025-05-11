# server/models.py
from database import db

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    # Можно добавить отношение, если потребуется: movie.bookings
    bookings = db.relationship("Booking", backref="movie", lazy=True)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description}

class Auditorium(db.Model):
    __tablename__ = "auditoriums"
    id = db.Column(db.Integer, primary_key=True)
    # Связь с местами: один зал имеет множество мест
    seats = db.relationship("Seat", backref="auditorium", lazy=True)

    def to_dict(self):
        return {"id": self.id}

class Seat(db.Model):
    __tablename__ = "seats"
    id = db.Column(db.Integer, primary_key=True)
    row = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    auditorium_id = db.Column(db.Integer, db.ForeignKey("auditoriums.id"), nullable=False)

    def to_dict(self):
        return {"id": self.id, "row": self.row, "number": self.number, "auditorium_id": self.auditorium_id}

class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey("seats.id"), nullable=False)

    def to_dict(self):
        return {"id": self.id, "movie_id": self.movie_id, "seat_id": self.seat_id}
