# server/app.py
from flask import Flask
from database import db
from controllers import movies_blueprint, bookings_blueprint
from models import Auditorium, Seat

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123@localhost:5432"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(movies_blueprint, url_prefix="/api/movies")
    app.register_blueprint(bookings_blueprint, url_prefix="/api/bookings")

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        # Предварительное заполнение таблицы seats, если они еще не созданы
        if not Auditorium.query.first():
            auditorium = Auditorium()
            db.session.add(auditorium)
            db.session.commit()
            for row in range(1, 6):        # 5 рядов
                for number in range(1, 11):  # 10 мест в ряду
                    seat = Seat(row=row, number=number, auditorium_id=auditorium.id)
                    db.session.add(seat)
            db.session.commit()
    app.run(debug=True)
