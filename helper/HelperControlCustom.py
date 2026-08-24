import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap import ScrolledFrame

class ScrolledCheckboxList(tb.Frame):
    def __init__(
            self,
            parent: tk.Misc,
            _text:str | None = None,
            items: list[str] | None = None,
            bootstyle: str = "primary-round-toggle"):
        super().__init__(parent)

        self.bootstyle = bootstyle
        self.vars: dict[str, tk.BooleanVar] = {}

        self.scroll_frame = ScrolledFrame(self, autohide=True)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)

        if items and len(items) > 0:
            self.SetItems(items)

    def SetItems(self, items:list[str], _state:bool=True)->None:
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.vars.clear()

        for item in items:
            var = tk.BooleanVar(value=_state)
            self.vars[item] = var

            chk = tb.Checkbutton(
                self.scroll_frame,
                text=item,
                variable=var,
                bootstyle=self.bootstyle,
            )
            chk.pack(anchor=tk.W, pady=(0, 1), padx=(1, 0))

    def GetCheckedItems(self)->list[str]:
        return [item for item, var in self.vars.items() if var.get()]

    def SelectAll(self, state:bool=True)->None:
        for var in self.vars.values():
            var.set(state)