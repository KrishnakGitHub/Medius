"# Medius" 


![Screenshot (9)](https://github.com/KrishnakGitHub/Medius/assets/41542288/55479c7f-7c1a-49ec-b145-afc1d41752c8)

![Screenshot (10)](https://github.com/KrishnakGitHub/Medius/assets/41542288/5515c0c1-03f0-4746-83f5-5dbe0cfe3416)


# Django File Upload and Email Summary Report

This Django project allows users to upload Excel/CSV files, generates a summary report of the uploaded data, and emails the report to specified recipients.

## Features

- Upload Excel or CSV files.
- Generate a summary report based on the uploaded data.
- Email the summary report as an attachment.

## Requirements

- requirements.txt
- Run command 'pip install requirements.txt'

## Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/yourusername/Medius.git
cd Medius

- pip install -r requirements.txt
- Create a .env file in the root directory and add
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com
DEFAULT_TO_EMAIL=tech@themedius.ai,hr@themedius.ai

- python manage.py migrate
- python manage.py runserver


