import tkinter as tk
from tkinter import ttk

class ColorfulCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title('Big Clean Colorful Calculator')
        self.root.resizable(False, False)

        self.style = ttk.Style(root)
        self.style.configure('TButton', font=('Segoe UI', 16, 'bold'), foreground='#202020')
        self.style.configure('TEntry', font=('Segoe UI', 26, 'bold'))

        self.expression = ''

        # Colorful gradient background using canvas
        self.canvas = tk.Canvas(root, width=410, height=560, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.color_index = 0
        self.gradient_colors = ['#ffe4e1', '#ffefd5', '#e6e6fa', '#d8bfd8', '#e0ffff', '#cce7ff', '#d4edda']
        self._draw_background()

        frame = tk.Frame(self.canvas, bg='white', bd=0)
        frame.place(relx=0.5, rely=0.5, anchor='center')

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(frame, textvariable=self.entry_var, justify='right', state='readonly')
        self.entry.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=8, pady=(12, 4))

        for i in range(1, 5):
            frame.rowconfigure(i, weight=1)
            frame.columnconfigure(i-1, weight=1, uniform='low')

        buttons = [
            ('C', 1, 0), ('±', 1, 1), ('%', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2)
        ]

        for (text, r, c) in buttons:
            btn = ttk.Button(frame, text=text, command=lambda t=text: self.on_button_click(t))
            if text == '0':
                btn.grid(row=r, column=c, columnspan=2, sticky='nsew', padx=7, pady=7)
            elif text == '=':
                btn.grid(row=r, column=c, columnspan=2, sticky='nsew', padx=7, pady=7)
            else:
                btn.grid(row=r, column=c, sticky='nsew', padx=7, pady=7)

    def _draw_background(self):
        c = self.gradient_colors[self.color_index % len(self.gradient_colors)]
        self.canvas.delete('bg')
        self.canvas.create_rectangle(0, 0, 410, 560, fill=c, outline=c, tags='bg')
        self.color_index += 1
        self.root.after(1000, self._draw_background)

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ''
        elif char == '=':
            self.calculate()
            return
        elif char == '±':
            self.toggle_sign()
            return
        elif char == '%':
            self.apply_percent()
            return
        else:
            self.expression += char

        self.entry_var.set(self.expression)

    def calculate(self):
        try:
            answer = str(eval(self.expression))
            self.expression = answer
        except Exception:
            answer = 'Error'
            self.expression = ''
        self.entry_var.set(answer)

    def toggle_sign(self):
        if self.expression.startswith('-'):
            self.expression = self.expression[1:]
        else:
            self.expression = '-' + self.expression
        self.entry_var.set(self.expression)

    def apply_percent(self):
        try:
            value = float(self.expression)
            self.expression = str(value / 100)
            self.entry_var.set(self.expression)
        except Exception:
            self.entry_var.set('Error')
            self.expression = ''


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('410x560')
    ColorfulCalculator(root)
    root.mainloop()