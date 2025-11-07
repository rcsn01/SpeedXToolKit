import customtkinter as ctk
import tkinter.filedialog as _tk_filedialog

"""CTk dialog wrappers for messagebox and simpledialog-like behavior.
These provide a drop-in replacement for tkinter.messagebox and tkinter.simpledialog
using CustomTkinter so dialogs match the app theme. Additionally this module
wraps tkinter.filedialog functions so callers can import a `filedialog` object
from here and remain compatible with existing code and tests.
"""


def _get_ctk_parent():
    try:
        # customtkinter keeps the ancestor window in a private helper in some versions
        if hasattr(ctk, "_get_ancestor_window"):
            return ctk._get_ancestor_window()
    except Exception:
        pass
    return None


def _modal_window(title="", width=400, height=160):
    win = ctk.CTkToplevel()
    win.title(title)
    win.geometry(f"{width}x{height}")
    win.resizable(False, False)
    # Try to attach to the CTk parent if available
    try:
        parent = _get_ctk_parent()
        if parent:
            win.transient(parent)
    except Exception:
        pass
    win.grab_set()
    return win


def showinfo(title, message):
    win = _modal_window(title, width=420, height=140)
    frame = ctk.CTkFrame(win)
    frame.pack(fill="both", expand=True, padx=16, pady=12)

    ctk.CTkLabel(frame, text=message, wraplength=380).pack(pady=(0, 12))

    def _ok():
        win.destroy()

    ctk.CTkButton(frame, text="OK", command=_ok).pack()
    win.wait_window()


def showwarning(title, message):
    # Same implementation as showinfo but separate name for callers
    return showinfo(title, message)


def showerror(title, message):
    win = _modal_window(title, width=420, height=140)
    frame = ctk.CTkFrame(win)
    frame.pack(fill="both", expand=True, padx=16, pady=12)

    ctk.CTkLabel(frame, text=message, wraplength=380, text_color="#d9534f").pack(pady=(0, 12))

    def _ok():
        win.destroy()

    ctk.CTkButton(frame, text="OK", command=_ok).pack()
    win.wait_window()


def askstring(title, prompt, initialvalue=None):
    win = _modal_window(title, width=420, height=160)
    frame = ctk.CTkFrame(win)
    frame.pack(fill="both", expand=True, padx=16, pady=12)

    ctk.CTkLabel(frame, text=prompt, wraplength=380).pack(anchor="w")
    entry = ctk.CTkEntry(frame, width=320)
    if initialvalue is not None:
        entry.insert(0, str(initialvalue))
    entry.pack(pady=(8, 8))

    result = {"value": None}

    def _ok():
        result["value"] = entry.get()
        win.destroy()

    def _cancel():
        result["value"] = None
        win.destroy()

    btn_frame = ctk.CTkFrame(frame)
    btn_frame.pack()
    ctk.CTkButton(btn_frame, text="OK", command=_ok).grid(row=0, column=0, padx=6)
    ctk.CTkButton(btn_frame, text="Cancel", command=_cancel).grid(row=0, column=1, padx=6)

    entry.focus_set()
    win.wait_window()
    return result["value"]


def askinteger(title, prompt, initialvalue=None):
    val = askstring(title, prompt, initialvalue=initialvalue)
    if val is None:
        return None
    try:
        return int(val)
    except Exception:
        # mimic tkinter behavior by raising ValueError
        raise ValueError("invalid literal for int() with base 10: '{}'".format(val))


def askyesno(title, question):
    win = _modal_window(title, width=420, height=140)
    frame = ctk.CTkFrame(win)
    frame.pack(fill="both", expand=True, padx=16, pady=12)

    ctk.CTkLabel(frame, text=question, wraplength=380).pack(pady=(0, 12))

    result = {"value": False}

    def _yes():
        result["value"] = True
        win.destroy()

    def _no():
        result["value"] = False
        win.destroy()

    btn_frame = ctk.CTkFrame(frame)
    btn_frame.pack()
    ctk.CTkButton(btn_frame, text="Yes", command=_yes).grid(row=0, column=0, padx=6)
    ctk.CTkButton(btn_frame, text="No", command=_no).grid(row=0, column=1, padx=6)

    win.wait_window()
    return result["value"]


# --- Filedialog compatibility wrappers ---
# Provide a `filedialog` object with common functions. Tests and other modules
# that expect a module-like object (with asksaveasfilename, askopenfilename, etc.)
# can import `filedialog` from here and continue to use it as before.


def askopenfilename(**kwargs):
    parent = _get_ctk_parent()
    return _tk_filedialog.askopenfilename(parent=parent, **kwargs)


def askopenfilenames(**kwargs):
    parent = _get_ctk_parent()
    return _tk_filedialog.askopenfilenames(parent=parent, **kwargs)


def asksaveasfilename(**kwargs):
    parent = _get_ctk_parent()
    return _tk_filedialog.asksaveasfilename(parent=parent, **kwargs)


def askdirectory(**kwargs):
    parent = _get_ctk_parent()
    return _tk_filedialog.askdirectory(parent=parent, **kwargs)


# Expose a module-like object for backward compatibility
class _FileDialogProxy:
    def __getattr__(self, name):
        if name in ("askopenfilename", "askopenfilenames", "asksaveasfilename", "askdirectory"):
            return globals()[name]
        return getattr(_tk_filedialog, name)


filedialog = _FileDialogProxy()


# Provide a module-like `messagebox` proxy so existing modules that import
# `from tkinter import messagebox` can be updated to import this `messagebox`
# without changing call sites (and tests that monkeypatch mod.messagebox will
# continue to work).
class _MessageBoxProxy:
    def showinfo(self, title, message):
        return showinfo(title, message)

    def showwarning(self, title, message):
        return showwarning(title, message)

    def showerror(self, title, message):
        return showerror(title, message)


messagebox = _MessageBoxProxy()
