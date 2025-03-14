""" Tying it all together with 'main.py' """

from flask import Flask

app = Flask(__name__)

@app.route("/")  # Add a route for the home page
def home():
    return "Flask App is Running Successfully on Render!"

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))  # Use Render's PORT environment variable
    app.run(host="0.0.0.0", port=port, debug=True)

