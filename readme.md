# SimpleMicroblogAPI

This is a simple anonymous microblogging API similar to Twitter / X used as a demonstration for handling API requests as part of the [Intro to Svelte Workshop (2026)](https://github.com/ProgSoc/svelte-workshop-demo-2026) that I hosted for UTS Programmers' Society (18/09/2026).

### Installation

```bash
# Optional: create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the API

```bash
python main.py
```

The server starts in debug mode at **http://localhost:5000**.

## API Reference

| Method | Endpoint                    | Description                                  | Request body                                               | Success | Errors                                                      |
| ------ | --------------------------- | -------------------------------------------- | ---------------------------------------------------------- | ------- | ----------------------------------------------------------- |
| `GET`  | `/api/posts`                | Get the latest posts (up to 50)              | None                                                       | `200`   | None                                                        |
| `GET`  | `/api/posts/<post_id>`      | Get a single post along with its comments    | None                                                       | `200`   | `404` Post not found                                        |
| `GET`  | `/api/user/<user_id>`       | Get a user by ID                             | None                                                       | `200`   | `404` User not found                                        |
| `GET`  | `/api/user/<user_id>/posts` | Get posts made by a specific user (up to 50) | None                                                       | `200`   | `404` User not found                                        |
| `POST` | `/api/post`                 | Create a new post                            | `user` (required), `content` (required, max 67 characters) | `201`   | `400` Missing `user` or `content`<br>`413` Content too long |
| `POST` | `/api/comment/<post_id>`    | Add a comment to an existing post            | `user` (required), `content` (required)                    | `201`   | `404` Post not found                                        |
