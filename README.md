Straight forward contact manager. I am using token authentication rather than sessions, so CSRF exemptions are applied to the API endpoints (views). Additionally, I implemented my own fuzzy search using Levenshtein distance. I omitted the use of environment variables for DB info and the secret key since there is no plan to fully deploy this project.

### Stack
* Django REST Framework
* PostgreSQL
* React
