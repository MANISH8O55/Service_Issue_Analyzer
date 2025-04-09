import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

class ITServiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IT Service Issue Analyzer")
        self.root.geometry("900x600")

        # Search Frame
        self.search_frame = ttk.Frame(root)
        self.search_frame.pack(pady=10)

        ttk.Label(self.search_frame, text="Search Issue:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(self.search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", self.search_issues)

        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search_issues)
        self.search_button.pack(side=tk.LEFT, padx=5)

        # Results Treeview
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        columns = ("IssueName", "Functionality", "Area", "LOB")
        self.results_tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        self.results_tree.heading("IssueName", text="Issue Name")
        self.results_tree.heading("Functionality", text="Functionality")
        self.results_tree.heading("Area", text="Area")
        self.results_tree.heading("LOB", text="Line of Business")
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.results_tree.bind("<<TreeviewSelect>>", self.display_details)

        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_tree.configure(yscrollcommand=self.scrollbar.set)

        # Details Frame
        self.details_frame = ttk.LabelFrame(root, text="Issue Details")
        self.details_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.details_text = tk.Text(self.details_frame, wrap=tk.WORD, height=15)
        self.details_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.details_text.config(state=tk.DISABLED)

        # Load JSON Data
        self.load_data()

    def load_data(self):
        json_file_path = r"D:\Service portal\knowledge portal\Mybell_Resolutions.json"
        if not os.path.exists(json_file_path):
            messagebox.showerror("Error", f"The file '{json_file_path}' was not found.")
            self.data = []
            return

        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Error decoding JSON from '{json_file_path}'.")
            self.data = []

    def search_issues(self, event=None):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return

        self.results_tree.delete(*self.results_tree.get_children())

        for issue in self.data:
            if query in issue["IssueName"].lower():
                self.results_tree.insert("", tk.END, values=(
                    issue["IssueName"],
                    issue["Functionality"],
                    issue["Area"],
                    issue["LOB"]
                ))

    def display_details(self, event):
        selected_item = self.results_tree.selection()
        if not selected_item:
            return

        item = self.results_tree.item(selected_item)
        issue_name = item["values"][0]

        for issue in self.data:
            if issue["IssueName"] == issue_name:
                self.details_text.config(state=tk.NORMAL)
                self.details_text.delete("1.0", tk.END)
                self.details_text.insert(tk.END, f"Issue Name: {issue['IssueName']}\n")
                self.details_text.insert(tk.END, f"Functionality: {issue['Functionality']}\n")
                self.details_text.insert(tk.END, f"Area: {issue['Area']}\n")
                self.details_text.insert(tk.END, f"Line of Business: {issue['LOB']}\n\n")
                self.details_text.insert(tk.END, "Resolutions:\n")
                for resolution in issue["Resolutions"]:
                    self.details_text.insert(tk.END, f"  Due To: {resolution['DueTo']}\n")
                    self.details_text.insert(tk.END, "  Triaging Steps:\n")
                    for step in resolution["TriagingSteps"]:
                        self.details_text.insert(tk.END, f"    - {step}\n")
                    self.details_text.insert(tk.END, "\n")
                self.details_text.config(state=tk.DISABLED)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = ITServiceApp(root)
    root.mainloop()
