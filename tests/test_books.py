"""Integration tests for the /books endpoints."""


VALID_BOOK = {"title": "Clean Code", "author": "Robert C. Martin", "price": 35.99}


class TestCreateBook:
    def test_create_returns_201(self, client):
        response = client.post("/books", json=VALID_BOOK)
        assert response.status_code == 201

    def test_create_returns_id(self, client):
        data = client.post("/books", json=VALID_BOOK).json()
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_create_invalid_price(self, client):
        response = client.post("/books", json={**VALID_BOOK, "price": -1})
        assert response.status_code == 422

    def test_create_missing_title(self, client):
        response = client.post("/books", json={"author": "Someone", "price": 9.99})
        assert response.status_code == 422


class TestListBooks:
    def test_list_returns_200(self, client):
        response = client.get("/books")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestGetBook:
    def test_get_existing_book(self, client):
        book_id = client.post("/books", json=VALID_BOOK).json()["id"]
        response = client.get(f"/books/{book_id}")
        assert response.status_code == 200
        assert response.json()["id"] == book_id

    def test_get_nonexistent_book(self, client):
        response = client.get("/books/999999")
        assert response.status_code == 404


class TestDeleteBook:
    def test_delete_existing_book(self, client):
        book_id = client.post("/books", json=VALID_BOOK).json()["id"]
        assert client.delete(f"/books/{book_id}").status_code == 204
        assert client.get(f"/books/{book_id}").status_code == 404

    def test_delete_nonexistent_book(self, client):
        assert client.delete("/books/999999").status_code == 404