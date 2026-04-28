import sys
import os

# Add project root to sys.path so "backend.app.main" resolves correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.main import app
