import pandas as pd
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Querybox
from ttkbootstrap.constants import *
from github_api import search_github_repos
from config import load_token_from_env
from tkinter import messagebox, filedialog

def launch_app():
    app = RepoFinderApp()
    app.root.mainloop()

class RepoFinderApp:
    def __init__(self):
        self.root = tb.Window(themename="flatly")  # can toggle themes
        self.root.title("GitHub Repo Finder")
        self.root.geometry("1050x700")

        self.token = load_token_from_env() or self.ask_token()
        self.df = pd.DataFrame()

        # UI components
        self.build_ui()

    def ask_token(self):
        return Querybox.get_string("Enter GitHub Token", prompt="Paste your GitHub personal access token:")

    def build_ui(self):
        # Theme toggle
        self.theme_toggle = tb.Button(self.root, text="🌙 Toggle Theme", command=self.toggle_theme, bootstyle="outline-dark")
        self.theme_toggle.pack(pady=5, anchor="ne", padx=10)

        # Header
        tb.Label(self.root, text="GitHub Repo Finder", font=("Segoe UI", 20, "bold")).pack(pady=10)

        # Search + filters
        search_frame = tb.Frame(self.root, padding=10)
        search_frame.pack(pady=5)

        tb.Label(search_frame, text="Query").grid(row=0, column=0, padx=5, sticky=W)
        self.query_entry = tb.Entry(search_frame, width=40)
        self.query_entry.grid(row=0, column=1, padx=5)

        tb.Label(search_frame, text="Language").grid(row=0, column=2, padx=5)
        self.language_entry = tb.Entry(search_frame, width=15)
        self.language_entry.grid(row=0, column=3, padx=5)

        tb.Label(search_frame, text="Min Stars").grid(row=0, column=4, padx=5)
        self.stars_entry = tb.Entry(search_frame, width=10)
        self.stars_entry.insert(0, "20")
        self.stars_entry.grid(row=0, column=5, padx=5)

        tb.Button(search_frame, text="🔍 Search", command=self.search_repos, bootstyle="success").grid(row=0, column=6, padx=10)
        tb.Button(search_frame, text="📄 Export CSV", command=self.export_csv, bootstyle="info").grid(row=0, column=7, padx=5)

        # Treeview (Table)
        columns = ("Name", "Stars", "Language", "URL")
        self.tree = tb.Treeview(self.root, columns=columns, show="headings", bootstyle="secondary")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=250 if col == "URL" else 120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def toggle_theme(self):
        current = self.root.getvar("ttk::theme")
        next_theme = "darkly" if current == "flatly" else "flatly"
        self.root.style.theme_use(next_theme)

    def search_repos(self):
        query = self.query_entry.get()
        language = self.language_entry.get()
        stars = self.stars_entry.get()

        if not query:
            messagebox.showwarning("Query Missing", "Enter a GitHub search query.")
            return

        try:
            self.df = search_github_repos(self.token, query, language, stars)
            self.populate_table()
        except Exception as e:
            messagebox.showerror("API Error", str(e))

    def populate_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=(row["Name"], row["Stars"], row["Language"], row["URL"]))

    def export_csv(self):
        if self.df.empty:
            messagebox.showwarning("Nothing to Export", "No data available to export.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if file:
            self.df.to_csv(file, index=False)
            messagebox.showinfo("Exported", f"Data saved to:\n{file}")
