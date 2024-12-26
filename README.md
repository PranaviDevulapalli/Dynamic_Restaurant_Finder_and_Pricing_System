# Dynamic Restaurant Finder and Pricing System

A dynamic pricing system built for restaurants using Python and Django. This system adjusts menu prices based on various factors like location, time of day, and weather conditions. The system integrates Google Maps API for restaurant data and OpenWeatherMap API for weather-related factors to calculate dynamic pricing.

## Features

- **Dynamic Menu Pricing**: Prices are adjusted based on the time of day, location, and weather conditions.
- **Restaurant Finder**: The system can find nearby restaurants using Google Maps API.
- **Weather Integration**: Fetch real-time weather data using the OpenWeatherMap API to adjust menu pricing based on external conditions.
- **User Authentication**: Secure login and authentication using JWT (JSON Web Token) for both customers and restaurant owners.

## Technologies Used

- **Python**: The main programming language for backend development.
- **Django**: The web framework used to build the application.
- **Google Maps API**: Used to retrieve restaurant data based on location.
- **OpenWeatherMap API**: Used to fetch real-time weather data to influence pricing.
- **JWT (JSON Web Tokens)**: Used for authentication and authorization.
- **SQLite/PostgreSQL**: Database for storing restaurant and user data.

## Installation

To get started with this project locally, follow these steps:

### Prerequisites

- Python 3.x
- pip (Python's package installer)
- Virtual environment (recommended)

### Steps to Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Dynamic_Restaurant_Finder_and_Pricing_System.git
   cd Dynamic_Restaurant_Finder_and_Pricing_System
