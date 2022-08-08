remake_db:
	rm db.sqlite3
	./manage.py makemigrations
	./manage.py migrate
