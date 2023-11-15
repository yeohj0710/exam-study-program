import tkinter as tk
from tkinter import filedialog, simpledialog, Text
from PIL import Image, ImageTk, ImageGrab
import os, secrets


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
        self.result = self.text.get("1.0", tk.END)  # 결과 변수를 설정하여 텍스트를 저장


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("족보 암기 프로그램 last updated on 231026 by 여형준")
        self.root.minsize(width=800, height=600)

        self.folder_number = tk.Label(root, font=("Helvetica", 10), fg="lightgray")
        self.folder_number.pack()

        self.current_directory = None
        self.quiz_folders = []
        self.current_quiz_indices = []

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=0, anchor="center")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(padx=10, pady=10, anchor="center")

        self.question_images = [None]
        self.answer_label = tk.Label(self.frame, image=None)
        self.answer_image = None

        self.answer_button = tk.Button(
            self.button_frame,
            text="정답 확인 (J)",
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
            text="다음 문제 (K)",
            command=self.show_quiz,
            state=tk.DISABLED,
            highlightbackground="gray",
            highlightcolor="gray",
        )
        self.next_button.pack(padx=10, pady=7, side="left")

        self.add_quiz_button = tk.Button(
            self.button_frame,
            text="문제 생성 (A)",
            command=self.add_quiz,
            state=tk.DISABLED,
        )
        self.add_quiz_button.pack(padx=10, side="left")

        self.add_choice_button = tk.Button(
            self.button_frame,
            text="이미지 추가 (win + shift + s로 문제 캡쳐한 상태로) (S)",
            command=self.add_choice,
            state=tk.DISABLED,
        )
        self.add_choice_button.pack(padx=10, pady=7, side="left")

        self.question_number_label = tk.Label(self.frame, font=("Helvetica", 8))
        self.question_number_label.pack(pady=5)

        self.root.bind("j", lambda event: self.show_answer())
        self.root.bind("k", lambda event: self.show_quiz())
        self.root.bind("a", lambda event: self.add_quiz())
        self.root.bind("s", lambda event: self.add_choice())

        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="족보 폴더 선택", command=self.select_quiz_folder)
        menu_bar.add_cascade(label="족보 폴더 선택", menu=file_menu)
        root.config(menu=menu_bar)

    def select_quiz_folder(self):
        self.current_directory = filedialog.askdirectory()
        self.load_quiz_folders
        self.show_quiz()

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

    def show_quiz(self):
        if len(self.current_quiz_indices) == 0:
            self.load_quiz_folders()

        if self.question_images[0] is not None:
            for label in self.question_images:
                label.pack_forget()

        self.answer_label.pack_forget()

        index = self.current_quiz_indices.pop(0)
        folder_name = self.quiz_folders[index]
        folder_path = os.path.join(self.current_directory, folder_name)

        self.folder_number.config(text="폴더 번호 : " + folder_name + "번")

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
                image = self.resize_image(image, 720, 180)
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

    def show_answer(self):
        for label in self.question_images[1:]:
            label.pack_forget()
        self.answer_label.config(image=self.answer_image)
        self.answer_label.pack(pady=5)
        self.answer_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def add_quiz(self):
        name = self.find_next_folder_name()
        folder_path = os.path.join(self.current_directory, name)
        os.makedirs(folder_path, exist_ok=True)

        self.file_path = folder_path

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
