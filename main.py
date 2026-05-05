import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os
import random


class MovieLibrary:
    """Графическое приложение для хранения информации о фильмах"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Ткаченко Руслан")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)
        
        # Файл для хранения фильмов
        self.data_file = "movies.json"
        self.movies = []
        self.filtered_movies = []
        
        # Загрузка фильмов
        self.load_movies()
        
        # Переменные для фильтрации
        self.filter_genre = tk.StringVar()
        self.filter_year = tk.StringVar()
        self.filter_rating = tk.StringVar()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление фильтров
        self.update_filters()
        
        # Отображение всех фильмов
        self.refresh_movie_list()
    
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        # Основная рамка
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="🎬 MOVIE LIBRARY - Библиотека фильмов", 
                                 font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Левая панель - добавление/редактирование фильма
        left_frame = ttk.LabelFrame(main_frame, text="📝 Добавить / Редактировать фильм", padding="15")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Название фильма
        ttk.Label(left_frame, text="Название фильма:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=2)
        self.title_entry = ttk.Entry(left_frame, width=40, font=("Arial", 11))
        self.title_entry.pack(fill=tk.X, pady=5)
        
        # Режиссер
        ttk.Label(left_frame, text="Режиссер:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=2)
        self.director_entry = ttk.Entry(left_frame, width=40, font=("Arial", 11))
        self.director_entry.pack(fill=tk.X, pady=5)
        
        # Год выпуска
        year_frame = ttk.Frame(left_frame)
        year_frame.pack(fill=tk.X, pady=5)
        ttk.Label(year_frame, text="Год выпуска:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.year_entry = ttk.Entry(year_frame, width=10, font=("Arial", 11))
        self.year_entry.pack(side=tk.LEFT, padx=10)
        ttk.Label(year_frame, text="(например: 2024)").pack(side=tk.LEFT)
        
        # Жанр
        ttk.Label(left_frame, text="Жанр:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=2)
        self.genre_entry = ttk.Entry(left_frame, width=40, font=("Arial", 11))
        self.genre_entry.pack(fill=tk.X, pady=5)
        
        # Рейтинг
        rating_frame = ttk.Frame(left_frame)
        rating_frame.pack(fill=tk.X, pady=5)
        ttk.Label(rating_frame, text="Рейтинг (0-10):", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.rating_entry = ttk.Entry(rating_frame, width=10, font=("Arial", 11))
        self.rating_entry.pack(side=tk.LEFT, padx=10)
        
        # Описание
        ttk.Label(left_frame, text="Описание:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=2)
        self.description_text = tk.Text(left_frame, height=6, width=40, wrap=tk.WORD)
        self.description_text.pack(fill=tk.X, pady=5)
        
        # Кнопки действий
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(pady=10)
        
        self.add_btn = ttk.Button(btn_frame, text="➕ ДОБАВИТЬ ФИЛЬМ", command=self.add_movie)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.update_btn = ttk.Button(btn_frame, text="✏️ ОБНОВИТЬ", command=self.update_movie, state=tk.DISABLED)
        self.update_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(btn_frame, text="🗑 ОЧИСТИТЬ ФОРМУ", command=self.clear_form)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Правая панель - список фильмов
        right_frame = ttk.LabelFrame(main_frame, text="📋 Список фильмов", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Панель фильтрации
        filter_frame = ttk.LabelFrame(right_frame, text="🔍 Фильтрация", padding="10")
        filter_frame.pack(fill=tk.X, pady=5)
        
        # Фильтр по жанру
        genre_filter_frame = ttk.Frame(filter_frame)
        genre_filter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(genre_filter_frame, text="Жанр:").pack(side=tk.LEFT, padx=5)
        self.genre_combo = ttk.Combobox(genre_filter_frame, textvariable=self.filter_genre, width=20, state="readonly")
        self.genre_combo.pack(side=tk.LEFT, padx=5)
        self.genre_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
        # Фильтр по году
        year_filter_frame = ttk.Frame(filter_frame)
        year_filter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(year_filter_frame, text="Год:").pack(side=tk.LEFT, padx=5)
        self.year_combo = ttk.Combobox(year_filter_frame, textvariable=self.filter_year, width=20, state="readonly")
        self.year_combo.pack(side=tk.LEFT, padx=5)
        self.year_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
        # Фильтр по рейтингу
        rating_filter_frame = ttk.Frame(filter_frame)
        rating_filter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(rating_filter_frame, text="Рейтинг (мин):").pack(side=tk.LEFT, padx=5)
        self.rating_combo = ttk.Combobox(rating_filter_frame, textvariable=self.filter_rating, width=20, state="readonly")
        self.rating_combo.pack(side=tk.LEFT, padx=5)
        self.rating_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
        # Кнопки фильтрации
        filter_btn_frame = ttk.Frame(filter_frame)
        filter_btn_frame.pack(pady=5)
        ttk.Button(filter_btn_frame, text="🎲 СЛУЧАЙНЫЙ ФИЛЬМ", command=self.show_random_movie).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_btn_frame, text="🔄 СБРОСИТЬ ФИЛЬТРЫ", command=self.reset_filters).pack(side=tk.LEFT, padx=5)
        
        # Таблица фильмов
        columns = ("ID", "Название", "Режиссер", "Год", "Жанр", "Рейтинг")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("ID", text="№")
        self.tree.heading("Название", text="Название фильма")
        self.tree.heading("Режиссер", text="Режиссер")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Рейтинг", text="Рейтинг")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Название", width=200)
        self.tree.column("Режиссер", width=150)
        self.tree.column("Год", width=80, anchor=tk.CENTER)
        self.tree.column("Жанр", width=120)
        self.tree.column("Рейтинг", width=80, anchor=tk.CENTER)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопки управления
        control_frame = ttk.Frame(right_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="📖 ПОКАЗАТЬ ОПИСАНИЕ", command=self.show_description).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="✏️ РЕДАКТИРОВАТЬ", command=self.select_movie).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🗑 УДАЛИТЬ", command=self.delete_movie).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="💾 СОХРАНИТЬ", command=self.save_movies).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="📤 ЭКСПОРТ", command=self.export_movies).pack(side=tk.LEFT, padx=5)
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=5)
        
        # Счетчик фильмов
        self.count_label = ttk.Label(main_frame, text="", font=("Arial", 9))
        self.count_label.pack()
        self.update_count_label()
    
    def validate_movie(self, title, director, year, genre, rating):
        """Валидация полей фильма"""
        # Проверка на пустые поля
        if not title or not title.strip():
            messagebox.showerror("Ошибка", "Название фильма не может быть пустым!")
            return False
        
        if not director or not director.strip():
            messagebox.showerror("Ошибка", "Имя режиссера не может быть пустым!")
            return False
        
        if not year or not year.strip():
            messagebox.showerror("Ошибка", "Год выпуска не может быть пустым!")
            return False
        
        if not genre or not genre.strip():
            messagebox.showerror("Ошибка", "Жанр не может быть пустым!")
            return False
        
        if not rating or not rating.strip():
            messagebox.showerror("Ошибка", "Рейтинг не может быть пустым!")
            return False
        
        # Проверка года
        try:
            year_int = int(year)
            if year_int < 1888 or year_int > 2026:
                messagebox.showerror("Ошибка", "Год должен быть от 1888 до 2026!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть целым числом!")
            return False
        
        # Проверка рейтинга
        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return False
        
        return True
    
    def add_movie(self):
        """Добавление нового фильма"""
        try:
            title = self.title_entry.get().strip()
            director = self.director_entry.get().strip()
            year = self.year_entry.get().strip()
            genre = self.genre_entry.get().strip()
            rating = self.rating_entry.get().strip()
            description = self.description_text.get("1.0", tk.END).strip()
            
            # Валидация
            if not self.validate_movie(title, director, year, genre, rating):
                return
            
            # Проверка на дубликат
            for movie in self.movies:
                if movie['title'].lower() == title.lower():
                    messagebox.showerror("Ошибка", f"Фильм '{title}' уже существует в библиотеке!")
                    return
            
            # Создание нового фильма
            new_movie = {
                'id': len(self.movies) + 1,
                'title': title,
                'director': director,
                'year': int(year),
                'genre': genre,
                'rating': float(rating),
                'description': description,
                'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.movies.append(new_movie)
            self.save_movies()
            self.clear_form()
            self.update_filters()
            self.refresh_movie_list()
            self.update_count_label()
            self.status_var.set(f"✅ Фильм '{title}' добавлен в библиотеку!")
            messagebox.showinfo("Успех", f"Фильм '{title}' успешно добавлен!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить фильм: {e}")
    
    def update_movie(self):
        """Обновление существующего фильма"""
        if not hasattr(self, 'editing_id'):
            return
        
        try:
            title = self.title_entry.get().strip()
            director = self.director_entry.get().strip()
            year = self.year_entry.get().strip()
            genre = self.genre_entry.get().strip()
            rating = self.rating_entry.get().strip()
            description = self.description_text.get("1.0", tk.END).strip()
            
            if not self.validate_movie(title, director, year, genre, rating):
                return
            
            for movie in self.movies:
                if movie['id'] == self.editing_id:
                    movie['title'] = title
                    movie['director'] = director
                    movie['year'] = int(year)
                    movie['genre'] = genre
                    movie['rating'] = float(rating)
                    movie['description'] = description
                    break
            
            self.save_movies()
            self.clear_form()
            self.update_filters()
            self.refresh_movie_list()
            self.status_var.set(f"✏️ Фильм '{title}' обновлен!")
            messagebox.showinfo("Успех", "Фильм успешно обновлен!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить фильм: {e}")
    
    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите фильм для удаления!")
            return
        
        item = self.tree.item(selected[0])
        movie_title = item['values'][1]
        
        if messagebox.askyesno("Подтверждение", f"Удалить фильм '{movie_title}'?"):
            movie_id = item['values'][0]
            self.movies = [movie for movie in self.movies if movie['id'] != movie_id]
            
            # Перенумерация ID
            for i, movie in enumerate(self.movies, 1):
                movie['id'] = i
            
            self.save_movies()
            self.update_filters()
            self.refresh_movie_list()
            self.update_count_label()
            self.status_var.set(f"🗑 Фильм '{movie_title}' удален!")
            messagebox.showinfo("Успех", "Фильм удален!")
    
    def select_movie(self):
        """Выбор фильма для редактирования"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите фильм для редактирования!")
            return
        
        item = self.tree.item(selected[0])
        movie_id = item['values'][0]
        
        for movie in self.movies:
            if movie['id'] == movie_id:
                self.editing_id = movie_id
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, movie['title'])
                self.director_entry.delete(0, tk.END)
                self.director_entry.insert(0, movie['director'])
                self.year_entry.delete(0, tk.END)
                self.year_entry.insert(0, movie['year'])
                self.genre_entry.delete(0, tk.END)
                self.genre_entry.insert(0, movie['genre'])
                self.rating_entry.delete(0, tk.END)
                self.rating_entry.insert(0, movie['rating'])
                self.description_text.delete("1.0", tk.END)
                self.description_text.insert("1.0", movie.get('description', ''))
                
                self.add_btn.config(state=tk.DISABLED)
                self.update_btn.config(state=tk.NORMAL)
                break
    
    def show_description(self):
        """Показать описание выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите фильм!")
            return
        
        item = self.tree.item(selected[0])
        movie_id = item['values'][0]
        
        for movie in self.movies:
            if movie['id'] == movie_id:
                desc_window = tk.Toplevel(self.root)
                desc_window.title(f"Описание фильма - {movie['title']}")
                desc_window.geometry("500x400")
                
                text_widget = tk.Text(desc_window, wrap=tk.WORD, font=("Arial", 11))
                text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                info = f"""🎬 НАЗВАНИЕ: {movie['title']}

👨‍🎨 РЕЖИССЕР: {movie['director']}

📅 ГОД: {movie['year']}

🎭 ЖАНР: {movie['genre']}

⭐ РЕЙТИНГ: {movie['rating']}/10

📝 ОПИСАНИЕ:
{movie.get('description', 'Описание отсутствует')}

📅 ДОБАВЛЕН: {movie.get('date_added', 'Неизвестно')}
"""
                text_widget.insert("1.0", info)
                text_widget.config(state=tk.DISABLED)
                
                ttk.Button(desc_window, text="Закрыть", command=desc_window.destroy).pack(pady=10)
                break
    
    def show_random_movie(self):
        """Показать случайный фильм"""
        if not self.filtered_movies:
            source = self.movies
        else:
            source = self.filtered_movies
        
        if not source:
            messagebox.showinfo("Информация", "Нет фильмов для выбора!")
            return
        
        movie = random.choice(source)
        
        # Выделяем фильм в списке
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == movie['id']:
                self.tree.selection_set(item)
                self.tree.see(item)
                break
        
        # Показываем описание
        desc_window = tk.Toplevel(self.root)
        desc_window.title(f"🎲 СЛУЧАЙНЫЙ ФИЛЬМ - {movie['title']}")
        desc_window.geometry("500x400")
        
        text_widget = tk.Text(desc_window, wrap=tk.WORD, font=("Arial", 11))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        info = f"""🎲 ВАШ СЛУЧАЙНЫЙ ФИЛЬМ:

🎬 НАЗВАНИЕ: {movie['title']}

👨‍🎨 РЕЖИССЕР: {movie['director']}

📅 ГОД: {movie['year']}

🎭 ЖАНР: {movie['genre']}

⭐ РЕЙТИНГ: {movie['rating']}/10

📝 ОПИСАНИЕ:
{movie.get('description', 'Описание отсутствует')}
"""
        text_widget.insert("1.0", info)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(desc_window, text="Закрыть", command=desc_window.destroy).pack(pady=10)
        
        self.status_var.set(f"🎲 Случайный фильм: {movie['title']}")
    
    def clear_form(self):
        """Очистка формы ввода"""
        self.title_entry.delete(0, tk.END)
        self.director_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        self.description_text.delete("1.0", tk.END)
        
        self.add_btn.config(state=tk.NORMAL)
        self.update_btn.config(state=tk.DISABLED)
        
        if hasattr(self, 'editing_id'):
            delattr(self, 'editing_id')
    
    def apply_filters(self, event=None):
        """Применение фильтров"""
        try:
            genre = self.filter_genre.get()
            year = self.filter_year.get()
            rating = self.filter_rating.get()
            
            self.filtered_movies = []
            
            for movie in self.movies:
                genre_match = not genre or movie['genre'] == genre
                year_match = not year or str(movie['year']) == year
                rating_match = not rating or movie['rating'] >= float(rating)
                
                if genre_match and year_match and rating_match:
                    self.filtered_movies.append(movie)
            
            self.refresh_movie_list(self.filtered_movies)
            count = len(self.filtered_movies)
            self.status_var.set(f"🔍 Найдено фильмов: {count}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка фильтрации: {e}")
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.filter_genre.set("")
        self.filter_year.set("")
        self.filter_rating.set("")
        self.filtered_movies = []
        self.refresh_movie_list()
        self.status_var.set("🔄 Фильтры сброшены")
    
    def refresh_movie_list(self, movies_list=None):
        """Обновление списка фильмов"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Определяем источник данных
        if movies_list is not None:
            source = movies_list
        else:
            source = self.movies
        
        # Добавление фильмов в таблицу
        for movie in source:
            self.tree.insert("", tk.END, values=(
                movie['id'],
                movie['title'],
                movie['director'],
                movie['year'],
                movie['genre'],
                f"{movie['rating']:.1f}"
            ))
    
    def update_filters(self):
        """Обновление списков для фильтрации"""
        try:
            genres = sorted(set(movie['genre'] for movie in self.movies))
            years = sorted(set(str(movie['year']) for movie in self.movies), reverse=True)
            ratings = ["5", "6", "7", "8", "9"]
            
            self.genre_combo['values'] = [""] + genres
            self.year_combo['values'] = [""] + years
            self.rating_combo['values'] = [""] + ratings
            
        except Exception as e:
            print(f"Ошибка обновления фильтров: {e}")
    
    def update_count_label(self):
        """Обновление счетчика фильмов"""
        count = len(self.movies)
        self.count_label.config(text=f"📊 Всего фильмов в библиотеке: {count}")
    
    def load_movies(self):
        """Загрузка фильмов из JSON файла"""
        default_movies = [
            {
                "id": 1,
                "title": "Побег из Шоушенка",
                "director": "Фрэнк Дарабонт",
                "year": 1994,
                "genre": "Драма",
                "rating": 9.3,
                "description": "Два заключенных находят дружбу и искупление в тюремные годы.",
                "date_added": "2026-05-05 10:00:00"
            },
            {
                "id": 2,
                "title": "Крестный отец",
                "director": "Фрэнсис Форд Коппола",
                "year": 1972,
                "genre": "Криминал",
                "rating": 9.2,
                "description": "Глава мафиозной семьи передает контроль своему неохотно соглашающемуся сыну.",
                "date_added": "2026-05-05 10:00:00"
            },
            {
                "id": 3,
                "title": "Темный рыцарь",
                "director": "Кристофер Нолан",
                "year": 2008,
                "genre": "Боевик",
                "rating": 9.0,
                "description": "Бэтмен против Джокера в Готэме.",
                "date_added": "2026-05-05 10:00:00"
            },
            {
                "id": 4,
                "title": "Криминальное чтиво",
                "director": "Квентин Тарантино",
                "year": 1994,
                "genre": "Криминал",
                "rating": 8.9,
                "description": "Переплетающиеся истории наемных убийц, боксера и гангстеров.",
                "date_added": "2026-05-05 10:00:00"
            },
            {
                "id": 5,
                "title": "Властелин колец: Возвращение короля",
                "director": "Питер Джексон",
                "year": 2003,
                "genre": "Фэнтези",
                "rating": 8.9,
                "description": "Гэндальф и Арагорн ведут мир людей против сил Сарумана.",
                "date_added": "2026-05-05 10:00:00"
            }
        ]
        
        try:
            if not os.path.exists(self.data_file):
                self.movies = default_movies
                self.save_movies()
                self.status_var.set("📖 Загружены фильмы по умолчанию")
                return
            
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = f.read()
                    
                    if not data.strip():
                        self.movies = default_movies
                        self.status_var.set("⚠️ Файл пуст, загружены фильмы по умолчанию")
                        return
                    
                    loaded_data = json.loads(data)
                    
                    if not isinstance(loaded_data, list):
                        self.movies = default_movies
                        return
                    
                    self.movies = loaded_data
                    self.status_var.set(f"📂 Загружено {len(self.movies)} фильмов")
                    
            except json.JSONDecodeError:
                self.movies = default_movies
                self.status_var.set("⚠️ Ошибка JSON, загружены фильмы по умолчанию")
                
                backup_file = f"{self.data_file}.backup"
                try:
                    if os.path.exists(self.data_file):
                        os.rename(self.data_file, backup_file)
                except Exception:
                    pass
                    
        except Exception as e:
            self.movies = []
            self.status_var.set(f"❌ Ошибка загрузки: {e}")
    
    def save_movies(self):
        """Сохранение фильмов в JSON файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=2)
            self.status_var.set("💾 Фильмы сохранены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить фильмы: {e}")
    
    def export_movies(self):
        """Экспорт фильмов в JSON файл"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Экспорт фильмов"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.movies, f, ensure_ascii=False, indent=2)
                self.status_var.set(f"📤 Экспортировано {len(self.movies)} фильмов")
                messagebox.showinfo("Успех", f"Экспортировано {len(self.movies)} фильмов!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")


def main():
    try:
        root = tk.Tk()
        app = MovieLibrary(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Не удалось запустить приложение:\n{e}")


if __name__ == "__main__":
    main()
