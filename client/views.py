import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import requests
from controllers import MovieController

class MovieSelectionView(tb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.controller = MovieController()
        self.movies = []  # каждый фильм — словарь с полями id, title, description
        self.create_widgets()
        self.refresh_movies()

    def create_widgets(self):
        # Список фильмов (используем стандартный tk.Listbox)
        self.movies_listbox = tk.Listbox(self, width=50, height=15, font=("Helvetica", 12))
        self.movies_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Панель кнопок (виджеты ttkbootstrap)
        self.buttons_frame = tb.Frame(self)
        self.buttons_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        self.add_btn = tb.Button(self.buttons_frame, text="Добавить", bootstyle=INFO, command=self.controller.add_movie)
        self.add_btn.pack(fill=tk.X, pady=5)
        
        self.edit_btn = tb.Button(self.buttons_frame, text="Редактировать", bootstyle=PRIMARY, command=self.on_edit_movie)
        self.edit_btn.pack(fill=tk.X, pady=5)
        
        self.delete_btn = tb.Button(self.buttons_frame, text="Удалить", bootstyle=DANGER, command=self.on_delete_movie)
        self.delete_btn.pack(fill=tk.X, pady=5)
        
        self.select_btn = tb.Button(self.buttons_frame, text="Выбрать зал", bootstyle=SUCCESS, command=self.select_movie)
        self.select_btn.pack(fill=tk.X, pady=5)
        
        self.booking_btn = tb.Button(self.buttons_frame, text="Управлять бронями", bootstyle=WARNING, command=self.open_booking_management)
        self.booking_btn.pack(fill=tk.X, pady=5)

    def refresh_movies(self):
        self.movies = self.controller.get_movies()
        self.movies_listbox.delete(0, tk.END)
        for movie in self.movies:
            self.movies_listbox.insert(tk.END, movie['title'])
        self.after(5000, self.refresh_movies)

    def get_selected_movie(self):
        selection = self.movies_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Не выбран фильм.")
            return None
        index = selection[0]
        return self.movies[index]

    def on_edit_movie(self):
        movie = self.get_selected_movie()
        if movie:
            self.controller.edit_movie(movie)

    def on_delete_movie(self):
        movie = self.get_selected_movie()
        if movie:
            self.controller.delete_movie(movie)

    def select_movie(self):
        movie = self.get_selected_movie()
        if movie:
            auditorium_window = tb.Toplevel(self)
            AuditoriumView(auditorium_window, movie['id'], movie['title']).pack(fill=tk.BOTH, expand=True)

    def open_booking_management(self):
        movie = self.get_selected_movie()
        if movie:
            booking_window = tb.Toplevel(self)
            BookingManagementView(booking_window, movie['id'], movie['title']).pack(fill=tk.BOTH, expand=True)


class AuditoriumView(tb.Frame):
    def __init__(self, master, movie_id, movie_title):
        super().__init__(master, padding=20)
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.selected_seats = []  # формат: "row-seat" (например, "2-5")
        self.seat_buttons = {}    # ключ: "row-seat", значение: кнопка
        self.create_widgets()
        self.load_seating()

    def create_widgets(self):
        self.label = tb.Label(self, text=f"Зал для фильма: {self.movie_title}", font=("Helvetica", 16, "bold"))
        self.label.grid(row=0, column=0, columnspan=10, pady=10)

    def load_seating(self):
        booked = self.get_booked_seats()
        # Предположим зал с 5 рядами, 10 мест в каждом ряду
        for row in range(1, 6):
            for seat in range(1, 11):
                key = f"{row}-{seat}"
                btn = tb.Button(self, text=key, width=4, command=lambda r=row, s=seat: self.toggle_seat(r, s))
                btn.seat_id = (row - 1) * 10 + seat  # числовой идентификатор места
                btn.grid(row=row, column=seat, padx=2, pady=2)
                if key in booked:
                    btn.configure(bootstyle="danger", state="disabled")
                else:
                    btn.configure(bootstyle="secondary")
                self.seat_buttons[key] = btn
        self.confirm_btn = tb.Button(self, text="Подтвердить бронь", bootstyle="success", command=self.confirm_booking)
        self.confirm_btn.grid(row=7, column=0, columnspan=10, pady=10)

    def toggle_seat(self, row, seat):
        key = f"{row}-{seat}"
        btn = self.seat_buttons.get(key)
        if btn.cget("state") == "disabled":
            return  # нельзя выбирать занятые места
        # Если место уже выбрано, отменяем выбор; иначе выбираем
        if key in self.selected_seats:
            btn.configure(bootstyle="secondary")
            self.selected_seats.remove(key)
        else:
            btn.configure(bootstyle="success")
            self.selected_seats.append(key)

    def get_booked_seats(self):
        try:
            url = f"http://localhost:5000/api/bookings/?movie_id={self.movie_id}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            booked_keys = []
            # Если сервер возвращает список объектов (словари)
            if data and isinstance(data[0], dict):
                for booking in data:
                    seat_id = booking.get("seat_id")
                    for row in range(1, 6):
                        for seat in range(1, 11):
                            if (row - 1) * 10 + seat == seat_id:
                                booked_keys.append(f"{row}-{seat}")
                return booked_keys
            # Если сервер возвращает список чисел
            elif data and isinstance(data[0], int):
                for row in range(1, 6):
                    for seat in range(1, 11):
                        seat_id = (row - 1) * 10 + seat
                        if seat_id in data:
                            booked_keys.append(f"{row}-{seat}")
                return booked_keys
            else:
                return []
        except Exception as e:
            print("Ошибка получения забронированных мест:", e)
            return []

    def refresh_seating(self):
        booked = self.get_booked_seats()
        for key, btn in self.seat_buttons.items():
            if key in booked:
                btn.configure(bootstyle="danger", state="disabled")
                if key in self.selected_seats:
                    self.selected_seats.remove(key)
            else:
                # Если место не выбрано, устанавливаем стандартный стиль
                if key not in self.selected_seats:
                    btn.configure(bootstyle="secondary", state="normal")

    def confirm_booking(self):
        if not self.selected_seats:
            messagebox.showwarning("Предупреждение", "Нет выбранных мест.")
            return
        selected_seat_ids = []
        for key in self.selected_seats:
            try:
                row, seat = map(int, key.split("-"))
                seat_id = (row - 1) * 10 + seat
                selected_seat_ids.append(seat_id)
            except Exception as e:
                print("Ошибка преобразования ключа:", key, e)
        data = {"movie_id": self.movie_id, "seats": selected_seat_ids}
        try:
            response = requests.post("http://localhost:5000/api/bookings/", json=data)
            response.raise_for_status()
            messagebox.showinfo("Информация", f"Бронь для мест {', '.join(self.selected_seats)} оформлена.")
            self.selected_seats.clear()
            self.refresh_seating()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при оформлении брони: {e}")


class BookingManagementView(tb.Frame):
    def __init__(self, master, movie_id, movie_title):
        super().__init__(master, padding=20)
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.bookings = []  # список объектов брони (словари с ключами "id" и "seat_id")
        self.create_widgets()
        self.refresh_bookings()

    def create_widgets(self):
        self.label = tb.Label(self, text=f"Брони для фильма: {self.movie_title}", font=("Helvetica", 16, "bold"))
        self.label.pack(pady=10)
        
        self.bookings_listbox = tk.Listbox(self, width=50, height=10, font=("Helvetica", 12))
        self.bookings_listbox.pack(pady=10)
        
        self.buttons_frame = tb.Frame(self)
        self.buttons_frame.pack(pady=5)
        
        self.cancel_btn = tb.Button(self.buttons_frame, text="Отменить бронь", bootstyle="danger", command=self.cancel_booking)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = tb.Button(self.buttons_frame, text="Обновить", bootstyle="info", command=self.refresh_bookings)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)

    def refresh_bookings(self):
        try:
            url = f"http://localhost:5000/api/bookings/?movie_id={self.movie_id}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            # Если данные не в виде объектов, преобразуем их:
            if data and not isinstance(data[0], dict):
                self.bookings = [{"id": None, "seat_id": seat} for seat in data]
            else:
                self.bookings = data
            self.bookings_listbox.delete(0, tk.END)
            for booking in self.bookings:
                if isinstance(booking, dict):
                    booking_id = booking.get("id") if booking.get("id") is not None else "N/A"
                    seat_id = booking.get("seat_id")
                else:
                    seat_id = booking
                    booking_id = "N/A"
                if seat_id is None:
                    continue
                row = (seat_id - 1) // 10 + 1
                seat = (seat_id - 1) % 10 + 1
                display_text = f"Бронь ID: {booking_id} - Ряд {row}, Место {seat}"
                self.bookings_listbox.insert(tk.END, display_text)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки бронирований: {e}")

    def get_selected_booking(self):
        selection = self.bookings_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Не выбрано бронирование.")
            return None
        index = selection[0]
        if index < len(self.bookings):
            return self.bookings[index]
        return None

    def cancel_booking(self):
        booking = self.get_selected_booking()
        if booking:
            if isinstance(booking, dict):
                booking_id = booking.get("id")
                if booking_id is None:
                    messagebox.showerror("Ошибка", "Невозможно отменить бронь: отсутствует идентификатор брони.")
                    return
            else:
                messagebox.showerror("Ошибка", "Невозможно отменить бронь: некорректные данные.")
                return
            try:
                url = f"http://localhost:5000/api/bookings/{booking_id}/"
                response = requests.delete(url)
                response.raise_for_status()
                messagebox.showinfo("Информация", "Бронь отменена.")
                self.refresh_bookings()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при отмене бронирования: {e}")

if __name__ == "__main__":
    app = tb.Window(themename="flatly")
    app.title("Cinema Booking Application")
    app.geometry("1000x700")
    main_view = MovieSelectionView(app)
    main_view.pack(fill="both", expand=True)
    app.mainloop()
