
# FastAPI Chatbot Application

This project is a simple chatbot service using FastAPI, SQLModel (SQLite), and OpenAI's GPT model to answer user questions. It also provides functionality for managing users, storing chat histories, and health checking the service.

## Features

- **User Management**: Initialize new users with roles.
- **Chatbot Interaction**: Ask a question to the chatbot and get a response from OpenAI's GPT model.
- **Chat History**: Retrieve chat history for a specific user.
- **Health Check**: Check the service health, including database and OpenAI system availability.

## Project Structure

- **app**: Contains the core application logic and API endpoints.
    - **routers**: Contains API routers for user, chatbot, and system routes.
    - **models**: Defines SQLModel database models.
    - **crud**: Contains functions to interact with the database.
    - **utils**: Includes utility functions, like interacting with OpenAI's API.
    - **database**: Contains the database session and initialization logic.
    - **main.py**: The entry point for the FastAPI application.
  
- **tests**: Contains tests for the application's API endpoints.
  
## Dependencies

- FastAPI
- SQLAlchemy
- SQLModel
- OpenAI
- dotenv
- pytest

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/alejomjc/ChatBot.git
    cd ChatBot
    ```

2. Create a `.env` file in the root directory with the following content:
    ```ini
    OPENAI_API_KEY=your_openai_api_key
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Initialize the database:
    ```bash
    python -m app.database.init_db
    ```

5. Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```

6. The application will be available at `http://localhost:8000`.

## API Endpoints

### 1. `/init_user`
- **POST**: Initializes a new user with a specific role.
  
  **Request Body**:
  ```json
  {
    "username": "test_user",
    "role": "admin"
  }
  ```

  **Response**:
  ```json
  {
    "message": "User created",
    "user": {
      "id": 1,
      "username": "test_user",
      "role": "admin"
    }
  }
  ```

### 2. `/ask`
- **POST**: Ask a question to the chatbot and get a response.

  **Request Body**:
  ```json
  {
    "username": "test_user",
    "question": "What are common workplace risks?"
  }
  ```

  **Response**:
  ```json
  {
    "response": "Common workplace risks include slips, trips, falls, and ergonomic hazards."
  }
  ```

### 3. `/history/{username}`
- **GET**: Retrieve the chat history for a specific user.

  **Response**:
  ```json
  {
    "history": [
      {
        "question": "What are common workplace risks?",
        "response": "Common workplace risks include slips, trips, falls, and ergonomic hazards."
      }
    ]
  }
  ```

### 4. `/health`
- **GET**: Check the health of the service, including the database and GPT system.

  **Response**:
  ```json
  {
    "service": "ok",
    "database": "ok",
    "gpt": "ok"
  }
  ```

## Testing

To run tests for the application:

1. Install testing dependencies:
    ```bash
    pip install pytest
    ```

2. Run the tests:
    ```bash
    pytest tests/tests_endpoints.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
