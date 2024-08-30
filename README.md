# Skype Listener

A Python-based Skype bot that listens to a Skype group for cellphone numbers, updates a MySQL database with the user information, and returns the user ID.

## Features

- Listens for new messages in a Skype group.
- Detects cellphone numbers and queries a MySQL database.
- Returns the user ID associated with the cellphone number.

## Prerequisites

- Docker
- Python 3.9+
- MySQL Database

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/vida-lashani/Skype_Listener_Bot.git
cd skype-listener-main
```
Running with Docker

Build the Docker Image:
```bash
docker build -t skype-bot .
```
Run the Docker Container:
```bash
docker run -d skype-bot
```
or run using Docker Compose

Start the Bot:
```bash
docker-compose up -d
```
