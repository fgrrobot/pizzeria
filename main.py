import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import re


class PizzaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍕Пиццерия")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2C3E50')

        self.style = {
            'bg': '#2C3E50',
            'tab_bg': '#34495E',
            'tab_active': '#E74C3C',
            'tab_text': '#ECF0F1',
            'card': '#34495E',
            'accent': '#E74C3C',
            'text': '#ECF0F1'
        }

        self.user = None
        self.auth_frame = None
        self.cart_items = []
        self.menu_categories = {
            "Пиццы": [
                {"name": "Маргарита", "desc": "Сыр моцарелла, томатный соус, базилик", "price": "450₽", "image": "images/Маргарита.jpg"},
                {"name": "Пепперони", "desc": "Пепперони, моцарелла, томатный соус", "price": "550₽", "image": "images/Пепперони.jpg"},
                {"name": "Гавайская", "desc": "Ветчина, ананасы, моцарелла, соус", "price": "500₽", "image": "images/Гавайская.jpg"},
            ],
            "Закуски": [
                {"name": "Картофель фри", "desc": "Хрустящий картофель с соусом", "price": "180₽", "image": "images/картошка фри.jpeg"},
                {"name": "Наггетсы", "desc": "Куриные наггетсы (6 шт)", "price": "220₽", "image": "images/нагетсы.jpeg"},
                {"name": "Картофель по деревенски", "desc": "Хрустящий картофель с соусом", "price": "150₽", "image": "images/картошка по деревенски.jpeg"}
            ],
            "Напитки": [
                {"name": "Кола", "desc": "0.5 л", "price": "120₽", "image": "images/кола.jpeg"},
                {"name": "Сок", "desc": "0.5 л", "price": "120₽", "image": "images/яблочный сок.jpeg"},
                {"name": "Вода", "desc": "Негазированная, 0.5 л", "price": "80₽", "image": "images/вода.jpeg"}
            ]
        }
        self.current_menu_category = "Пиццы"
        self.active_tab = 0
        self.tab_frames = []
        self.tab_buttons = []
        self.category_buttons = {}

        self.load_users()
        if self.user:
            self.setup_interface()
        else:
            self.show_auth_screen()

    def load_users(self):
        self.users_db = {}
        if os.path.exists("users.json"):
            try:
                with open("users.json", "r", encoding="utf-8") as f:
                    self.users_db = json.load(f)
            except:
                self.users_db = {}
        self.user = None

    def save_users(self):
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(self.users_db, f, ensure_ascii=False, indent=4)

    def validate_phone(self, phone):
        cleaned = re.sub(r'\D', '', phone)
        if len(cleaned) < 10:
            return None
        if cleaned.startswith('8'):
            cleaned = '7' + cleaned[1:]
        elif not cleaned.startswith('7'):
            cleaned = '7' + cleaned
        if len(cleaned) != 11:
            return None
        return cleaned

    def show_auth_screen(self):
        if self.auth_frame:
            self.auth_frame.destroy()

        self.auth_frame = tk.Frame(self.root, bg=self.style['bg'])
        self.auth_frame.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(self.auth_frame, text="🍕 Добро пожаловать!", font=("Arial", 24, "bold"),
                         bg=self.style['bg'], fg=self.style['accent'])
        title.pack(pady=40)

        self.auth_mode = tk.StringVar(value="login")
        mode_frame = tk.Frame(self.auth_frame, bg=self.style['bg'])
        mode_frame.pack(pady=10)

        tk.Radiobutton(mode_frame, text="Вход", variable=self.auth_mode, value="login",
                       bg=self.style['bg'], fg=self.style['text'], selectcolor=self.style['accent'],
                       font=("Arial", 12), command=self.toggle_auth_mode).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="Регистрация", variable=self.auth_mode, value="register",
                       bg=self.style['bg'], fg=self.style['text'], selectcolor=self.style['accent'],
                       font=("Arial", 12), command=self.toggle_auth_mode).pack(side=tk.LEFT, padx=10)

        form_frame = tk.Frame(self.auth_frame, bg=self.style['card'], relief='raised', bd=2, padx=30, pady=30)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Номер телефона:", bg=self.style['card'], fg=self.style['text'],
                 font=("Arial", 12)).pack(anchor='w')
        self.phone_entry = tk.Entry(form_frame, font=("Arial", 14), width=25)
        self.phone_entry.pack(pady=5)

        tk.Label(form_frame, text="Имя (только при регистрации):", bg=self.style['card'], fg=self.style['text'],
                 font=("Arial", 12)).pack(anchor='w', pady=(10, 0))
        self.name_entry = tk.Entry(form_frame, font=("Arial", 14), width=25)
        self.name_entry.pack(pady=5)

        self.submit_btn = tk.Button(form_frame, text="Войти", font=("Arial", 14, "bold"),
                                    bg=self.style['accent'], fg="white", command=self.handle_auth)
        self.submit_btn.pack(pady=20)

        self.toggle_auth_mode()

    def toggle_auth_mode(self):
        mode = self.auth_mode.get()
        if mode == "login":
            self.name_entry.config(state='disabled')
            self.submit_btn.config(text="Войти")
        else:
            self.name_entry.config(state='normal')
            self.submit_btn.config(text="Зарегистрироваться")

    def handle_auth(self):
        phone_input = self.phone_entry.get().strip()
        phone = self.validate_phone(phone_input)
        if not phone:
            messagebox.showerror("Ошибка", "Введите корректный номер телефона (10+ цифр)")
            return

        mode = self.auth_mode.get()
        if mode == "register":
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите имя")
                return
            if phone in self.users_db:
                messagebox.showerror("Ошибка", "Пользователь с таким номером уже существует")
                return
            self.users_db[phone] = {"name": name, "phone": phone}
            self.save_users()
            self.user = self.users_db[phone]
            messagebox.showinfo("Успех", f"Регистрация завершена, {name}!")
            self.auth_frame.pack_forget()
            self.setup_interface()
        else:
            if phone not in self.users_db:
                messagebox.showerror("Ошибка", "Пользователь не найден. Зарегистрируйтесь.")
                return
            self.user = self.users_db[phone]
            messagebox.showinfo("Успех", f"Добро пожаловать, {self.user['name']}!")
            self.auth_frame.pack_forget()
            self.setup_interface()

    def setup_interface(self):
        tab_bar = tk.Frame(self.root, bg=self.style['bg'])
        tab_bar.pack(fill=tk.X, padx=10, pady=(10, 0))

        content_area = tk.Frame(self.root, bg=self.style['bg'])
        content_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tabs = [
            ("🍕 Меню", self.setup_menu),
            ("🔧 Кастомная Пицца", self.setup_builder),
            ("🛒 Корзина", self.setup_cart)
        ]

        for index, (tab_name, _) in enumerate(tabs):
            tab_btn = tk.Button(tab_bar, text=tab_name,
                              font=('Arial', 10, 'bold'),
                              bg=self.style['tab_bg'], fg=self.style['tab_text'],
                              relief='flat', bd=0,
                              command=lambda idx=index: self.select_tab(idx))
            tab_btn.pack(side=tk.LEFT, padx=2)
            self.tab_buttons.append(tab_btn)

        for tab_name, tab_creator in tabs:
            tab_content = tk.Frame(content_area, bg=self.style['bg'])
            tab_creator(tab_content)
            self.tab_frames.append(tab_content)

        self.select_tab(0)

    def select_tab(self, tab_index):
        for frame in self.tab_frames:
            frame.pack_forget()

        for btn_index, button in enumerate(self.tab_buttons):
            if btn_index == tab_index:
                button.configure(bg=self.style['tab_active'], fg='white')
            else:
                button.configure(bg=self.style['tab_bg'], fg=self.style['tab_text'])

        self.tab_frames[tab_index].pack(fill=tk.BOTH, expand=True)
        self.active_tab = tab_index

    def setup_menu(self, parent):
        header = tk.Label(parent, text="🍕 МЕНЮ",
                         font=('Arial', 20, 'bold'),
                         bg=self.style['bg'], fg=self.style['accent'])
        header.pack(pady=20)

        category_bar = tk.Frame(parent, bg=self.style['bg'])
        category_bar.pack(pady=(0, 15))

        for cat in ["Пиццы", "Закуски", "Напитки"]:
            btn = tk.Button(category_bar, text=cat,
                            font=('Arial', 11, 'bold'),
                            bg=self.style['tab_bg'], fg=self.style['tab_text'],
                            relief='flat', bd=0,
                            command=lambda c=cat: self.switch_menu_category(c))
            btn.pack(side=tk.LEFT, padx=10)
            self.category_buttons[cat] = btn

        main_container = tk.Frame(parent, bg=self.style['bg'])
        main_container.pack(fill=tk.BOTH, expand=True)

        scroll_canvas = tk.Canvas(main_container, bg=self.style['bg'], highlightthickness=0)
        scroll_bar = tk.Scrollbar(main_container, orient=tk.VERTICAL, command=scroll_canvas.yview)
        self.menu_items_container = tk.Frame(scroll_canvas, bg=self.style['bg'])

        self.menu_items_container.bind(
            "<Configure>",
            lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        )

        scroll_canvas.create_window((0, 0), window=self.menu_items_container, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scroll_bar.set)

        scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20))

        self.switch_menu_category("Пиццы")

    def switch_menu_category(self, category):
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.configure(bg=self.style['tab_active'], fg='white')
            else:
                btn.configure(bg=self.style['tab_bg'], fg=self.style['tab_text'])

        for widget in self.menu_items_container.winfo_children():
            widget.destroy()

        self.current_menu_category = category
        items = self.menu_categories.get(category, [])

        for position, pizza_item in enumerate(items):
            item_frame = self.create_menu_item(self.menu_items_container, pizza_item)
            row_num, col_num = position // 3, position % 3
            item_frame.grid(row=row_num, column=col_num, padx=10, pady=10)

        for i in range(3):
            self.menu_items_container.grid_columnconfigure(i, weight=1)

    def create_menu_item(self, parent, pizza_data):
        item_frame = tk.Frame(parent, bg=self.style['card'], relief='raised', bd=2, width=280, height=400)
        item_frame.pack_propagate(False)

        try:
            pizza_image = Image.open(pizza_data["image"])
            pizza_image = pizza_image.resize((150, 150), Image.Resampling.LANCZOS)
            photo_img = ImageTk.PhotoImage(pizza_image)
        except:
            photo_img = None

        image_display = tk.Label(item_frame, image=photo_img, bg=self.style['card'], width=150, height=150)
        if photo_img:
            image_display.image = photo_img
        image_display.pack(pady=10)

        name_display = tk.Label(
            item_frame, text=pizza_data["name"],
            font=('Arial', 14, 'bold'),
            bg=self.style['card'], fg=self.style['accent'],
            wraplength=250, justify='center'
        )
        name_display.pack(pady=(5, 5))

        desc_display = tk.Label(
            item_frame, text=pizza_data["desc"],
            font=('Arial', 9),
            bg=self.style['card'], fg=self.style['text'],
            wraplength=250, justify='center'
        )
        desc_display.pack(pady=5)

        price_display = tk.Label(
            item_frame, text=pizza_data["price"],
            font=('Arial', 16, 'bold'),
            bg=self.style['card'], fg=self.style['accent']
        )
        price_display.pack(pady=5)

        add_button = tk.Button(
            item_frame, text="➕ Добавить",
            font=('Arial', 10, 'bold'),
            bg=self.style['accent'], fg='white',
            command=lambda: self.cart_add(pizza_data)
        )
        add_button.pack(pady=10, padx=20, fill=tk.X, ipady=3)

        return item_frame

    def setup_builder(self, parent):
        builder_title = tk.Label(parent, text="🔧 КАСТОМНАЯ ПИЦЦА",
                         font=('Arial', 18, 'bold'),
                         bg=self.style['bg'], fg=self.style['accent'])
        builder_title.pack(pady=20)

        size_selector = tk.LabelFrame(parent, text="📏 Размер пиццы",
                                   font=('Arial', 12, 'bold'),
                                   bg=self.style['card'], fg=self.style['text'],
                                   padx=15, pady=15)
        size_selector.pack(fill=tk.X, padx=20, pady=10)

        self.pizza_size = tk.StringVar(value="medium")
        size_options = [
            ("Маленькая (25см) - 350₽", "small"),
            ("Средняя (30см) - 500₽", "medium"),
            ("Большая (35см) - 650₽", "large")
        ]

        for label_text, size_value in size_options:
            size_btn = tk.Radiobutton(size_selector, text=label_text, value=size_value,
                                variable=self.pizza_size,
                                font=('Arial', 10),
                                bg=self.style['card'], fg=self.style['text'],
                                selectcolor=self.style['accent'])
            size_btn.pack(anchor='w', pady=2)

        toppings_selector = tk.LabelFrame(parent, text="🍅 Начинки (+50₽)",
                                       font=('Arial', 12, 'bold'),
                                       bg=self.style['card'], fg=self.style['text'],
                                       padx=15, pady=15)
        toppings_selector.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.topping_selection = {}
        available_toppings = ["Пепперони", "Грибы", "Сыр", "Ветчина", "Ананасы", "Лук"]

        for pos, topping_name in enumerate(available_toppings):
            topping_var = tk.BooleanVar()
            topping_cb = tk.Checkbutton(toppings_selector, text=topping_name, variable=topping_var,
                                font=('Arial', 10),
                                bg=self.style['card'], fg=self.style['text'],
                                selectcolor=self.style['accent'])
            topping_cb.grid(row=pos // 3, column=pos % 3, sticky='w', padx=10, pady=5)
            self.topping_selection[topping_name] = topping_var

        build_btn = tk.Button(parent, text="🍕 СОЗДАТЬ ПИЦЦУ",
                               font=('Arial', 14, 'bold'),
                               bg=self.style['accent'], fg='white',
                               command=self.build_custom_pizza)
        build_btn.pack(pady=20, ipadx=10, ipady=5)

    def setup_cart(self, parent):
        cart_header = tk.Label(parent, text="🛒 ВАША КОРЗИНА",
                         font=('Arial', 18, 'bold'),
                         bg=self.style['bg'], fg=self.style['accent'])
        cart_header.pack(pady=20)

        list_container = tk.Frame(parent, bg=self.style['card'], relief='sunken', bd=2)
        list_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.cart_display = tk.Listbox(list_container, font=('Arial', 11),
                                       bg=self.style['card'], fg=self.style['text'],
                                       selectbackground=self.style['accent'])

        list_scroll = tk.Scrollbar(list_container, orient=tk.VERTICAL)
        self.cart_display.config(yscrollcommand=list_scroll.set)
        list_scroll.config(command=self.cart_display.yview)

        self.cart_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        bottom_panel = tk.Frame(parent, bg=self.style['bg'])
        bottom_panel.pack(fill=tk.X, padx=20, pady=10)

        self.total_display = tk.Label(bottom_panel, text="Итого: 0₽",
                                    font=('Arial', 16, 'bold'),
                                    bg=self.style['bg'], fg=self.style['accent'])
        self.total_display.pack(side=tk.LEFT)

        action_buttons = tk.Frame(bottom_panel, bg=self.style['bg'])
        action_buttons.pack(side=tk.RIGHT)

        clear_btn = tk.Button(action_buttons, text="🗑️ Очистить",
                              font=('Arial', 10, 'bold'),
                              bg='#E74C3C', fg='white',
                              command=self.empty_cart)
        clear_btn.pack(side=tk.LEFT, padx=5)

        order_btn = tk.Button(action_buttons, text="✅ Заказать",
                              font=('Arial', 10, 'bold'),
                              bg='#27AE60', fg='white',
                              command=self.finalize_order)
        order_btn.pack(side=tk.LEFT, padx=5)

    def cart_add(self, pizza_item):
        self.cart_items.append(pizza_item)
        self.refresh_cart()
        messagebox.showinfo("Успех", f"'{pizza_item['name']}' добавлено в корзину!")

    def build_custom_pizza(self):
        size_pricing = {'small': 350, 'medium': 500, 'large': 650}
        base_cost = size_pricing[self.pizza_size.get()]

        chosen_toppings = [name for name, var in self.topping_selection.items() if var.get()]
        toppings_cost = len(chosen_toppings) * 50
        final_price = base_cost + toppings_cost

        size_labels = {'small': 'Маленькая', 'medium': 'Средняя', 'large': 'Большая'}
        custom_name = f"Кастомная {size_labels[self.pizza_size.get()]} пицца"

        if chosen_toppings:
            custom_name += f" с {', '.join(chosen_toppings)}"

        custom_pizza = {
            "name": custom_name,
            "desc": "Ваша уникальная пицца",
            "price": f"{final_price}₽"
        }

        self.cart_add(custom_pizza)

    def refresh_cart(self):
        self.cart_display.delete(0, tk.END)

        cart_total = 0
        for cart_item in self.cart_items:
            display_line = f"{cart_item['name']} - {cart_item['price']}"
            self.cart_display.insert(tk.END, display_line)
            item_price = int(cart_item['price'].replace('₽', ''))
            cart_total += item_price

        self.total_display.config(text=f"Итого: {cart_total}₽")

    def empty_cart(self):
        self.cart_items.clear()
        self.refresh_cart()

    def finalize_order(self):
        if not self.cart_items:
            messagebox.showwarning("Ошибка", "Корзина пуста!")
            return

        order_total = sum(int(item['price'].replace('₽', '')) for item in self.cart_items)
        message = f"✅ Заказ оформлен, {self.user['name']}!\n" \
                  f"🍕 Позиций: {len(self.cart_items)}\n" \
                  f"💵 Сумма: {order_total}₽\n" \
                  f"📞 Свяжемся по: {self.user['phone']}\n" \
                  f"⏰ Доставка: 30-45 минут"
        messagebox.showinfo("Заказ принят!", message)
        self.empty_cart()


if __name__ == "__main__":
    window = tk.Tk()
    app_instance = PizzaApp(window)
    window.mainloop()