source .env/Scripts/activate
pip freeze > requirements.txt
cd project
python -m application.server.main
python -m application.client.main
