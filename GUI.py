import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from Game import Game

main_frame = None

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Меню игры")
        self.root.attributes('-fullscreen', True)  # Полноэкранный режим
        self.players = tk.IntVar()
        self.board_size = tk.IntVar()
        self.computer_mode = tk.BooleanVar()
        self.computer_difficulty = tk.StringVar()
        self.create_main_menu()
        self.game = None

    def get_non_empty_string(self, prompt, parent):
        while True:
            player_name = simpledialog.askstring("Введите никнейм", prompt, parent=parent)
            if player_name is not None and player_name.strip() != "":
                return player_name

    def start_game(self, mode, computer_difficulty, count_players, map_grid):
        player_names = []
        root = tk.Tk()
        root.attributes('-alpha', 0)
        root.geometry('250x250+530+270')
        root.update_idletasks()

        for i in range(count_players):
            prompt = f"Игрок {i + 1}, введите свой никнейм:"
            player_name = self.get_non_empty_string(prompt, parent=root)
            player_names.append(player_name)

        self.game = Game(mode, computer_difficulty, count_players, map_grid, player_names, self.root)

    def create_main_menu(self):
        global main_frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        center_frame = ttk.Frame(main_frame)
        center_frame.grid(row=0, column=0, padx=10, pady=10)

        button_style = ttk.Style()
        button_style.configure("Custom.TButton", font=("Helvetica", 14))
        button_style.configure("Custom.TButton", padding=10)

        label_style = ttk.Style()
        label_style.configure("Custom.TLabel", font=("Helvetica", 16))

        players_style = ttk.Style()
        players_style.configure("Custom.TMenubutton", font=("Helvetica", 12), background="lightblue", foreground="black")

        ttk.Label(center_frame, text="Выберите режим игры", style="Custom.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 10))
        ttk.Button(center_frame, text="Играть с игроками",  command=lambda:self.create_player_options(), width=20, style="Custom.TButton").grid(row=1, column=0, padx=5, pady=10)
        ttk.Button(center_frame, text="Играть с компьютером",  command=lambda:self.create_computer_options(), width=22, style="Custom.TButton").grid(row=1, column=1, padx=5, pady=10)
        ttk.Button(self.root, text="Выход", command=self.on_exit_button_click, style="Custom.TButton").grid(row=0, column=1, sticky=tk.NE)
        ttk.Button(self.root, text="Таблица рекордов", command=self.create_score_table, style="Custom.TButton").grid(row=0, column=0, sticky=tk.NE)

    def create_player_options(self):
        global main_frame
        main_frame.grid_forget()

        player_options_frame = ttk.Frame(self.root, padding="20")
        player_options_frame.grid(row=0, column=0)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        center_frame = ttk.Frame(player_options_frame)
        center_frame.grid(row=0, column=0, padx=10, pady=10)

        players_label = ttk.Label(center_frame, text="Количество игроков:", style="Custom.TLabel")
        players_label.grid(row=0, column=0, pady=(0, 10))
        players_values = [2, 3, 4]
        self. players.set(players_values[0])

        players_menu = ttk.OptionMenu(center_frame, self.players, players_values[0], *players_values,
                                      style="Custom.TMenubutton")
        players_menu.grid(row=0, column=1, pady=(0, 10))

        board_size_label = ttk.Label(center_frame, text="Размер поля:", style="Custom.TLabel")
        board_size_label.grid(row=1, column=0, pady=(0, 10), sticky="W")
        board_size_values = [8, 10, 12, 15, 20]
        self.board_size.set(board_size_values[0])

        # Применяем стиль "Custom.TMenubutton" к OptionMenu
        board_size_menu = ttk.OptionMenu(center_frame, self.board_size, board_size_values[0], *board_size_values,
                                         style="Custom.TMenubutton")
        board_size_menu.grid(row=1, column=1, pady=(0, 10))

        ttk.Button(center_frame, text="Начать игру", command=lambda:self.start_game("P", "", self.players.get(),
        self.board_size.get()), width=20, style="Custom.TButton").grid(row=2, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(center_frame, text="Назад", command=lambda:self.return_to_main_menu(), style="Custom.TButton")\
            .grid(row=3, column=0, columnspan=2, pady=(10, 0))

    def create_computer_options(self):
        global main_frame
        main_frame.grid_forget()

        computer_options_frame = ttk.Frame(self.root, padding="20")
        computer_options_frame.grid(row=0, column=0)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        center_frame = ttk.Frame(computer_options_frame)
        center_frame.grid(row=0, column=0, padx=10, pady=10)

        computer_difficulty_label = ttk.Label(center_frame, text="Сложность компьютера:", style="Custom.TLabel")
        computer_difficulty_label.grid(row=0, column=0, pady=(0, 10), sticky="W")
        computer_difficulty_values = ["Рандомный", "Сложный"]
        self.computer_difficulty.set(computer_difficulty_values[0])
        board_size_menu = ttk.OptionMenu(center_frame, self.computer_difficulty, computer_difficulty_values[0],
                                         *computer_difficulty_values, style="Custom.TMenubutton")
        board_size_menu.grid(row=0, column=1, pady=(0, 10))

        computer_difficulty_menu = ttk.OptionMenu(center_frame, self.computer_difficulty, computer_difficulty_values[0],
                                                  *computer_difficulty_values, style="Custom.TMenubutton")
        computer_difficulty_menu.grid(row=0, column=1, pady=(0, 10), sticky="W")

        board_size_label = ttk.Label(center_frame, text="Размер поля:", style="Custom.TLabel")
        board_size_label.grid(row=1, column=0, pady=(0, 10), sticky="W")
        board_size_values = [8, 10, 12, 15, 20]
        self.board_size.set(board_size_values[0])
        board_size_menu = ttk.OptionMenu(center_frame, self.board_size, board_size_values[0],
                                         *board_size_values, style="Custom.TMenubutton")
        board_size_menu.grid(row=1, column=1, pady=(0, 10))

        board_size_menu = ttk.OptionMenu(center_frame, self.board_size, board_size_values[0], *board_size_values,
                                         style="Custom.TMenubutton")
        board_size_menu.grid(row=1, column=1, pady=(0, 10))

        ttk.Button(center_frame, text="Начать игру", command=lambda:
        self.start_game("PC", self.computer_difficulty.get(), 1, self.board_size.get()),
                   width=20, style="Custom.TButton").grid(row=2, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(center_frame, text="Назад", command= lambda:self.return_to_main_menu(), style="Custom.TButton")\
            .grid(row=3, column=0, columnspan=2, pady=(10, 0))

    def create_score_table(self):
        tabel = self.load_scores_from_json("scores.json")
        print(tabel)
        if tabel is None:
            return

        score_list = [(player_name, score) for player_name, score in tabel.items()]

        score_list.sort(key=lambda x: x[1], reverse=True)

        score_window = tk.Toplevel(self.root)
        score_window.title("Таблица рекордов")
        score_window.geometry("1000x1000")

        scores_frame = tk.Frame(score_window)
        scores_frame.pack()

        scores_label = tk.Label(scores_frame, text=f"Имя пользователя{' ' * 12}Счет", font=("Helvetica", 16),
                                anchor='w')
        scores_label.grid(row=0, column=0, sticky='w')

        row = 1
        for player_name, score in score_list:
            score_label = tk.Label(scores_frame, text=f"{player_name}{' ' * 25}{score}", font=("Helvetica", 18),
                                   anchor='w')
            score_label.grid(row=row, column=0, padx=80, sticky='w')
            row += 1

    def load_scores_from_json(self, file_path):
        with open(file_path, "r") as json_file:
            return json.load(json_file)

    def on_exit_button_click(self):
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.root.quit()

    def return_to_main_menu(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.create_main_menu()