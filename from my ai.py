import tkinter as tk

def add():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        result = num1 + num2
        label_result.config(text=f"Result: {result}")
    except ValueError:
        label_result.config(text="Error: Please enter valid numbers")

def subtract():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        result = num1 - num2
        label_result.config(text=f"Result: {result}")
    except ValueError:
        label_result.config(text="Error: Please enter valid numbers")

def multiply():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        result = num1 * num2
        label_result.config(text=f"Result: {result}")
    except ValueError:
        label_result.config(text="Error: Please enter valid numbers")

def divide():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        if num2 == 0:
            label_result.config(text="Error: Division by zero")
        else:
            result = num1 / num2
            label_result.config(text=f"Result: {result}")
    except ValueError:
        label_result.config(text="Error: Please enter valid numbers")

def clear():
    entry_num1.delete(0, tk.END)
    entry_num2.delete(0, tk.END)
    label_result.config(text="Result: ")

# Create the main window
window = tk.Tk()
window.title("Calculator")
window.geometry("400x300")  # Set window size

# Create input fields and labels
label_num1 = tk.Label(window, text="Enter first number:")
label_num1.pack()
entry_num1 = tk.Entry(window)
entry_num1.pack()

label_num2 = tk.Label(window, text="Enter second number:")
label_num2.pack()
entry_num2 = tk.Entry(window)
entry_num2.pack()

# Create buttons for operations
button_add = tk.Button(window, text="+", command=add)
button_subtract = tk.Button(window, text="-", command=subtract)
button_multiply = tk.Button(window, text="*", command=multiply)
button_divide = tk.Button(window, text="/", command=divide)
button_clear = tk.Button(window, text="Clear", command=clear)

# Arrange buttons using grid layout
button_add.pack()
button_subtract.pack()
button_multiply.pack()
button_divide.pack()
button_clear.pack()

# Create result label
label_result = tk.Label(window, text="Result: ")
label_result.pack()

# Run the application
window.mainloop()