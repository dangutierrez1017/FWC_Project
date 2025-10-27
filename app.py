from flask import Flask
from src.controllers.routes import app
import os
print("Current working directory:", os.getcwd())
print("Template folder absolute path:", app.template_folder)

if __name__ == '__main__':
    app.run(debug=True)