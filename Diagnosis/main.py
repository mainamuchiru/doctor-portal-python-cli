# import argparse
# from typing import Iterable, List, Optional

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from menu.auth_menu import auth_menu



if __name__ == "__main__":
    auth_menu()
