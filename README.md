# UAI FC Arena

UAI FC Arena is an interactive platform where users can create and battle AI-powered bots using language models. This project combines elements of AI, natural language processing, and gamification to create a unique and educational experience.

## Features

- User authentication and management
- Bot creation and customization
- Battle system with LLM-generated actions
- Support for multiple LLM providers (OpenAI, Cerebras, Groq)
- Real-time prompt evaluation
- Leaderboard system
- NPC bots for training

## Tech Stack

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript (jQuery)
- Database: SQLite (development), PostgreSQL (production)
- ORM: SQLAlchemy
- CSS Framework: Bootstrap 4

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/uai-fc-arena.git
   cd uai-fc-arena
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the `backend` directory with the following content:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///database.db
   ```

5. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```

7. Open your browser and navigate to `http://localhost:5000` to access the application.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
