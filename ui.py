from tkinter import *
from tkinter import messagebox, filedialog, ttk
import pandas as pd
from github_api import search_github_repos

class GitHubRepoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Repo Finder")
        self.root.geometry("900x600")

        Label(root, text="Enter GitHub Search Query:", font=("Arial", 12)).pack(pady=10)
        self.query_entry = Entry(root, font=("Arial", 12), width=80)
        self.query_entry.pack(pady=5)

        Button(root, text="Search", command=self.search, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)
        Button(root, text="Export to CSV", command=self.export_csv, font=("Arial", 10)).pack(pady=5)

        self.tree = ttk.Treeview(root, columns=("Name", "Stars", "Language", "URL"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        self.tree.pack(fill=BOTH, expand=True)

        self.df = pd.DataFrame()

    def search(self):
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a search query.")
            return
        self.df = search_github_repos(query)
        self.populate_treeview()

    def populate_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=(row["Name"], row["Stars"], row["Language"], row["URL"]))

    def export_csv(self):
        if self.df.empty:
            messagebox.showwarning("Export Error", "No data to export.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.df.to_csv(file_path, index=False)
            messagebox.showinfo("Export Complete", f"Data saved to:\n{file_path}")
