import sys
import os

# Thêm đường dẫn thư mục gốc vào sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import reset_database
from views.gui import gui

if __name__ == "__main__":
    reset_database()
    gui()           