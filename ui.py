import os
import json
import pandas as pd
import ttkbootstrap as tb
import subprocess
import webbrowser
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox
from ttkbootstrap.constants import W
from ttkbootstrap.dialogs import Querybox
from github_api import search_github_repos
from config import load_token_from_env

# Auto-resolve safe history path
def get_history_path():
    try:
        base = os.getenv("APPDATA") or os.getenv("LOCALAPPDATA")
        if not base:
            base = os.path.expanduser("~\\AppData\\Roaming")
        path = os.path.join(base, "GitHubRepoFinder")
        os.makedirs(path, exist_ok=True)
        return os.path.join(path, "history.json")
    except Exception as e:
        print(f"[Fallback] Could not use APPDATA: {e}")
        return os.path.abspath("history.json")

HISTORY_FILE = get_history_path()

def launch_app():
    app = RepoFinderApp()
    app.root.mainloop()

class RepoFinderApp:
    def __init__(self):
        self.root = tb.Window(themename="flatly")
        self.root.title("GitHub Repo Finder")
        self.root.geometry("1100x750")
        self.token = load_token_from_env() or self.ask_token()
        self.df = pd.DataFrame()
        self.build_ui()

    def ask_token(self):
        return Querybox.get_string("Paste your GitHub personal access token:")

    def build_ui(self):
        tb.Button(self.root, text="🌙 Toggle Theme", command=self.toggle_theme, bootstyle="outline-dark").pack(pady=5, anchor="ne", padx=10)
        tb.Label(self.root, text="GitHub Repo Finder", font=("Segoe UI", 20, "bold")).pack(pady=10)

        form = tb.Frame(self.root, padding=10)
        form.pack()

        self.query_entry = tb.Entry(form, width=40)
        tb.Label(form, text="Query").grid(row=0, column=0, padx=5, sticky=W)
        self.query_entry.grid(row=0, column=1, padx=5)

        self.language_entry = tb.Entry(form, width=15)
        tb.Label(form, text="Language").grid(row=0, column=2, padx=5)
        self.language_entry.grid(row=0, column=3, padx=5)

        self.stars_entry = tb.Entry(form, width=10)
        tb.Label(form, text="Min Stars").grid(row=0, column=4, padx=5)
        self.stars_entry.insert(0, "20")
        self.stars_entry.grid(row=0, column=5, padx=5)

        self.license_entry = tb.Entry(form, width=15)
        tb.Label(form, text="License").grid(row=0, column=6, padx=5)
        self.license_entry.grid(row=0, column=7, padx=5)

        tb.Button(form, text="🔍 Search", command=self.search_repos, bootstyle="success").grid(row=0, column=8, padx=5)
        tb.Button(form, text="📄 Export CSV", command=self.export_csv, bootstyle="info").grid(row=0, column=9, padx=5)

        self.history_dropdown = tb.Menubutton(form, text="🕘 History", bootstyle="outline")
        self.history_menu = tb.Menu(self.history_dropdown)
        self.history_dropdown["menu"] = self.history_menu
        self.history_dropdown.grid(row=0, column=10, padx=5)

        self.update_history_dropdown()

        columns = ("Name", "Stars", "Language", "License", "URL")
        self.tree = tb.Treeview(self.root, columns=columns, show="headings", height=15, bootstyle="secondary")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=220 if col == "URL" else 130)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        action_frame = tb.Frame(self.root)
        action_frame.pack()

        tb.Button(action_frame, text="🌐 Open Repo", command=self.open_repo).pack(side="left", padx=10)
        tb.Button(action_frame, text="⭐ Star Repo", command=self.star_repo).pack(side="left", padx=10)
        tb.Button(action_frame, text="📥 Clone Repo", command=self.clone_repo).pack(side="left", padx=10)
        tb.Button(action_frame, text="📊 Show Charts", command=self.show_charts).pack(side="left", padx=10)

    def toggle_theme(self):
        current = self.root.style.theme.name
        next_theme = "darkly" if current != "darkly" else "flatly"
        self.root.style.theme_use(next_theme)

    def search_repos(self):
        query = self.query_entry.get()
        language = self.language_entry.get()
        stars = self.stars_entry.get()
        license_type = self.license_entry.get()

        if not query:
            messagebox.showwarning("Query Missing", "Enter a GitHub search query.")
            return

        try:
            self.df = search_github_repos(self.token, query, language, stars, license_type)
            self.save_query_to_history(query)
            self.update_history_dropdown()
            self.populate_table()
        except Exception as e:
            import traceback
            messagebox.showerror("API Error", f"{str(e)}\n\n{traceback.format_exc()}")

    def populate_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=(row["Name"], row["Stars"], row["Language"], row.get("License", ""), row["URL"]))

    def export_csv(self):
        if self.df.empty:
            messagebox.showwarning("Nothing to Export", "No data available to export.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if file:
            self.df.to_csv(file, index=False)
            messagebox.showinfo("Exported", f"Data saved to:\n{file}")

    def open_repo(self):
        selected = self.tree.selection()
        if selected:
            url = self.tree.item(selected[0])["values"][4]
            webbrowser.open(url)

    def clone_repo(self):
        selected = self.tree.selection()
        if selected:
            url = self.tree.item(selected[0])["values"][4]
            subprocess.Popen(["start", "cmd", "/k", f"git clone {url}"], shell=True)

    def star_repo(self):
        import requests
        selected = self.tree.selection()
        if selected:
            repo = self.tree.item(selected[0])["values"][0]
            response = requests.put(f"https://api.github.com/user/starred/{repo}",
                                    headers={"Authorization": f"token {self.token}",
                                             "Accept": "application/vnd.github.v3+json"})
            if response.status_code == 204:
                messagebox.showinfo("Success", f"You starred {repo} 🎉")
            else:
                messagebox.showerror("Error", f"Failed to star: {response.status_code}")

    def show_charts(self):
        if self.df.empty:
            messagebox.showwarning("No Data", "Run a search first.")
            return
        self.df["Language"].value_counts().plot(kind="bar", title="Languages")
        plt.ylabel("Repo Count")
        plt.show()

    def save_query_to_history(self, query):
        try:
            history = self.load_history()
            if query not in history:
                history.append(query)
                with open(HISTORY_FILE, "w") as f:
                    json.dump(history[-10:], f)
        except Exception as e:
            messagebox.showerror("Write Error", f"Could not save search history:\n{e}")

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def update_history_dropdown(self):
        self.history_menu.delete(0, "end")
        for q in reversed(self.load_history()):
            self.history_menu.add_command(label=q, command=lambda q=q: self.query_entry.insert(0, q))
