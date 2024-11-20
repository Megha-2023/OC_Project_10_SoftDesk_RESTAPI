# SoftDesk

The project is an issue tracking application designed for all three platforms(Web, Android and iOS). It enables users to design different projects, add users to a project, create issues in the project and add comments on each issues. It contains API endpoints that serve the data. The application complies to OWASP security measures.

## Setup

### 1. Clone the Repository

First, clone this repository to your local machine. Then navigate inside the folder softdesk and open command prompt from inside the cloned repository

### 2. Create Virtual Environment

To create virtual environment, install virtualenv package of python and activate it by following command on terminal:

```python
pip install virtualenv
python -m venv <<name_of_env>>
Windows: <<name_of_env>>\Scripts\activate.bat

Powershell: <<name_of_env>>\Scripts\activate

Unix/MacOS: source <<name_of_env>>/bin/acivate
```

### 3. Requirements

To install required python packages, copy requirements.txt file and then run following command on terminal:

```python
pip install requirements.txt
```

### 4. Start Server

On the terminal enter following command to start the server:

```python
python manage.py runserver
```

### 5. Test all endpoints in Postman

Once server is running, you can test all API endpoints in Postman app as per its documentation.
