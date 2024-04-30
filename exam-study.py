import tkinter as tk
from tkinter import filedialog, simpledialog, Text
from PIL import Image, ImageTk, ImageGrab
import os, secrets
import webbrowser


class MultiLineEntryDialog(simpledialog.Dialog):
    def __init__(self, parent, title, initial_text=""):
        self.data = initial_text
        simpledialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        self.text = Text(master, wrap=tk.WORD, height=10, width=40)
        self.text.pack(expand=tk.YES, fill=tk.BOTH)
        self.text.insert("1.0", self.data)
        return self.text

    def apply(self):
        self.result = self.text.get("1.0", tk.END)


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Study Program")

        path = os.path.join(os.path.dirname(__file__), "star.ico")
        if os.path.isfile(path):
            self.root.iconbitmap(path)

        self.root.minsize(width=800, height=600)

        self.folder_number = tk.Label(root, font=("Helvetica", 10), fg="lightgray")
        self.folder_number.pack()

        self.current_directory = None
        self.quiz_folders = []
        self.current_quiz_indices = []
        self.prev_index = 0

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=0, anchor="center")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(padx=10, pady=10, anchor="center")

        self.question_images = [None]
        self.answer_label = tk.Label(self.frame, image=None)
        self.answer_image = None
        self.is_answer_off = True

        self.answer_button = tk.Button(
            self.button_frame,
            text="Check Answer (J)",
            command=self.show_answer,
            state=tk.DISABLED,
        )
        self.answer_button.pack(
            padx=10,
            pady=7,
            side="left",
            anchor="center",
        )

        self.next_button = tk.Button(
            self.button_frame,
            text="Next Question (K)",
            command=self.show_quiz,
            state=tk.DISABLED,
            highlightbackground="gray",
            highlightcolor="gray",
        )
        self.next_button.pack(padx=10, pady=7, side="left")

        self.add_quiz_button = tk.Button(
            self.button_frame,
            text="Create Question (A)",
            command=self.add_quiz,
            state=tk.DISABLED,
        )
        self.add_quiz_button.pack(padx=10, side="left")

        self.add_choice_button = tk.Button(
            self.button_frame,
            text="Add Image (S)",
            command=self.add_choice,
            state=tk.DISABLED,
        )
        self.add_choice_button.pack(padx=10, pady=7, side="left")

        self.question_number_label = tk.Label(self.frame, font=("Helvetica", 8))
        self.question_number_label.pack(pady=5)

        self.menu_bar = tk.Menu(root)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(
            label="Select Test Bank", command=self.select_quiz_folder
        )

        self.background_color_option_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.background_color_option_menu.add_command(
            label="Light Mode", command=self.turn_into_light_mode
        )
        self.background_color_option_menu.add_command(
            label="Dark Mode", command=self.turn_into_dark_mode
        )

        instructions_menu = tk.Menu(self.menu_bar, tearoff=0)
        instructions_menu.add_command(
            label="How to Use", command=self.show_instructions
        )

        version_menu = tk.Menu(self.menu_bar, tearoff=0)
        version_menu.add_command(label="Program Information", command=self.show_version)

        self.menu_bar.add_cascade(label="Select Test Bank", menu=self.file_menu)
        self.menu_bar.add_cascade(
            label="Background Color Option", menu=self.background_color_option_menu
        )
        self.menu_bar.add_cascade(label="How to Use", menu=instructions_menu)
        self.menu_bar.add_cascade(label="Program Information", menu=version_menu)

        root.config(menu=self.menu_bar)

    def turn_into_light_mode(self, widget=None):
        if widget is None:
            self.answer_button.configure(fg="black")
            self.next_button.configure(fg="black")
            self.add_quiz_button.configure(fg="black")
            self.add_choice_button.configure(fg="black")

            widget = self.root

        if widget == self.menu_bar:
            return

        widget.configure(bg="SystemButtonFace")

        if hasattr(widget, "children"):
            for child in widget.children.values():
                self.turn_into_light_mode(child)
        return

    def turn_into_dark_mode(self, widget=None):
        if widget is None:
            self.answer_button.configure(fg="gray")
            self.next_button.configure(fg="gray")
            self.add_quiz_button.configure(fg="gray")
            self.add_choice_button.configure(fg="gray")

            widget = self.root

        if widget == self.menu_bar:
            return

        widget.configure(bg="black")

        if hasattr(widget, "children"):
            for child in widget.children.values():
                self.turn_into_dark_mode(child)
        return

    def open_link(self, event):
        webbrowser.open("https://github.com/yeohj0710/exam-study-program")
        self.instructions_window.destroy()

    def show_instructions(self):
        self.instructions_window = tk.Toplevel(self.root)
        self.instructions_window.title("How to Use")

        INSTRUCTIONS_WINDOW_MIN_WIDTH = 400
        INSTRUCTIONS_WINDOW_MIN_HEIGHT = 120

        self.instructions_window.minsize(
            width=INSTRUCTIONS_WINDOW_MIN_WIDTH, height=INSTRUCTIONS_WINDOW_MIN_HEIGHT
        )

        path = os.path.join(os.path.dirname(__file__), "star.ico")

        if os.path.isfile(path):
            self.instructions_window.iconbitmap(path)

        parent_x = self.root.winfo_rootx() + self.root.winfo_width() // 2
        parent_y = self.root.winfo_rooty() + self.root.winfo_height() // 2

        self.instructions_window.geometry(
            f"+{parent_x - INSTRUCTIONS_WINDOW_MIN_WIDTH // 2}+{parent_y - INSTRUCTIONS_WINDOW_MIN_HEIGHT}"
        )

        tk.Label(self.instructions_window, text="").pack()

        link_label = tk.Label(
            self.instructions_window,
            text="프로그램의 자세한 사용 방법은 아래의 링크에서 확인할 수 있습니다.",
        )
        link_label.pack()

        tk.Label(self.instructions_window, text="").pack()

        link_label = tk.Label(
            self.instructions_window,
            text="프로그램 사용 설명글 링크",
            fg="blue",
            cursor="hand2",
        )
        link_label.pack()

        link_label.bind("<Button-1>", self.open_link)

    def show_version(self):
        self.version_window = tk.Toplevel(self.root)
        self.version_window.title("Program Information")

        VERSION_WINDOW_MIN_WIDTH = 300
        VERSION_WINDOW_MIN_HEIGHT = 100

        self.version_window.minsize(
            width=VERSION_WINDOW_MIN_WIDTH, height=VERSION_WINDOW_MIN_HEIGHT
        )

        path = os.path.join(os.path.dirname(__file__), "star.ico")
        if os.path.isfile(path):
            self.version_window.iconbitmap(path)

        parent_x = self.root.winfo_rootx() + self.root.winfo_width() // 2
        parent_y = self.root.winfo_rooty() + self.root.winfo_height() // 2

        self.version_window.geometry(
            f"+{parent_x - VERSION_WINDOW_MIN_WIDTH // 2}+{parent_y - VERSION_WINDOW_MIN_HEIGHT}"
        )

        label = tk.Label(self.version_window, text="Developer: 2020194025 yeohj0710")
        label.pack(padx=20, pady=10)

        label = tk.Label(self.version_window, text="Version: 240430")
        label.pack(padx=20, pady=10)

    def select_quiz_folder(self):
        temp_directory = self.current_directory
        self.current_directory = filedialog.askdirectory()

        if self.current_directory:
            self.root.bind("j", lambda event: self.show_answer())
            self.root.bind("k", lambda event: self.show_quiz())
            self.root.bind("a", lambda event: self.add_quiz())
            self.root.bind("s", lambda event: self.add_choice())

            self.load_quiz_folders
            self.show_quiz()
        elif temp_directory:
            self.current_directory = temp_directory
        else:
            self.answer_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.add_quiz_button.config(state=tk.DISABLED)
            self.add_choice_button.config(state=tk.DISABLED)

            self.root.unbind("j")
            self.root.unbind("k")
            self.root.unbind("a")
            self.root.unbind("s")

    def load_quiz_folders(self):
        self.quiz_folders = [
            folder
            for folder in os.listdir(self.current_directory)
            if os.path.isdir(os.path.join(self.current_directory, folder))
        ]
        self.current_quiz_indices = list(range(len(self.quiz_folders)))
        secrets.SystemRandom().shuffle(self.current_quiz_indices)

    def resize_image(self, image, max_width, max_height):
        resized_image = image.copy()

        width, height = resized_image.size
        if width > max_width or height > max_height:
            resized_image.thumbnail((max_width, max_height))

        return resized_image

    def show_quiz(self, again=False):
        if len(self.current_quiz_indices) == 0:
            self.load_quiz_folders()

        if len(self.current_quiz_indices) == 0:
            self.add_quiz_button.config(state=tk.NORMAL)
            self.add_choice_button.config(state=tk.NORMAL)

            return

        if self.question_images[0] is not None:
            for label in self.question_images:
                label.pack_forget()

        self.answer_label.pack_forget()

        index = self.prev_index

        if not again:
            index = self.current_quiz_indices.pop(0)
            self.prev_index = index
            self.is_answer_off = True

        folder_name = self.quiz_folders[index]
        folder_path = os.path.join(self.current_directory, folder_name)

        self.folder_number.config(text="Folder ID : " + folder_name)

        images = [
            image
            for image in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, image))
        ]

        last_number = 1
        while True:
            name = str(last_number + 1) + ".png"
            if name not in images:
                break
            last_number += 1

        shuffled_numbers = [i for i in range(1, last_number + 1)]
        part_numbers = shuffled_numbers[1:-1]
        secrets.SystemRandom().shuffle(part_numbers)
        shuffled_numbers[1:-1] = part_numbers

        self.question_images = [None] * len(images)

        for i in range(last_number):
            image_path = os.path.join(folder_path, str(shuffled_numbers[i]) + ".png")
            image = Image.open(image_path)
            if i == 0:
                image = self.resize_image(image, 1440, 400)
            else:
                image = self.resize_image(image, 1440, 600)
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(self.frame, image=photo)
            label.image = photo

            self.question_images[i] = label

            if i == len(images) - 1:
                self.answer_image = photo

        for label in self.question_images[:-1]:
            label.pack(pady=10)

        self.answer_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)
        self.add_quiz_button.config(state=tk.NORMAL)
        self.add_choice_button.config(state=tk.NORMAL)

        self.answer_button.config(text="Check Answer (J)")

    def show_answer(self):
        if self.is_answer_off:
            for label in self.question_images[1:]:
                label.pack_forget()
            self.answer_label.config(image=self.answer_image)
            self.answer_label.pack(pady=5)
            self.answer_button.config(text="Hide Answer (J)")
            self.next_button.config(state=tk.NORMAL)
        else:
            self.show_quiz(again=True)
            self.answer_button.config(text="Check Answer (J)")

        self.is_answer_off = not self.is_answer_off

    def add_quiz(self):
        name = self.find_next_folder_name()
        folder_path = os.path.join(self.current_directory, name)
        os.makedirs(folder_path, exist_ok=True)

        self.file_path = folder_path

        if self.next_button["state"] == tk.DISABLED:
            self.next_button.config(state=tk.NORMAL)

    def find_next_folder_name(self):
        self.load_quiz_folders()
        i = 1
        while True:
            name = str(i)
            if name not in self.quiz_folders:
                return name
            i += 1

    def add_choice(self):
        self.choice_images = [
            image
            for image in os.listdir(self.file_path)
            if os.path.isfile(os.path.join(self.file_path, image))
        ]

        i = 1
        while True:
            name = str(i) + ".png"
            if name not in self.choice_images:
                break
            i += 1

        img = ImageGrab.grabclipboard()
        if img:
            img = self.resize_image(img, img.size[0], img.size[1])
            img.save(os.path.join(self.file_path, str(i) + ".png"))


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
