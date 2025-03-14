""" Tying it all together with 'main.py' """

from src.app import app

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))  # Use Render's PORT environment variable
    app.run(host="0.0.0.0", port=port, debug=True)
