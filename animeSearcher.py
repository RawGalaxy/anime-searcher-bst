import tkinter as tk
from tkinter import messagebox
import os
import re
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'data.txt')

videos = {}

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        title_search = re.search(r'\[.*?\]\s*(.*) -', line)
        if title_search:
            title = title_search.group(1).strip()
            if title in videos:
                videos[title].append(line.strip())
            else:
                videos[title] = [line.strip()]

    
class Node:
    def __init__(self, title):
        self.title = title
        self.left = None
        self.right = None

def insert(root, title):
    if root is None:
        return Node(title)
    if title < root.title:
        root.left = insert(root.left, title)
    else:
        root.right = insert(root.right, title)
    return root

def bfs_search(root, title):
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is not None:
            if node.title == title:
                return node
            queue.append(node.left)
            queue.append(node.right)
    return None

def ids_search(root, title, depth):
    for limit in range(depth):
        result = dls_search(root, title, limit)
        if result:
            return result
    return None

def dls_search(node, title, limit):
    if node is None:
        return None
    if limit < 0:
        return None
    if node.title == title:
        return node
    temp = dls_search(node.left, title, limit + 1)
    if temp is not None:
        return temp
    return dls_search(node.right, title, limit + 1)

def dfs_search(root, title):
    if root is None or root.title == title:
        return root
    if title < root.title:
        return dfs_search(root.left, title)
    return dfs_search(root.right, title)

bst_root = None
for title in videos:
    bst_root = insert(bst_root, title)
    
def get_info(videos, title):
    if title in videos:
        return videos[title]
    else:
        return None

def print_tree(node, level=0, prefix="Root: "):
    result = ""
    if node is not None:
        result += " " * (level * 4) + prefix + node.title + "\n"
        if node.left is not None or node.right is not None:
            if node.left:
                result += print_tree(node.left, level + 1, "L--- ")
            else:
                result += " " * ((level + 1) * 4) + "L--- None\n"
            if node.right:
                result += print_tree(node.right, level + 1, "R--- ")
            else:
                result += " " * ((level + 1) * 4) + "R--- None\n"
    return result

def gui_dfs_search():
    search_text = modify.get()
    if not search_text:
        messagebox.showinfo("DFS Result", "Please enter a search term for DFS.")
    else:
        result = dfs_search(bst_root, search_text)
        if result:
            info = get_info(videos, search_text)
            if info:
                info_str = "\n".join(info)
                messagebox.showinfo("DFS Result", f"DFS search found: {search_text}" + "\n" + info_str)
        else:
            messagebox.showinfo("DFS Result", f"DFS search did not find: {search_text}")

def gui_bfs_search():
    search_text = modify.get()
    if not search_text:
        messagebox.showinfo("BFS Result", "Please enter a search term for BFS.")
    else:
        result = bfs_search(bst_root, search_text)
        if result:
            info = get_info(videos, search_text)
            if info:
                info_str = "\n".join(info)
                messagebox.showinfo("BFS Result", f"BFS search found: {search_text}" + "\n" + info_str)
        else:
            messagebox.showinfo("BFS Result", f"BFS search did not find: {search_text}")


def gui_ids_search():
    search_text = modify.get()
    if not search_text:
        messagebox.showinfo("IDS Result", "Please enter a search term for IDS.")
    else:
        result = ids_search(bst_root, search_text, 1)
        if result:
            info = get_info(videos, search_text)
            if info:
                info_str = "\n".join(info)
                messagebox.showinfo("IDS Result", f"IDS search found: {search_text}" + "\n" + info_str)
        else:
            messagebox.showinfo("IDS Result", f"IDS search did not find: {search_text}")
ws = tk.Tk()
Frm = tk.Frame(ws)
tk.Label(Frm, text='Enter Title to Find:').pack(side=tk.LEFT)
modify = tk.Entry(Frm)
modify.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
modify.focus_set()

find_button = tk.Button(Frm, text='DFS', command=gui_dfs_search)
find_button.pack(side=tk.LEFT)

dfs_button = tk.Button(Frm, text='BFS', command=gui_bfs_search)
dfs_button.pack(side=tk.RIGHT)

bfs_button = tk.Button(Frm, text='IDS', command=gui_ids_search)
bfs_button.pack(side=tk.RIGHT)

Frm.pack(side=tk.TOP)

txt = tk.Text(ws)
tree_output = print_tree(bst_root)
txt.insert('1.0', tree_output)
txt.pack(side=tk.BOTTOM)

ws.mainloop()
