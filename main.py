import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
from datetime import datetime
import os


class PasswordGenerator:
    """Графическое приложение для генерации случайных паролей с историей"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("800x650")
        self.root.resizable(True, True)
        
        # Настройка стилей
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Password.TEntry", font=("Courier", 14))
        
        # Файл для хранения истории
        self.history_file = "password_history.json"
        self.history = []
        
        # Загрузка истории
        self.load_history()
        
        # Переменные для настроек
        self.password_length = tk.IntVar(value=12)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление истории
        self.refresh_history()
    
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        # Основная рамка
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="🔐 ГЕНЕРАТОР СЛУЧАЙНЫХ ПАРОЛЕЙ", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Рамка настроек
        settings_frame = ttk.LabelFrame(main_frame, text="Настройки пароля", padding="15")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Ползунок длины пароля
        length_frame = ttk.Frame(settings_frame)
        length_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(length_frame, text="Длина пароля:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.length_scale = ttk.Scale(
            length_frame, from_=4, to=32, orient=tk.HORIZONTAL,
            variable=self.password_length, command=self.update_length_label
        )
        self.length_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        self.length_label = ttk.Label(length_frame, text="12", font=("Arial", 10, "bold"))
        self.length_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(length_frame, text="символов").pack(side=tk.LEFT, padx=5)
        
        # Чекбоксы для выбора символов
        checkbox_frame = ttk.LabelFrame(settings_frame, text="Типы символов", padding="10")
        checkbox_frame.pack(fill=X, pady=10)
        
        # Создаем два столбца для чекбоксов
        left_col = ttk.Frame(checkbox_frame)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        right_col = ttk.Frame(checkbox_frame)
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        ttk.Checkbutton(
            left_col, text="🔤 Заглавные буквы (A-Z)",
            variable=self.use_uppercase, command=self.validate_settings
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Checkbutton(
            left_col, text="🔡 Строчные буквы (a-z)",
            variable=self.use_lowercase, command=self.validate_settings
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Checkbutton(
            right_col, text="🔢 Цифры (0-9)",
            variable=self.use_digits, command=self.validate_settings
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Checkbutton(
            right_col, text="✨ Спецсимволы (!@#$%^&*)",
            variable=self.use_special, command=self.validate_settings
        ).pack(anchor=tk.W, pady=5)
        
        # Кнопка генерации
        generate_btn = ttk.Button(
            settings_frame, text="🎲 СГЕНЕРИРОВАТЬ ПАРОЛЬ",
            command=self.generate_password
        )
        generate_btn.pack(pady=15)
        
        # Рамка отображения пароля
        display_frame = ttk.LabelFrame(main_frame, text="Сгенерированный пароль", padding="15")
        display_frame.pack(fill=tk.X, pady=10)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            display_frame, textvariable=self.password_var,
            font=("Courier", 14), state="readonly", justify="center"
        )
        self.password_entry.pack(fill=tk.X, padx=10, pady=10)
        
        # Рамка для кнопок копирования
        copy_frame = ttk.Frame(display_frame)
        copy_frame.pack(pady=5)
        
        copy_btn = ttk.Button(copy_frame, text="📋 Копировать в буфер", command=self.copy_to_clipboard)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Индикатор сложности
        self.strength_label = ttk.Label(copy_frame, text="", font=("Arial", 9))
        self.strength_label.pack(side=tk.LEFT, padx=10)
        
        # Рамка истории
        history_frame = ttk.LabelFrame(main_frame, text="История паролей", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Таблица истории
        columns = ("ID", "Пароль", "Длина", "Символы", "Дата")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)
        
        self.tree.heading("ID", text="№")
        self.tree.heading("Пароль", text="Пароль")
        self.tree.heading("Длина", text="Длина")
        self.tree.heading("Символы", text="Использованные символы")
        self.tree.heading("Дата", text="Дата создания")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Пароль", width=200, anchor=tk.CENTER)
        self.tree.column("Длина", width=70, anchor=tk.CENTER)
        self.tree.column("Символы", width=200, anchor=tk.CENTER)
        self.tree.column("Дата", width=150, anchor=tk.CENTER)
        
        # Скроллбар для таблицы
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопки управления историей
        btn_frame = ttk.Frame(history_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="🗑 Очистить историю", command=self.clear_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="💾 Сохранить историю", command=self.save_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 Обновить", command=self.refresh_history).pack(side=tk.LEFT, padx=5)
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=5)
    
    def update_length_label(self, event=None):
        """Обновление отображения длины пароля"""
        self.length_label.config(text=str(int(self.password_length.get())))
    
    def validate_settings(self):
        """Проверка, что выбран хотя бы один тип символов"""
        if not (self.use_uppercase.get() or self.use_lowercase.get() or 
                self.use_digits.get() or self.use_special.get()):
            messagebox.showwarning(
                "Предупреждение",
                "Выберите хотя бы один тип символов!\nУстанавливаю строчные буквы по умолчанию."
            )
            self.use_lowercase.set(True)
    
    def check_password_strength(self, password):
        """Оценка сложности пароля"""
        score = 0
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in "!@#$%^&*" for c in password):
            score += 1
        
        if score <= 2:
            return "🔴 Слабый"
        elif score <= 4:
            return "🟡 Средний"
        else:
            return "🟢 Сильный"
    
    def generate_password(self):
        """Генерация случайного пароля на основе настроек"""
        # Валидация длины
        length = int(self.password_length.get())
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля - 4 символа!")
            self.password_length.set(4)
            length = 4
        elif length > 32:
            messagebox.showerror("Ошибка", "Максимальная длина пароля - 32 символа!")
            self.password_length.set(32)
            length = 32
        
        # Проверка выбора символов
        self.validate_settings()
        
        # Формирование пула символов
        char_pool = ""
        used_types = []
        
        if self.use_uppercase.get():
            char_pool += string.ascii_uppercase
            used_types.append("A-Z")
        if self.use_lowercase.get():
            char_pool += string.ascii_lowercase
            used_types.append("a-z")
        if self.use_digits.get():
            char_pool += string.digits
            used_types.append("0-9")
        if self.use_special.get():
            char_pool += "!@#$%^&*"
            used_types.append("!@#$%^&*")
        
        # Гарантируем, что пароль содержит хотя бы один символ каждого выбранного типа
        password_chars = []
        
        # Добавляем по одному символу каждого типа
        if self.use_uppercase.get():
            password_chars.append(random.choice(string.ascii_uppercase))
        if self.use_lowercase.get():
            password_chars.append(random.choice(string.ascii_lowercase))
        if self.use_digits.get():
            password_chars.append(random.choice(string.digits))
        if self.use_special.get():
            password_chars.append(random.choice("!@#$%^&*"))
        
        # Заполняем остальные символы случайными из пула
        remaining_length = length - len(password_chars)
        if remaining_length > 0:
            password_chars.extend(random.choice(char_pool) for _ in range(remaining_length))
        
        # Перемешиваем символы
        random.shuffle(password_chars)
        password = ''.join(password_chars)
        
        # Оценка сложности
        strength = self.check_password_strength(password)
        self.strength_label.config(text=f"Сложность: {strength}")
        
        # Сохранение в историю
        self.save_to_history(password, length, ', '.join(used_types))
        
        # Отображение пароля
        self.password_var.set(password)
        self.status_var.set(f"✅ Пароль сгенерирован! Сложность: {strength}")
    
    def save_to_history(self, password, length, char_types):
        """Сохранение пароля в историю"""
        history_entry = {
            'id': len(self.history) + 1,
            'password': password,
            'length': length,
            'char_types': char_types,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(history_entry)
        self.save_history()
        self.refresh_history()
    
    def refresh_history(self):
        """Обновление таблицы истории"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление записей
        for entry in reversed(self.history):  # Показываем новые сверху
            self.tree.insert("", 0, values=(
                entry['id'],
                entry['password'],
                entry['length'],
                entry['char_types'],
                entry['date']
            ))
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.refresh_history()
            self.status_var.set("🗑 История очищена")
            messagebox.showinfo("Успех", "История очищена!")
    
    def copy_to_clipboard(self):
        """Копирование пароля в буфер обмена"""
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.status_var.set("📋 Пароль скопирован в буфер обмена!")
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Предупреждение", "Сначала сгенерируйте пароль!")
    
    def load_history(self):
        """Загрузка истории из JSON файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                self.status_var.set(f"📂 Загружено {len(self.history)} записей из истории")
            except (json.JSONDecodeError, FileNotFoundError):
                self.history = []
                self.status_var.set("⚠️ Ошибка загрузки истории")
        else:
            self.history = []
            self.status_var.set("🆕 Новая сессия")
    
    def save_history(self):
        """Сохранение истории в JSON файл"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")
            self.status_var.set("❌ Ошибка сохранения истории")


def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
