import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import defaultdict, deque

class JobSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Scheduling System using Graphs")
        self.root.geometry("700x550")
        
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self.all_nodes = set()

        # --- UI Components ---
        # Frame for Inputs
        input_frame = tk.LabelFrame(root, text=" Define Job Dependencies ", font=("Arial", 11, "bold"), padx=10, pady=10)
        input_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(input_frame, text="Pre-requisite Job (u):").grid(row=0, column=0, sticky="w", pady=5)
        self.u_entry = tk.Entry(input_frame, width=15)
        self.u_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Dependent Job (v):").grid(row=0, column=2, sticky="w", pady=5)
        self.v_entry = tk.Entry(input_frame, width=15)
        self.v_entry.grid(row=0, column=3, padx=5, pady=5)

        self.add_btn = tk.Button(input_frame, text="Add Dependency", bg="#4CAF50", fg="white", command=self.add_edge)
        self.add_btn.grid(row=0, column=4, padx=10, pady=5)

        # Action Frame
        action_frame = tk.Frame(root)
        action_frame.pack(fill="x", padx=15, pady=5)

        self.schedule_btn = tk.Button(action_frame, text="Compute Job Schedule", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), command=self.compute_schedule)
        self.schedule_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(action_frame, text="Reset Graph", bg="#f44336", fg="white", font=("Arial", 10, "bold"), command=self.reset_graph)
        self.reset_btn.pack(side="left", padx=5)

        # Output Display Frame
        output_frame = tk.LabelFrame(root, text=" Execution Schedule & Logs ", font=("Arial", 11, "bold"), padx=10, pady=10)
        output_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.output_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=75, height=15, font=("Courier", 10))
        self.output_area.pack(fill="both", expand=True)

    def add_edge(self):
        u = self.u_entry.get().strip()
        v = self.v_entry.get().strip()
        if not u or not v:
            messagebox.showerror("Error", "Both job fields must be filled!")
            return
        
        self.graph[u].append(v)
        self.in_degree[v] += 0  # ensure v exists in in_degree
        if u not in self.in_degree:
            self.in_degree[u] = 0
        self.in_degree[v] += 1
        
        self.all_nodes.add(u)
        self.all_nodes.add(v)

        self.output_area.insert(tk.END, f"Added Dependency: Job '{u}' must run before Job '{v}'\n")
        self.u_entry.delete(0, tk.END)
        self.v_entry.delete(0, tk.END)

    def compute_schedule(self):
        # Kahn's Algorithm for Topological Sort
        in_deg_copy = self.in_degree.copy()
        queue = deque([node for node in self.all_nodes if in_deg_copy[node] == 0])
        topo_order = []

        while queue:
            curr = queue.popleft()
            topo_order.append(curr)
            for neighbor in self.graph[curr]:
                in_deg_copy[neighbor] -= 1
                if in_deg_copy[neighbor] == 0:
                    queue.append(neighbor)

        self.output_area.insert(tk.END, "-"*50 + "\n")
        if len(topo_order) == len(self.all_nodes):
            self.output_area.insert(tk.END, "SUCCESS: Valid Job Schedule Found (Topological Order):\n")
            self.output_area.insert(tk.END, " -> ".join(topo_order) + "\n")
        else:
            self.output_area.insert(tk.END, "ERROR: Cycle detected! Circular dependency found. Cannot schedule jobs.\n")
        self.output_area.insert(tk.END, "-"*50 + "\n")
        self.output_area.see(tk.END)

    def reset_graph(self):
        self.graph.clear()
        self.in_degree.clear()
        self.all_nodes.clear()
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, "Graph has been reset.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = JobSchedulerApp(root)
    root.mainloop()