activate virtual environment:
.\env\Scripts\activate

update requirements txt file
pip freeze > requirements.txt

docker-compose down  # Stop containers
docker-compose build --no-cache  # Rebuild without cache
docker-compose up  # Start again

