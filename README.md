# Binance WebSocket API Price Tracker

Real-time cryptocurrency price tracking system that connects to Binance WebSocket API to fetch and store BTC/USDT prices.

## Features

- Real-time price updates via WebSocket connection
- Automatic price storage in PostgreSQL database
- REST API for historical price data
- Swagger/ReDoc API documentation
- WebSocket client connection support
- Periodic price saving (every 60 seconds)

## Technology Stack

- Python 3.11
- Django 5.1
- Django Channels
- Django REST Framework
- PostgreSQL
- WebSocket (Binance API)
- Swagger/ReDoc
- pytest for testing

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd WebSocket\ API\ Binance
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` file.

5. Apply migrations:

```bash
cd crypto_project
python manage.py migrate
```

## Running the Application

Start the server:

```bash
DJANGO_SETTINGS_MODULE=crypto_project.settings daphne -p 8000 crypto_project.asgi:application
```

Access the API documentation:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## API Endpoints

- `GET /api/prices/` - Get historical price data
- `WS /ws/prices/` - WebSocket connection for real-time prices

## WebSocket Client Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>Crypto Price Tracker</title>
</head>
<body>
    <div id="price"></div>
    <script>
        const ws = new WebSocket('ws://localhost:8000/ws/prices/');
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            document.getElementById('price').innerHTML = 
                `BTC/USDT: ${data.price} (${new Date(data.timestamp).toLocaleString()})`;
        };
    </script>
</body>
</html>
```

## Running Tests

```bash
pytest
```

## Project Structure

```
crypto_project/
├── crypto/
│   ├── consumers.py      # WebSocket consumer
│   ├── models.py         # Database models
│   ├── price_service.py  # Price fetching service
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API views
│   └── tests/            # Test files
├── crypto_project/
│   ├── asgi.py          # ASGI configuration
│   ├── settings.py      # Project settings
│   └── urls.py          # URL configuration
└── manage.py
```
