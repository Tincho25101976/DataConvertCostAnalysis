import tkinter as tk
from tkinter import font as ft

import ttkbootstrap as tb

class ToolTip:
    def __init__(self, widget, text, _font:ft.Font | tuple | None = None):
        self.widget:tk.Widget = widget
        self.text:str = text
        self.font:ft.Font | tuple | None = (_font if _font is not None else ft.Font(family="Segoe UI", size=8))
        self.tip_window:tk.Toplevel | None = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

        self.__style = tb.Style()
        self.__style.configure("TLabelframe.primary.TLabel", 
                                    font=self.font,
                                    foreground="#ffffff")

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return

        x = self.widget.winfo_pointerx() + 15
        y = self.widget.winfo_pointery() + 10

        #x = x + self.widget.winfo_rootx() + 20
        #y = y + self.widget.winfo_rooty() - 20

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tb.Label(
            tw, 
            text=self.text, 
            justify=tk.LEFT,
            relief=tk.SOLID, 
            borderwidth=1,
            style='TLabelframe.primary.Label'
        )
        label.pack(ipadx=4, ipady=2)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None