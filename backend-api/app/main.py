from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import redis
import psycopg2
import requests
from datetime import datetime

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database and cache connections
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Models
class WeatherResponse(BaseModel):
    city: str
    temp: float
    humidity: int
    conditions: str

class ForecastItem(BaseModel):
    date: str
    temp: float
    conditions: str

class WeatherDataResponse(BaseModel):
    current: WeatherResponse
    forecast: List[ForecastItem]

class HistoryItem(BaseModel):
    city: str
    timestamp: datetime

# Initialize connections
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def get_redis_connection():
    return redis.Redis.from_url(REDIS_URL)

# API Endpoints
@app.get("/api/weather", response_model=WeatherDataResponse)
async def get_weather(city: str):
    # Check cache first
    redis_conn = get_redis_connection()
    cached_data = redis_conn.get(f"weather:{city.lower()}")
    
    if cached_data:
        return WeatherDataResponse.parse_raw(cached_data)
    
    # If not in cache, fetch from weather service
    try:
        response = requests.get(
            f"http://weather-fetcher:5000/fetch-weather?city={city}&api_key={WEATHER_API_KEY}"
        )
        response.raise_for_status()
        weather_data = response.json()
        
        # Cache the result for 30 minutes
        redis_conn.setex(
            f"weather:{city.lower()}",
            1800,
            WeatherDataResponse(
                current=weather_data["current"],
                forecast=weather_data["forecast"]
            ).json()
        )
        
        # Save to history
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO search_history (city, timestamp) VALUES (%s, %s)",
            (city, datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return weather_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history", response_model=List[HistoryItem])
async def get_history():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT city, timestamp FROM search_history ORDER BY timestamp DESC LIMIT 10")
        rows = cur.fetchall()
        return [HistoryItem(city=row[0], timestamp=row[1]) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

# Initialize database tables
def initialize_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id SERIAL PRIMARY KEY,
            city VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Initialize on startup
initialize_database()
