import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'main.csv')

        self.main_csv = pd.read_csv(filename)

    def create_widgets(self):
        self.select_button = tk.Button(self)
        self.select_button["text"] = "Select CSV file"
        self.select_button["command"] = self.select_file
        self.select_button.pack(side="top")

        self.file_label = tk.Label(self)
        self.file_label.pack()

        self.merge_button = tk.Button(self)
        self.merge_button["text"] = "Merge CSV files"
        self.merge_button["command"] = self.merge_csv
        self.merge_button.pack(side="top")

        self.format_var = tk.StringVar()
        self.format_var.set("csv")
        self.csv_radio = tk.Radiobutton(self, text="CSV", variable=self.format_var, value="csv")
        self.csv_radio.pack(side="left")
        self.xlsx_radio = tk.Radiobutton(self, text="XLSX", variable=self.format_var, value="xlsx")
        self.xlsx_radio.pack(side="left")
        
        self.save_button = tk.Button(self)
        self.save_button["text"] = "Save merged file"
        self.save_button["command"] = self.save_file
        self.save_button.pack(side="top")

    def select_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.filepath = filepath
        self.file_label["text"] = filepath

    def merge_csv(self):
        user_dataframe = pd.read_csv(self.filepath)
        merged_dataframe = pd.concat([self.main_csv[self.main_csv.columns], user_dataframe], ignore_index=True, sort=False)
        self.merged_dataframe = merged_dataframe

    def save_file(self):
        filepath = filedialog.asksaveasfilename(filetypes=[("CSV files", "*.csv"), ("XLSX files", "*.xlsx")], defaultextension=self.format_var.get())
        if self.format_var.get() == "csv":
            self.merged_dataframe.to_csv(filepath, index=False)
        elif self.format_var.get() == "xlsx":
            self.merged_dataframe.to_excel(filepath, index=False)
            
root = tk.Tk()
app = App(master=root)


app.mainloop()

