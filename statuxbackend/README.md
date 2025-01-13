clone the repository to your computer by running:
git clone https://github.com/thegreenphoton/internsurf.git

install dependencies by running: pip install -r requirements.txt

create a virtual environment by running: python3 -m venv venv

activate the virtual environment by running: source venv/bin/activate

initialize the database by running: python create_db.py

now run the app by running:
  export FLASK_APP=app.py   # On macOS/Linux
  set FLASK_APP=app.py      # On Windows
  flask run

Once the app is running, you can access it in your web browser by going to http://127.0.0.1:5000 (or the specified host and port).



