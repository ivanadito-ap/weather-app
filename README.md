# 🌤️ Weather Forecaster App

## 📝 Description
Cloud Three Weather Forecaster is a web application developed as a project for the Cloud Computing course. It allows users to search for and view the current weather and a 5-day forecast for a specified city. The application is built using a microservices architecture, containerized with Docker, and orchestrated with Docker Compose.

## Features
* 🌡️ **Current Weather Data**: Get up-to-date weather information for any city.
* 📅 **5-Day Forecast**: View a 5-day weather forecast.
* ⚡ **Caching**: Implements Redis caching for faster responses on repeated city searches, reducing external API calls.
* 🕓 **Search History**: Logs user search activity (city and timestamp) to a PostgreSQL database.
* 💻 **Responsive UI**: User-friendly interface built with React.

## 🛠️ Tech Stack & Architecture

### Technologies Used:
* **Frontend**: React.js
* **Backend API**: FastAPI (Python)
* **Weather Fetcher Service**: Flask (Python)
* **Database**: PostgreSQL
* **Caching**: Redis
* **Reverse Proxy**: Nginx
* **Containerization**: Docker & Docker Compose

### 🧱 Architecture Overview:
The application is composed of six Docker containers that work together:

1.  **`frontend` (React.js)**:
    * 🎨 Serves the user interface.
    * Users input a city name, and it communicates with the `backend-api` to fetch and display weather data.
    * Accessible via Nginx.

2.  **`backend-api` (FastAPI, Python)**:
    * 🧠 The main backend service that handles requests from the `frontend`.
    * Manages business logic:
        * Checks Redis cache for existing weather data.
        * If data is not cached or stale, it calls the `weather-fetcher` service.
        * Stores new weather data in Redis.
        * Logs search queries to the PostgreSQL `database`.
        * Returns data to the `frontend`.

3.  **`weather-fetcher` (Flask, Python)**:
    * ☁️ An internal microservice dedicated to fetching weather data.
    * Called by the `backend-api`.
    * Retrieves current weather and forecast data from an external provider (e.g., OpenWeatherMap).

4.  **`database` (PostgreSQL)**:
    * 🗃️ Stores user search history (city searched and timestamp).

5.  **`cache` (Redis)**:
    * 🚀 Caches weather data for cities that have been searched.
    * This speeds up responses for subsequent requests for the same city and reduces the load on the `weather-fetcher` service and the external API.

6.  **`nginx` (Nginx)**:
    * 🔀 Acts as a reverse proxy.
    * Manages incoming HTTP requests and routes them to the appropriate service (primarily the `frontend` and `backend-api`).
    * Exposes the application on port 80.

## 🔁 How It Works
1.  The user navigates to the web application, accessing the React.js `frontend` through `Nginx`.
2.  The user types a city name into the search bar and submits.
3.  The `frontend` sends this city name to the `backend-api` (FastAPI service).
4.  The `backend-api` first checks `Redis` to see if weather data for this city is already cached.
    * If cached and not stale: The `backend-api` returns the cached data to the `frontend` (skip to step 9).
    * If not cached or stale: The `backend-api` proceeds to the next step.
5.  The `backend-api` calls the `weather-fetcher` (Flask service), passing the city name and an API key.
6.  The `weather-fetcher` service fetches the current weather and 5-day forecast data from an external weather data provider (OpenWeatherMap).
7.  The `weather-fetcher` service returns the weather data to the `backend-api`.
8.  The `backend-api` stores/updates the fetched weather data in `Redis` for future requests (cached for 30 minutes).
9.  Simultaneously, the `backend-api` logs the user's search activity (city searched, timestamp) into the `PostgreSQL database`.
10. The `backend-api` sends the weather data back to the React.js `frontend`.
11. The `frontend` displays the current weather and forecast information to the user.

## 🚀 Getting Started

### ✅ Prerequisites
* Docker
* Docker Compose

### 📦 Installation & Running
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ivanadito-ap/weather-app.git
    cd weather-app
    ```

2.  **Run the application using Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    This command will build the images if they don't exist and start all the services in detached mode.

3.  **Access the application:**
    Open your web browser and navigate to:
    `http://localhost`
    (Nginx reverse proxy is configured to listen on port 80).

    * The frontend will be available, and it will make API calls to `http://localhost/api/...` which Nginx routes to the `backend-api` service.

## 🔧 API Endpoints

### Backend API (FastAPI - `backend-api` service)
These are the primary endpoints used by the frontend:

* **`GET /api/weather?city={city_name}`**:
    * Fetches current weather and 5-day forecast for the specified `{city_name}`.
    * Example: `/api/weather?city=London`

* **`GET /api/history`**:
    * Retrieves the last 10 search history entries.

### Weather Fetcher Service (Flask - `weather-fetcher` service)
This is an internal service endpoint called by the `backend-api`:

* **`GET /fetch-weather?city={city_name}&api_key={your_api_key}`**:
    * Fetches weather data from the external OpenWeatherMap API.
    * *Note: This endpoint is intended for internal use by the `backend-api` service.*

## 📁 Project Structure
```
.
├── backend-api/          # FastAPI application (main backend logic)
│   ├── app/
│   │   └── main.py       # FastAPI application code
│   ├── Dockerfile
│   └── requirements.txt  # Python dependencies
├── frontend/             # React.js application (UI)
│   ├── public/
│   ├── src/              # React components and logic
│   │   ├── App.js
│   │   └── ...
│   ├── Dockerfile
│   └── package.json      # Node.js dependencies
├── weather-fetcher/      # Flask application (fetches from external API)
│   ├── app/
│   │   └── main.py       # Flask application code
│   ├── Dockerfile
│   └── requirements.txt  # Python dependencies
├── nginx/                # Nginx configuration
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml    # Docker Compose configuration for all services
└── README.md             # This file
```

## 👥 Team/Contributors
* Ivan Adito Arba Putra
* I Putu Herjuna Manasye Suarthana
* Mohammad Azka Khairur Rahman

## 🎓 Course Information
* Cloud Computing Course Project
* Universitas Gadjah Mada   
* Muhammad Husni Santriaji S.Si., M.T., M.S., Ph.D.
