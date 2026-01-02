from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import simpledialog # Добавляем для диалоговых окон

root = Tk()
root.geometry("2565x1445")
root.title("Drawing App")

userX, userY = 0, 0
canvas_bg_color = "white"
color = "black"
brush_size = 3
current_tool = "pen" # Новая переменная для отслеживания выбранного инструмента

# --- Функции инструментов ---

def store_pasit(event):
    global userX, userY
    userX = event.x
    userY = event.y

def on_canvas_click(event):
    if current_tool == "text":
        add_text_at_click(event)
    else:
        # Стандартное поведение для пера/ластика (начало линии)
        store_pasit(event)

def on_canvas_drag(event):
    if current_tool == "pen" or current_tool == "eraser":
        c.create_line(userX, userY, event.x, event.y, fill=color, width=brush_size, smooth=True, capstyle=ROUND)
        store_pasit(event)

def change_color():
    global color
    new_color_info = colorchooser.askcolor() 
    if new_color_info[1]: # Проверяем, что цвет выбран
        color = new_color_info[1]
        color_button.config(bg=color)

def update_brush_size(value):
    global brush_size
    brush_size = int(value)

# --- Функции кнопок ---

def set_tool_pen():
    global current_tool, color
    current_tool = "pen"
    color = "black" # Сброс цвета для пера
    color_button.config(bg="black")

def set_tool_eraser():
    global current_tool, color
    current_tool = "eraser"
    color = canvas_bg_color # Цвет фона для ластика
    color_button.config(bg=canvas_bg_color)
    
def set_tool_text():
    global current_tool
    current_tool = "text"
    print(f"Инструмент изменен на {current_tool}. Кликните на холсте, чтобы добавить текст.")


def clear_canvas():
    c.delete("all")

def save_canvas():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".ps",
        filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")]
    )
    if file_path:
        try:
            c.postscript(file=file_path, colormode='color')
            print(f"Изображение успешно сохранено в {file_path}")
        except Exception as e:
            print(f"Ошибка сохранения файла: {e}")

# --- НОВАЯ ФУНКЦИЯ: Добавление текста по координатам клика ---
def add_text_at_click(event):
    text_to_add = text_entry.get() # Получаем текст из поля ввода
    if text_to_add:
        # Используем метод create_text для добавления текста на холст
        c.create_text(
            event.x, event.y, 
            text=text_to_add, 
            fill=color, 
            font=("Helvetica", brush_size * 2), # Используем размер кисти для масштабирования шрифта
            anchor="nw" # Привязка к верхнему левому углу клика
        )
    else:
        print("Поле ввода текста пустое.")

# --- Создание интерфейса ---

control_frame = Frame(root, bd=2, relief=RAISED)
control_frame.pack(side=TOP, fill=X)

c = Canvas(root, width=2565, height=1445, bg=canvas_bg_color)
c.pack(fill=BOTH, expand=True)

# Кнопки инструментов
color_button = Button(control_frame, text="Color", command=change_color, bg="black", fg="white")
color_button.pack(side=LEFT, padx=10, pady=5)

pen_button = Button(control_frame, text="Pen", command=set_tool_pen)
pen_button.pack(side=LEFT, padx=5, pady=5)

eraser_button = Button(control_frame, text="Eraser", command=set_tool_eraser)
eraser_button.pack(side=LEFT, padx=5, pady=5)

size_label = Label(control_frame, text="Size:")
size_label.pack(side=LEFT, padx=5, pady=5)

size_slider = Scale(control_frame, from_=1, to=50, orient=HORIZONTAL, command=update_brush_size)
size_slider.set(brush_size)
size_slider.pack(side=LEFT, padx=5, pady=5)

# !!! НОВАЯ КНОПКА ИНСТРУМЕНТА ТЕКСТА !!!
text_tool_button = Button(control_frame, text="Text Tool", command=set_tool_text)
text_tool_button.pack(side=LEFT, padx=10, pady=5)

text_entry = Entry(control_frame, width=30, bd=2)
text_entry.pack(side=LEFT, padx=10, pady=5)
text_entry.insert(0, "Введите текст здесь")

clear_button = Button(control_frame, text="Clear Canvas", command=clear_canvas)
clear_button.pack(side=LEFT, padx=10, pady=5)

save_button = Button(control_frame, text="Save (as .ps)", command=save_canvas)
save_button.pack(side=LEFT, padx=10, pady=5)


# Привязка событий мыши к холсту изменена на одну общую функцию-обработчик
c.bind("<Button-1>", on_canvas_click)
c.bind("<B1-Motion>", on_canvas_drag)
c.bind("<ButtonRelease-1>", on_canvas_drag) # Также полезно для завершения рисования

root.mainloop()
