# Gameshop
Web software development course project

  Gameshop is a platform where developers can "sell" JS games they developed through a mockup payment service created
  for the course. No real transactions with this app. Users can Sign Up to the service as regular users or developers
  and buy games others have developed or add new game for sale. One game simple Brick Pong game has been developed for
  this project for demonstration. The game service supports loading and saving gamestaes and scores.
    
**Front-end**
- HTML5
- CSS
- Twitter Bootstrap
- Jquery
- Javascript

**Back-end**
- PosgresDB
- Django
- Python

Project can be found [here](https://indiegames.herokuapp.com/)  
  
  To run this locally:
  1. Pull the project
  2. Install the dependencies found in [requirements](./requrements.txt) wit ```pip install 'dependency'```
  3. run migrations in the manage.py-folder with ```python manage.py makemigrations``` and ```python manage.py makemigrations```
  4. create a superuser ```python manage.py createsuperuser```
  5. run the server ```python manage.py runserver```
  6. go to your Localhost:8000/admin and sign in with the super user
  7. You need to add a facebook app to get the site working in the admin-site 
  (you can create a facebook-app here [developers.facebook](https://developers.facebook.com/)). 
  All you need to do is to insert the url in Sites-table and App-ID and secret key of your app in Social-apps-table
  8. After adding the app you should be ready to go!
