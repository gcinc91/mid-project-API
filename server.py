from src.app import app
import src.controllers.controller
import os
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    app.run("0.0.0.0", os.getenv('PORT',3000), debug=True)