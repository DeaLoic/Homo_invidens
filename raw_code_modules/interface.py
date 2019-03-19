# interface and visualisation
import tkinter as tk

# создать окно
root_window = tk.Tk()

# выполнить конфигурацию окна
root_window.title("... Modeling")
root_window.geometry("400x250")
root_window.resizable(0,0)

# ввод начальных значений
frame_inputs = tk.LabelFrame(root_window)

entry_v0 = tk.Entry(frame_inputs)
entry_H = tk.Entry(frame_inputs)
entry_m = tk.Entry(frame_inputs)

canvas_v0 = tk.Canvas(frame_inputs)
canvas_H = tk.Canvas(frame_inputs)
canvas_m = tk.Canvas(frame_inputs)

canvas_v0.create_text(45, 10, text = "Начальная скорость - абсолютное значение:")
canvas_H.create_text(45, 10, text = "Высота сброса - в метрах:")
canvas_m.create_text(45, 10, text = "Масса груза - в килограммах:")

# ввод таблиц - указание пути к файлам с таблицами
frame_tables = tk.LabelFrame(root_window)

entry_path_1 = tk.Entry(frame_tables)
entry_path_2 = tk.Entry(frame_tables)

button_path_1 = tk.Button(frame_tables)
button_path_2 = tk.Button(frame_tables)

# Кнопка запуска
frame_output = tk.LabelFrame(root_window)
output_button = tk.Button(frame_output)

# расположить виджеты в окне
frame_inputs.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.35)
frame_tables.place(relx = 0, rely = 0.35, relwidth = 1, relheight = 0.35)
frame_output.place(relx = 0, rely = 0.7, relwidth = 1, relheight = 0.3)

root_window.mainloop()
