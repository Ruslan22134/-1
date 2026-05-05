import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime
import os


class QuoteGenerator:
    """Графическое приложение для генерации случайных цитат с фильтрацией"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator - Ткаченко Руслан")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Файл для хранения цитат
        self.data_file = "quotes.json"
        self.quotes = []
        self.filtered_quotes = []
        
        # Загрузка цитат
        self.load_quotes()
        
        # Переменные для фильтрации
        self.filter_author = tk.StringVar()
        self.filter_topic = tk.StringVar()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление списка авторов и тем
        self.update_filters()
        
        # Отображение случайной цитаты при запуске
        self.show_random_quote()
    
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        # Основная рамка
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="📖 ГЕНЕРАТОР СЛУЧАЙНЫХ ЦИТАТ", 
                                 font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Рамка для отображения цитаты
        quote_frame = ttk.LabelFrame(main_frame, text="🌟 Случайная цитата", padding="20")
        quote_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Текст цитаты
        self.quote_text = tk.Text(quote_frame, height=8, width=70, wrap=tk.WORD,
                                   font=("Georgia", 14), relief=tk.SUNKEN, borderwidth=2)
        self.quote_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.quote_text.config(state=tk.DISABLED)
        
        # Информация об авторе и теме
        info_frame = ttk.Frame(quote_frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        self.author_label = ttk.Label(info_frame, text="Автор: ---", font=("Arial", 11, "italic"))
        self.author_label.pack(side=tk.LEFT, padx=10)
        
        self.topic_label = ttk.Label(info_frame, text="Тема: ---", font=("Arial", 11))
        self.topic_label.pack(side=tk.LEFT, padx=10)
        
        self.date_label = ttk.Label(info_frame, text="Добавлена: ---", font=("Arial", 9))
        self.date_label.pack(side=tk.RIGHT, padx=10)
        
        # Кнопки управления
        btn_frame = ttk.Frame(quote_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="🎲 СЛУЧАЙНАЯ ЦИТАТА", 
                   command=self.show_random_quote).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📋 КОПИРОВАТЬ", 
                   command=self.copy_quote).pack(side=tk.LEFT, padx=5)
        
        # Рамка фильтрации
        filter_frame = ttk.LabelFrame(main_frame, text="🔍 Фильтрация цитат", padding="10")
        filter_frame.pack(fill=tk.X, pady=10)
        
        # Фильтр по автору
        author_filter_frame = ttk.Frame(filter_frame)
        author_filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(author_filter_frame, text="Автор:").pack(side=tk.LEFT, padx=5)
        self.author_combo = ttk.Combobox(author_filter_frame, textvariable=self.filter_author, 
                                          width=30, state="readonly")
        self.author_combo.pack(side=tk.LEFT, padx=5)
        self.author_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
        ttk.Button(author_filter_frame, text="Очистить", 
                   command=self.clear_author_filter).pack(side=tk.LEFT, padx=5)
        
        # Фильтр по теме
        topic_filter_frame = ttk.Frame(filter_frame)
        topic_filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(topic_filter_frame, text="Тема:").pack(side=tk.LEFT, padx=5)
        self.topic_combo = ttk.Combobox(topic_filter_frame, textvariable=self.filter_topic, 
                                         width=30, state="readonly")
        self.topic_combo.pack(side=tk.LEFT, padx=5)
        self.topic_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
        ttk.Button(topic_filter_frame, text="Очистить", 
                   command=self.clear_topic_filter).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="🔄 СБРОСИТЬ ВСЕ ФИЛЬТРЫ", 
                   command=self.reset_filters).pack(pady=5)
        
        # Рамка добавления новой цитаты
        add_frame = ttk.LabelFrame(main_frame, text="➕ Добавить новую цитату", padding="10")
        add_frame.pack(fill=tk.X, pady=10)
        
        # Поле для текста цитаты
        ttk.Label(add_frame, text="Текст цитаты:").pack(anchor=tk.W, pady=2)
        self.new_quote_text = tk.Text(add_frame, height=4, width=70, wrap=tk.WORD)
        self.new_quote_text.pack(fill=tk.X, pady=5)
        
        # Поле для автора
        author_frame = ttk.Frame(add_frame)
        author_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(author_frame, text="Автор:").pack(side=tk.LEFT, padx=5)
        self.new_author_entry = ttk.Entry(author_frame, width=30)
        self.new_author_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(author_frame, text="Тема:").pack(side=tk.LEFT, padx=5)
        self.new_topic_entry = ttk.Entry(author_frame, width=30)
        self.new_topic_entry.pack(side=tk.LEFT, padx=5)
        
        # Кнопки добавления
        add_btn_frame = ttk.Frame(add_frame)
        add_btn_frame.pack(pady=5)
        
        ttk.Button(add_btn_frame, text="💾 ДОБАВИТЬ ЦИТАТУ", 
                   command=self.add_quote).pack(side=tk.LEFT, padx=5)
        ttk.Button(add_btn_frame, text="🗑 ОЧИСТИТЬ ФОРМУ", 
                   command=self.clear_add_form).pack(side=tk.LEFT, padx=5)
        
        # Рамка управления данными
        data_frame = ttk.LabelFrame(main_frame, text="📊 Управление данными", padding="10")
        data_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(data_frame, text="📋 ПОКАЗАТЬ ВСЕ ЦИТАТЫ", 
                   command=self.show_all_quotes).pack(side=tk.LEFT, padx=5)
        ttk.Button(data_frame, text="🗑 УДАЛИТЬ ПОСЛЕДНЮЮ", 
                   command=self.delete_last_quote).pack(side=tk.LEFT, padx=5)
        ttk.Button(data_frame, text="💾 СОХРАНИТЬ В JSON", 
                   command=self.save_quotes).pack(side=tk.LEFT, padx=5)
        ttk.Button(data_frame, text="📤 ЭКСПОРТ", 
                   command=self.export_quotes).pack(side=tk.LEFT, padx=5)
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=5)
        
        # Счетчик цитат
        self.count_label = ttk.Label(main_frame, text="", font=("Arial", 9))
        self.count_label.pack()
        self.update_count_label()
    
    def validate_quote(self, text, author, topic):
        """Валидация полей цитаты"""
        # Проверка на пустые строки
        if not text or not text.strip():
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return False
        
        if not author or not author.strip():
            messagebox.showerror("Ошибка", "Автор не может быть пустым!")
            return False
        
        if not topic or not topic.strip():
            messagebox.showerror("Ошибка", "Тема не может быть пустой!")
            return False
        
        # Проверка на минимальную длину
        if len(text.strip()) < 5:
            messagebox.showerror("Ошибка", "Текст цитаты слишком короткий (минимум 5 символов)!")
            return False
        
        if len(author.strip()) < 2:
            messagebox.showerror("Ошибка", "Имя автора слишком короткое (минимум 2 символа)!")
            return False
        
        return True
    
    def add_quote(self):
        """Добавление новой цитаты"""
        try:
            text = self.new_quote_text.get("1.0", tk.END).strip()
            author = self.new_author_entry.get().strip()
            topic = self.new_topic_entry.get().strip()
            
            # Валидация
            if not self.validate_quote(text, author, topic):
                return
            
            # Проверка на дубликат
            for quote in self.quotes:
                if quote['text'].lower() == text.lower():
                    messagebox.showerror("Ошибка", "Такая цитата уже существует!")
                    return
            
            # Создание новой цитаты
            new_quote = {
                'id': len(self.quotes) + 1,
                'text': text,
                'author': author,
                'topic': topic,
                'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.quotes.append(new_quote)
            self.save_quotes()
            self.clear_add_form()
            self.update_filters()
            self.update_count_label()
            self.status_var.set(f"✅ Цитата добавлена! Автор: {author}, Тема: {topic}")
            messagebox.showinfo("Успех", "Цитата успешно добавлена!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить цитату: {e}")
    
    def clear_add_form(self):
        """Очистка формы добавления"""
        self.new_quote_text.delete("1.0", tk.END)
        self.new_author_entry.delete(0, tk.END)
        self.new_topic_entry.delete(0, tk.END)
    
    def show_random_quote(self):
        """Отображение случайной цитаты с учетом фильтров"""
        try:
            # Определяем источник цитат (с фильтром или без)
            if self.filtered_quotes:
                source_quotes = self.filtered_quotes
            else:
                source_quotes = self.quotes
            
            if not source_quotes:
                self.quote_text.config(state=tk.NORMAL)
                self.quote_text.delete("1.0", tk.END)
                self.quote_text.insert("1.0", "Нет цитат, соответствующих фильтру!\n\nДобавьте новые цитаты или сбросьте фильтры.")
                self.quote_text.config(state=tk.DISABLED)
                self.author_label.config(text="Автор: ---")
                self.topic_label.config(text="Тема: ---")
                self.date_label.config(text="Добавлена: ---")
                return
            
            # Выбор случайной цитаты
            quote = random.choice(source_quotes)
            
            # Отображение цитаты
            self.quote_text.config(state=tk.NORMAL)
            self.quote_text.delete("1.0", tk.END)
            self.quote_text.insert("1.0", f"«{quote['text']}»")
            self.quote_text.config(state=tk.DISABLED)
            
            self.author_label.config(text=f"Автор: {quote['author']}")
            self.topic_label.config(text=f"Тема: {quote['topic']}")
            self.date_label.config(text=f"Добавлена: {quote.get('date_added', 'Неизвестно')}")
            
            self.status_var.set(f"🎲 Показана случайная цитата от {quote['author']}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось показать цитату: {e}")
    
    def copy_quote(self):
        """Копирование цитаты в буфер обмена"""
        try:
            text = self.quote_text.get("1.0", tk.END).strip()
            if text and text != "Нет цитат, соответствующих фильтру!":
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
                self.status_var.set("📋 Цитата скопирована в буфер обмена!")
                messagebox.showinfo("Успех", "Цитата скопирована!")
            else:
                messagebox.showwarning("Предупреждение", "Нет цитаты для копирования!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать: {e}")
    
    def apply_filters(self, event=None):
        """Применение фильтров по автору и теме"""
        try:
            author = self.filter_author.get()
            topic = self.filter_topic.get()
            
            self.filtered_quotes = []
            
            for quote in self.quotes:
                author_match = not author or quote['author'] == author
                topic_match = not topic or quote['topic'] == topic
                
                if author_match and topic_match:
                    self.filtered_quotes.append(quote)
            
            count = len(self.filtered_quotes)
            self.status_var.set(f"🔍 Найдено цитат: {count}")
            
            if count > 0:
                self.show_random_quote()
            else:
                self.show_random_quote()  # Покажет сообщение "Нет цитат"
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка фильтрации: {e}")
    
    def clear_author_filter(self):
        """Очистка фильтра по автору"""
        self.filter_author.set("")
        self.apply_filters()
    
    def clear_topic_filter(self):
        """Очистка фильтра по теме"""
        self.filter_topic.set("")
        self.apply_filters()
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.filter_author.set("")
        self.filter_topic.set("")
        self.filtered_quotes = []
        self.apply_filters()
        self.status_var.set("🔄 Все фильтры сброшены")
    
    def update_filters(self):
        """Обновление списков авторов и тем для фильтрации"""
        try:
            authors = sorted(set(quote['author'] for quote in self.quotes))
            topics = sorted(set(quote['topic'] for quote in self.quotes))
            
            self.author_combo['values'] = authors
            self.topic_combo['values'] = topics
            
        except Exception as e:
            print(f"Ошибка обновления фильтров: {e}")
    
    def show_all_quotes(self):
        """Отображение всех цитат в отдельном окне"""
        try:
            if not self.quotes:
                messagebox.showinfo("Информация", "Нет добавленных цитат!")
                return
            
            # Создание нового окна
            quotes_window = tk.Toplevel(self.root)
            quotes_window.title("Все цитаты")
            quotes_window.geometry("800x500")
            
            # Текстовое поле для отображения
            text_widget = tk.Text(quotes_window, wrap=tk.WORD, font=("Georgia", 10))
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Скроллбар
            scrollbar = ttk.Scrollbar(text_widget)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_widget.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=text_widget.yview)
            
            # Вывод всех цитат
            for i, quote in enumerate(self.quotes, 1):
                text_widget.insert(tk.END, f"{i}. \"{quote['text']}\"\n")
                text_widget.insert(tk.END, f"   Автор: {quote['author']} | Тема: {quote['topic']}\n")
                text_widget.insert(tk.END, f"   Добавлена: {quote.get('date_added', 'Неизвестно')}\n")
                text_widget.insert(tk.END, "-" * 70 + "\n\n")
            
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось показать цитаты: {e}")
    
    def delete_last_quote(self):
        """Удаление последней добавленной цитаты"""
        try:
            if not self.quotes:
                messagebox.showwarning("Предупреждение", "Нет цитат для удаления!")
                return
            
            if messagebox.askyesno("Подтверждение", f"Удалить последнюю цитату?\n\n\"{self.quotes[-1]['text'][:100]}...\""):
                deleted = self.quotes.pop()
                self.save_quotes()
                self.update_filters()
                self.update_count_label()
                self.apply_filters()
                self.status_var.set(f"🗑 Удалена цитата от {deleted['author']}")
                messagebox.showinfo("Успех", "Цитата удалена!")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить цитату: {e}")
    
    def update_count_label(self):
        """Обновление счетчика цитат"""
        count = len(self.quotes)
        self.count_label.config(text=f"📊 Всего цитат в базе: {count}")
    
    def load_quotes(self):
        """Загрузка цитат из JSON файла с обработкой ошибок"""
        try:
            # Пример цитат по умолчанию, если файл пустой
            default_quotes = [
                {
                    "id": 1,
                    "text": "Будьте тем изменением, которое хотите видеть в мире.",
                    "author": "Махатма Ганди",
                    "topic": "Мотивация",
                    "date_added": "2026-05-05 10:00:00"
                },
                {
                    "id": 2,
                    "text": "Жизнь - это то, что с тобой происходит, пока ты строишь планы.",
                    "author": "Джон Леннон",
                    "topic": "Жизнь",
                    "date_added": "2026-05-05 10:00:00"
                },
                {
                    "id": 3,
                    "text": "Успех - это способность идти от неудачи к неудаче, не теряя энтузиазма.",
                    "author": "Уинстон Черчилль",
                    "topic": "Успех",
                    "date_added": "2026-05-05 10:00:00"
                },
                {
                    "id": 4,
                    "text": "Единственный способ сделать великую работу - любить то, что ты делаешь.",
                    "author": "Стив Джобс",
                    "topic": "Работа",
                    "date_added": "2026-05-05 10:00:00"
                },
                {
                    "id": 5,
                    "text": "Знание - сила.",
                    "author": "Фрэнсис Бэкон",
                    "topic": "Знание",
                    "date_added": "2026-05-05 10:00:00"
                }
            ]
            
            if not os.path.exists(self.data_file):
                self.quotes = default_quotes
                self.save_quotes()
                self.status_var.set("📖 Загружены цитаты по умолчанию")
                return
            
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = f.read()
                    
                    if not data.strip():
                        self.quotes = default_quotes
                        self.status_var.set("⚠️ Файл пуст, загружены цитаты по умолчанию")
                        return
                    
                    loaded_data = json.loads(data)
                    
                    if not isinstance(loaded_data, list):
                        self.quotes = default_quotes
                        self.status_var.set("⚠️ Неверный формат, загружены цитаты по умолчанию")
                        return
                    
                    self.quotes = loaded_data
                    self.status_var.set(f"📂 Загружено {len(self.quotes)} цитат")
                    
            except json.JSONDecodeError as e:
                self.quotes = default_quotes
                self.status_var.set(f"⚠️ Ошибка JSON, загружены цитаты по умолчанию")
                
                # Создание резервной копии
                backup_file = f"{self.data_file}.backup"
                try:
                    if os.path.exists(self.data_file):
                        os.rename(self.data_file, backup_file)
                        self.status_var.set(f"📁 Создана резервная копия: {backup_file}")
                except Exception:
                    pass
                    
        except Exception as e:
            self.quotes = []
            self.status_var.set(f"❌ Ошибка загрузки: {e}")
            messagebox.showerror("Ошибка", f"Не удалось загрузить цитаты:\n{e}")
    
    def save_quotes(self):
        """Сохранение цитат в JSON файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.quotes, f, ensure_ascii=False, indent=2)
            self.status_var.set("💾 Цитаты сохранены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить цитаты: {e}")
    
    def export_quotes(self):
        """Экспорт цитат в JSON файл"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Экспорт цитат"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.quotes, f, ensure_ascii=False, indent=2)
                self.status_var.set(f"📤 Цитаты экспортированы в {filename}")
                messagebox.showinfo("Успех", f"Экспортировано {len(self.quotes)} цитат!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")


def main():
    try:
        root = tk.Tk()
        app = QuoteGenerator(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Не удалось запустить приложение:\n{e}")


if __name__ == "__main__":
    main()
