import os
import tkinter as tk
from tkinter import ttk, filedialog

text_contents = dict()


def check_for_changes():
    current = get_text_widget()
    content = current.get("1.0", "end-1c")
    name = notebook.tab("current")["text"]

    if hash(content) != text_contents[str(current)]:
        if name[-1] != "*":
            notebook.tab("current", text=name + "*")
    elif name[-1] == "*":
        notebook.tab("current", text=name[:-1])


def get_text_widget():
    text_widget = notebook.nametowidget(notebook.select())

    return text_widget


def create_file(content="", title="Untitled"):
    text_area = tk.Text(notebook)
    text_area.insert("end", content)
    text_area.pack(fill="both", expand=True)

    notebook.add(text_area, text=title)
    notebook.select(text_area)

    text_contents[str(text_area)] = hash(content)


def open_file():
    file_path = filedialog.askopenfilename()

    try:
        filename = os.path.basename(file_path)

        with open(file_path, "r") as file:
            content = file.read()

    except (AttributeError, FileNotFoundError):
        print("Open operation cancelled")
        return

    create_file(content, filename)


def save_file():
    file_path = filedialog.asksaveasfilename()

    try:
        filename = os.path.basename(file_path)
        text_widget = get_text_widget()
        content = text_widget.get("1.0", "end-1c")

        with open(file_path, "w") as file:
            file.write(content)

    except (AttributeError, FileNotFoundError):
        print("Save operation cancelled")
        return

    notebook.tab("current", text=filename)
    text_contents[str(text_widget)] = hash(content)


root = tk.Tk()
root.title("Teclado Text Editor")
root.option_add("*tearOff", False)

main = ttk.Frame(root)
main.pack(fill="both", expand=True, padx=(1), pady=(4, 0))

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar)

menubar.add_cascade(menu=file_menu, label="File")

file_menu.add_command(label="New", command=create_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open...", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")

notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)

create_file()

root.bind("<KeyPress>", lambda event: check_for_changes())
root.bind("<Control-n>", lambda event: create_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())

root.mainloop()
