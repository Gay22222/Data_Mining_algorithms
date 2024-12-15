import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import io
from io import BytesIO
from graphviz import Digraph
import numpy as np
from collections import defaultdict
import matplotlib.pyplot
import statistics
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


# Thêm thư mục chứa Graphviz vào PATH
graphviz_path = os.path.abspath("libs/Graphviz")
os.environ["PATH"] += os.pathsep + graphviz_path