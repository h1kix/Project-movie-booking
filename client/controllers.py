# client/controllers.py
import requests
import tkinter as tk
from tkinter import simpledialog, messagebox

class MovieController:
    API_URL = "http://localhost:5000/api/movies/"

    def get_movies(self):
        try:
            response = requests.get(self.API_URL)
            response.raise_for_status()
            return response.json()  # Ожидается список фильмов в формате JSON
        except Exception as e:
            print("Ошибка получения фильмов:", e)
            return []

    def add_movie(self):
        # Запрос нового названия и описания через диалог
        title = simpledialog.askstring("Добавление фильма", "Введите название фильма:")
        if not title:
            return  # Если пользователь отменил
        description = simpledialog.askstring("Добавление фильма", "Введите описание фильма:")
        data = {"title": title, "description": description}
        try:
            response = requests.post(self.API_URL, json=data)
            response.raise_for_status()
            messagebox.showinfo("Успех", "Фильм успешно добавлен.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка добавления фильма: {e}")

    def edit_movie(self, movie):
        # movie – это словарь с полями id, title, description
        new_title = simpledialog.askstring("Редактирование фильма",
                                           "Введите новое название фильма:",
                                           initialvalue=movie.get("title"))
        if not new_title:
            return
        new_description = simpledialog.askstring("Редактирование фильма",
                                                 "Введите новое описание:",
                                                 initialvalue=movie.get("description", ""))
        data = {"title": new_title, "description": new_description}
        try:
            response = requests.put(f"{self.API_URL}{movie['id']}/", json=data)
            response.raise_for_status()
            messagebox.showinfo("Успех", "Фильм успешно отредактирован.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка редактирования фильма: {e}")

    def delete_movie(self, movie):
        # Запрашиваем подтверждение удаления
        confirm = messagebox.askyesno("Удаление фильма", f"Вы действительно хотите удалить фильм '{movie['title']}'?")
        if not confirm:
            return
        try:
            response = requests.delete(f"{self.API_URL}{movie['id']}/")
            response.raise_for_status()
            messagebox.showinfo("Успех", "Фильм успешно удалён.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления фильма: {e}")
