"""Run the Flask chatbot app."""
import os

from dotenv import load_dotenv
load_dotenv()

from app import create_app
app = create_app()

if __name__ == "__main__":
<<<<<<< HEAD
    port = int(os.environ.get("PORT", 5010))
    print(f'PORT: {port}')  
=======
    port = int(os.environ.get("PORT", 5000))
>>>>>>> fdf7e3a2212363ac755e74c61f1bd39f279ff498
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "0") == "1")
