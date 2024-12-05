import os

# Thêm thư mục chứa Graphviz vào PATH
graphviz_path = os.path.abspath("libs/Graphviz")
os.environ["PATH"] += os.pathsep + graphviz_path