import requests

class BookingService:
    BOOKING_API_URL = "http://localhost:5000/api/bookings"  # URL для бронирования

    @staticmethod
    def confirm_booking(movie_title, seats):
        # Простой пример формирования данных для бронирования.
        data = {
            "movie_title": movie_title,
            "seats": seats
        }
        try:
            response = requests.post(BookingService.BOOKING_API_URL, json=data)
            response.raise_for_status()
            print("Бронь успешно подтверждена")
            return True
        except Exception as e:
            print("Ошибка подтверждения бронирования:", e)
            return False

    @staticmethod
    def validate_seats(seats):
        # При необходимости можно добавить валидацию выбранных мест
        return len(seats) > 0
