from typing import List
import os
import pathlib

max_levels = int(input("Print levels: "))

EXCLUDE_DIRS = [
    ".git", "githooks", "docs", "examples", "migrations", "testdata", # not code files
    "mock" # auto generated
]

COUNT_EXTENSIONS = [
    ".go",
]

class Node:
    def __init__(self, path):
        self.path = path
        self.base_path = str(pathlib.Path(path).parent.resolve())
        self.file_name = os.path.basename(path)
        self.isdir = os.path.isdir(self.path)
        self.is_count_extension = not self.isdir and any([self.path.endswith(ext) for ext in COUNT_EXTENSIONS])
        self.children: List['Node'] = []
        self.lines = 0

    def count_lines(self) -> int:
        if not self.isdir and self.is_count_extension:
            self._count_file_lines()
            return self.lines

        elif self.isdir:
            # Create a node for each child and append to children list
            child_names = os.listdir(self.path)
            file_paths = []
            dir_paths = []
            for child_name in child_names:
                if child_name not in EXCLUDE_DIRS:
                    child_path = os.path.join(self.path, child_name)
                    if os.path.isdir(child_path):
                        dir_paths.append(child_path)
                    else:
                        file_paths.append(child_path)

            for path in file_paths+dir_paths:
                self.children.append(Node(path))
        
            # iterate through all children and let them count their lines
            for child in self.children:
                self.lines += child.count_lines()

            return self.lines

        else:
            # Not a golang file
            return 0

    def _count_file_lines(self):
        assert(not self.isdir)

        with open(self.path) as file:
            try:
                for line in file:
                    if line != "\n" and not line.strip().startswith("//"):
                        self.lines += 1
            except UnicodeDecodeError as e:
                print(f"===ERROR IN FILE {file}===")
                print(f"=== lines:{self.lines} ===")
                print(str(e))

    def print_tree(self, max_depth=1000, level=0):
        if level > max_depth:
            return

        if self.is_count_extension:
            print("| "*level + "  " + f"{self.lines:6.0f} --- {self.file_name}")
        
        if self.isdir:
            if self.lines > 0:
                print("| "*level + f"+ {self.lines:6.0f} --- {self.file_name}")

            for child in self.children:
                child.print_tree(max_depth, level=level+1)


root_folder = ""
root_path = os.getcwd() if not root_folder else os.path.join(os.getcwd(), root_folder)
root = Node(root_path)
root.count_lines()
print("\n"*2)
root.print_tree(max_levels)