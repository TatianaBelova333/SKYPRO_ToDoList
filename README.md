# ToDoList
___
**ToDoList** is a web application designed for creating and managing objectives and sharing them with other users.
The application has the following functions:
1. Registration/login/authentication via vk.com.

2. Creating objectives:
   * Setting a deadline and showing the time left till the deadline;
   * Choosing/adding/deleting/updating the objective category(e.g. personal, work, sports, education, etc.);
   * Choosing the objective priority(e.g. minor, major, critical, etc.);
   * Choosing the progress status(in progress, completed, pending, archived);
   * Sharing objectives with others via boards.

3. Updating objectives.
   * Updating the objective description;
   * Updating the objective status;
   * Updating the objective priority and category;

4. Deleting objectives.
   * After being deleted the objective becomes archived.

5. Searching for the objective by its name.
6. Filtering objectives by their status, category, priority, year, etc.
7. Adding comments to the objective.
8. Checking and/or creating new objectives via Telegram bot account.

___
### Requirements & Compatibility

* python = "^3.10"
* Django = "^4.1.1"
* django-environ = "^0.9.0"
* psycopg2-binary = "^2.9.3"
* djangorestframework = "^3.14.0"
* python-multipart = "^0.0.5"
* social-auth-app-django = "^5.0.0"
* django-filter = "^22.1"
* marshmallow-dataclass = "^8.5.9"
* requests = "^2.28.1"
* pytest-django = "^4.5.2"
* pytest-factoryboy = "^2.5.0"

---
### Installation
Set the following default values in your .env file.
* SECRET_KEY
* POSTGRES_PASSWORD
* POSTGRES_USER
* POSTGRES_DB
* POSTGRES_HOST
* VK_OAUTH2_KEY
* VK_OAUTH2_SECRET 
* TELEGRAM_BOT_TOKEN

Run command docker compose --build -d.


