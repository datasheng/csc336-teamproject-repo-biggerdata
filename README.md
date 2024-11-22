[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/NFzhPWeQ)

# CourseFlow

CourseFlow provides a seamless and efficient solution for university students navigating the complex - and often frustrating - course registration process.

## Server Setup Instructions

1. Install development headers and libraries

macOS (Homebrew)
```
brew install mysql-client pkg-config
```

Linux (Debian / Ubuntu)
```
sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config
```

2. Create virtual environment
```
python -m venv .venv
```

3. Activate virtual environment
```
source .venv/bin/activate
```

4. Install project dependencies in server directory
```
pip install -r requirements.txt
```

5. Add .env file containing the credentials
```
MY_HOST=localhost
MY_USER=MySQL_user
MY_PASSWORD=MySQL_password
MY_DB=MySQL_database
```

6. Run Flask server
```
python app.py
```

7. Open http://127.0.0.1:5000 in web browser
