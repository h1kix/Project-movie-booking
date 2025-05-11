import tkinter as tk
from views import MovieSelectionView

def main():
    root = tk.Tk()
    root.title("Бронирование билетов в кинотеатр")

    # Инициализация первого экрана: выбор фильма
    movie_selection_view = MovieSelectionView(root)
    movie_selection_view.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
