# Full Stack Bookstore API Backend

## Motivation
This project provides a platform for publishers and students to access books in a bookstore.
- Guests can see only books, but not their authors
- Registered students can view books and their authors
- Publishers (or Administrators) can view, add, edit and delete books and authors

The Endpoint can be accessed at
https://kcemenikecapstone.herokuapp.com

## API
Non-guests must be authenticated. I have provided a postman collection that you may use to test the API as well

### Endpoints

#### Public access
**GET** `/books`

Displays a list of books

```
curl -X GET https://kcemenikecapstone.herokuapp.com/books
```

Sample response

```
{
    "books": [
        {
            "category": "Technology",
            "id": 1,
            "title": "Python Fundamentals",
            "year": 1999
        }
    ],
    "success": true
}
```

#### Students access
**GET** `/authors`

Shows a list of authors

```
curl -X GET https://kcemenikecapstone.herokuapp.com/authors \
  -H 'Authorization: Bearer <TOKEN>' \

```

Sample response

```
{
    "authors": [
        {
            "firstname": "Kelechi",
            "id": 1,
            "lastname": "EMENIKE"
        }
    ],
    "success": true
}
```

#### Admin access

**POST** `/authors`

Adds an author to the database

```
curl -X POST \
  https://kcemenikecapstone.herokuapp.com/authors \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "firstname": "Kelechi",
    "lastname": "EMENIKE",
}'
```
Sample response

```
{
    "author": [
        {
            "firstname": "Kelechi",
            "id": 1,
            "lastname": "EMENIKE"
        }
    ],
    "success": true
}
```
**POST** `/books`

Add a new book

```
curl -X POST \
  https://kcemenikecapstone.herokuapp.com/books \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Python Fundamentals",
    "year": 2020
    "category": "Technology"
}' \

```
Sample response
```
{
    "title": "Python Fundamentals",
    "year": 1999,
    "category": "Technology"
}
```

**PATCH** `/authors/<id>`

Modifies an author

```
curl -X PATCH \
  https://kcemenikecapstone.herokuapp.com/authors/1 \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "firstname": "Igoma"
}'
```
Sample response
```
{
    "author": [
        {
            "firstname": "Igoma",
            "id": 1,
            "lastname": "EMENIKE"
        }
    ],
    "success": true
}
```

**PATCH** `/books/<id>`

Modifies an author

```
curl -X PATCH \
  https://kcemenikecapstone.herokuapp.com/books/1 \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Python Basics"
}'
```
Sample response
```
{
    "book": [
        {
            "category": "Technology",
            "id": 1,
            "title": "Python Basics",
            "year": 1999
        }
    ],
    "success": true
}
```

**DELETE** `/authors/<id>`

Deletes an author

```
curl -X DELETE \
  https://kcemenikecapstone.herokuapp.com/authors/1 \
  -H 'Authorization: Bearer <TOKEN> ' \

```
Sample response
```
{
    "delete": 2,
    "success": true
}
```

**DELETE** `/books/<id>`

Deletes an author

```
curl -X DELETE \
  https://kcemenikecapstone.herokuapp.com/books/1 \
  -H 'Authorization: Bearer <TOKEN> ' \

```
Sample response
```
{
    "delete": 1,
    "success": true
}
```
## Installation



### Installing Dependencies

#### Python and Pip
- Requires Python 3.7+
- Requirements can be setup by running pip -r requirements.txt


### Running the server

To run the server, execute:

```bash
python manage.py runserver
```

## Testing

I have included a tests.py that follows TDD principles. To test the API, kindly create a 'test_db' in postgres, then run:

```bash
python test_app.py
```
