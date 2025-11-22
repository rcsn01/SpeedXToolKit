import customtkinter as ctk
from views.ctk_dialogs import filedialog, showinfo, showwarning, showerror, askstring, askinteger, askyesno
import pandas as pd
import csv
from styles import TkinterDialogStyles, ButtonStyles, AppFonts, PanelStyles

def combine_file_view():
    try:
        # Prompt for first file
        file1 = filedialog.askopenfilename(title="Select First CSV File", filetypes=[("CSV files", "*.csv")])
        if not file1:
            showinfo("Cancelled", "No file selected.")
            return None

        # Prompt for second file
        file2 = filedialog.askopenfilename(title="Select Second CSV File", filetypes=[("CSV files", "*.csv")])
        if not file2:
            showinfo("Cancelled", "No second file selected.")
            return None
                
        def _read_csv_with_fallback(path):
            encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'latin-1']
            last_err = None
            # Read small sample for delimiter sniffing
            for enc in encodings:
                try:
                    with open(path, 'r', encoding=enc, newline='') as f:
                        sample = f.read(2048)
                        f.seek(0)
                        # Delimiter detection
                        try:
                            dialect = csv.Sniffer().sniff(sample)
                            delim = dialect.delimiter
                        except csv.Error:
                            delim = ','
                        return pd.read_csv(f, delimiter=delim)
                except UnicodeDecodeError as e:
                    last_err = e
                    continue
                except Exception as e:
                    last_err = e
                    continue
            raise last_err if last_err else RuntimeError('Failed to read CSV with fallback encodings.')

        df1 = _read_csv_with_fallback(file1)
        df2 = _read_csv_with_fallback(file2)

        # If duplicate column names, disambiguate with (1), (2) style
        def _dedupe_cols(cols):
            counts = {}
            result = []
            for c in cols:
                base = (c or '').strip() or 'Unnamed'
                counts[base] = counts.get(base, 0) + 1
                if counts[base] == 1:
                    result.append(base)
                else:
                    result.append(f"{base} ({counts[base]-1})")
            return result
        df1.columns = _dedupe_cols(df1.columns)
        df2.columns = _dedupe_cols(df2.columns)

        common_cols = list(set(df1.columns).intersection(set(df2.columns)))
        if not common_cols:
            showerror("No Common Columns", "The selected files share no column names to merge on.")
            return None

        """Display all columns with checkboxes and allow user to select which ones to keep."""
        root = ctk.CTkToplevel()
        root.title("Combine Files - Select Join Columns")
        root.geometry("520x560")
        # Use centralized panel/dialog colors
        root.configure(fg_color=PanelStyles.PREVIEW.get("fg_color", TkinterDialogStyles.DIALOG_BG))

        # Ensure window is on top and modal
        root.lift()
        root.focus_force()
        root.grab_set()
        try:
            if hasattr(ctk, "_get_ancestor_window"):
                parent = ctk._get_ancestor_window()
                if parent:
                    root.transient(parent)
        except Exception:
            pass

        result = {"confirmed": False, "selected_columns": []}
        checkbox_vars = {}

        def on_confirm():
            selected = [col for col, var in checkbox_vars.items() if var.get()]
            if not selected:
                showwarning("No columns selected", "Please select at least one column to merge on.")
                return
            result["confirmed"] = True
            result["selected_columns"] = selected
            root.destroy()

        def on_cancel():
            root.destroy()

        # File info display
        info_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        info_frame.pack(fill='x', padx=10, pady=(10,4))
        ctk.CTkLabel(
            info_frame,
            text=f"File 1: {file1}",
            anchor='w',
            wraplength=480,
            justify='left',
            text_color=TkinterDialogStyles.LABEL_FG,
            font=AppFonts.SMALL,
        ).pack(fill='x')
        ctk.CTkLabel(
            info_frame,
            text=f"File 2: {file2}",
            anchor='w',
            wraplength=480,
            justify='left',
            text_color=TkinterDialogStyles.LABEL_FG,
            font=AppFonts.SMALL,
        ).pack(fill='x', pady=(2,6))

        # Instruction label
        ctk.CTkLabel(
            root,
            text="Select the columns to merge on (only common columns listed):",
            font=AppFonts.BODY,
            wraplength=480,
            justify='left',
            text_color=TkinterDialogStyles.LABEL_FG,
        ).pack(pady=4, padx=10, anchor='w')

        # Scrollable frame setup
        scrollable_frame = ctk.CTkScrollableFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add checkboxes for each column
        for col in common_cols:
            var = ctk.BooleanVar(master=root)
            cb = ctk.CTkCheckBox(
                scrollable_frame,
                text=col,
                variable=var,
                text_color=TkinterDialogStyles.CHECKBOX_FG,
                anchor='w',
            )
            cb.pack(fill='x', anchor='w', pady=2)
            checkbox_vars[col] = var

        # Confirm/Cancel buttons
        button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        button_frame.pack(pady=20)

        primary = ButtonStyles.PRIMARY
        default = ButtonStyles.DEFAULT

        ctk.CTkButton(
            button_frame,
            text="Confirm",
            command=on_confirm,
            width=primary.get("width"),
            height=primary.get("height"),
            corner_radius=primary.get("corner_radius"),
            fg_color=primary.get("fg_color"),
            hover_color=primary.get("hover_color"),
            text_color=primary.get("text_color"),
            font=primary.get("font"),
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=on_cancel,
            width=default.get("width"),
            height=default.get("height"),
            corner_radius=default.get("corner_radius"),
            fg_color=default.get("fg_color"),
            hover_color=default.get("hover_color"),
            text_color=default.get("text_color"),
            font=default.get("font"),
        ).grid(row=0, column=1, padx=10)

        root.wait_window()

        if result["confirmed"]:
            return pd.merge(df1, df2, on=result["selected_columns"])
        return None
    except Exception as e:
        print("OHHH NOOOOOOOOO")
        print(f"Error: {e}")
        try:
            showerror("Combine Failed", f"Failed to combine files:\n{e}")
        except Exception:
            pass
        return None