"""
MedRadar Desktop App Launcher
Launches MedRadar in a dedicated standalone application window.
"""
import os
import sys
import threading
import time
import webbrowser

# Start backend in a background thread
def run_server():
    from app import app
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to initialize
    time.sleep(1.5)
    
    url = "http://127.0.0.1:5000"
    print(f"MedRadar App is running at {url}")
    
    # Try opening in dedicated app mode via Chrome/Edge if available
    opened = False
    for browser in ["chrome", "msedge", "edge"]:
        try:
            cmd = f'{browser} --app={url}'
            if os.system(cmd) == 0:
                opened = True
                break
        except Exception:
            pass
            
    if not opened:
        webbrowser.open(url)
        
    print("Press Ctrl+C to close the MedRadar app.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting MedRadar.")

