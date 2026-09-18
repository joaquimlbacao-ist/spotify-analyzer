import os
import threading
import webbrowser
import time
from src.api import app

def open_browser():
    time.sleep(2)
    port = int(os.getenv('PORT', 8000))
    webbrowser.open(f"http://127.0.0.1:{port}")

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    
    # Only open browser for local development
    if os.getenv('FLASK_ENV') != 'production':
        threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(host='0.0.0.0', port=port, debug=False)