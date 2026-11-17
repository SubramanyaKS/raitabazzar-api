# RaitaBazzar Backend API 🌾🚀

FastAPI-powered backend for **RaitaBazzar** — a digital agricultural marketplace empowering Karnataka farmers and buyers with live APMC mandi prices, vernacular crop discovery (Kannada, Hindi, Kanglish, English), and hyper-local agricultural weather forecasts.

---

## 📑 Table of Contents

- [Features](#-features)
- [Architecture & Project Structure](#-architecture--project-structure)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Configuration](#environment-configuration)
  - [Running the Server](#running-the-server)
- [API Reference](#-api-reference)
  - [1. Health Check](#1-health-check)
  - [2. Live Mandi Rates](#2-live-mandi-rates)
  - [3. Vernacular Crop Search & NLP](#3-vernacular-crop-search--nlp)
  - [4. Master Crops Catalog](#4-master-crops-catalog)
  - [5. Agricultural Weather Service](#5-agricultural-weather-service)
- [Running Automated Tests](#-running-automated-tests)
- [Roadmap](#-roadmap)

---

## 🌟 Features

- **Live Mandi Rates (`AGMARKNET`)**: Fetches real-time market prices from `data.gov.in`. Automatically merges and falls back to verified Karnataka APMC benchmark prices whenever upstream feeds are delayed or offline.
- **Vernacular Crop Search & NLP**: Multi-lingual, phonetic, and fuzzy crop resolution across **Kannada script** (`ಈರುಳ್ಳಿ`, `ಟೊಮೇಟೊ`), **Hindi script** (`प्याज`), **English** (`onion`), and **Kanglish/Hinglish** transliterations (`eerulli`, `pyaz`, `alugadde`).
- **APMC Benchmark Price Linking**: Dynamically links matched crop searches with local or district APMC benchmarks (modal, minimum, and maximum prices).
- **Localized Weather & Farming Advisories**: Live weather from Open-Meteo with automated bilingual (**English & Kannada**) agricultural advisories for harvesting, spraying, and grain drying.
- **Clean Service-Oriented Architecture**: Strict decoupling between FastAPI HTTP routers, core business logic services, and static datasets.
- **In-Memory Caching**: 1-hour TTL caching across third-party API queries to avoid rate-limiting and maximize throughput.

---

## 🏗 Architecture & Project Structure

The project follows a clean, decoupled **Router-Service-Data** pattern:

```text
raitabazzar-backend/
├── app/
│   ├── config.py                 # Pydantic Settings & environment variables
│   ├── main.py                   # FastAPI app initialization, middleware, & router mounts
│   ├── data/
│   │   ├── crop_master.py        # Master crop dictionary (29 crops) & vernacular synonyms map
│   │   └── data.py               # Karnataka APMC benchmarks & district GPS coordinates
│   ├── routers/                  # HTTP Layer (Validation, status codes, OpenAPI metadata)
│   │   ├── __init__.py
│   │   ├── crops.py              # /api/v1/crops routes (search, master)
│   │   ├── mandi.py              # /api/v1/mandi-rates route
│   │   └── weather.py            # /api/v1/weather route
│   └── services/                 # Business Logic Layer (Data processing, NLP, external APIs)
│       ├── __init__.py
│       ├── crop_services.py      # Vernacular search, fuzzy matching, benchmark resolution
│       ├── mandi_services.py     # data.gov.in fetcher, benchmark merger, rate caching
│       └── weather_services.py   # Open-Meteo weather client, advisory engine, caching
├── tests/                        # Automated unit & integration tests
│   ├── test_crop_services.py
│   ├── test_crops.py
│   ├── test_mandi_services.py
│   └── test_weather.py
├── .env.example                  # Template environment variables
├── API_ENDPOINTS_GUIDE.md        # Comprehensive data contracts & Flutter integration guide
├── requirements.txt              # Production and dev dependencies
└── README.md
```

---

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Server**: [Uvicorn](https://www.uvicorn.org/) (ASGI server)
- **Data Validation & Settings**: [Pydantic v2](https://docs.pydantic.dev/) & [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **HTTP Client**: [HTTPX](https://www.python-httpx.org/) (async requests with connection pooling)
- **External Data Providers**:
  - [data.gov.in](https://data.gov.in/) (AGMARKNET Daily Mandi Prices)
  - [Open-Meteo](https://open-meteo.com/) (Free hyper-local meteorological forecasts)

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** (Python 3.11 or 3.12/3.13 recommended)
- `pip` or virtualenv

### Installation

1. **Clone the repository and navigate into the project directory:**
   ```bash
   git clone https://github.com/your-username/raitabazzar-backend.git
   cd raitabazzar-backend
   ```

2. **Create and activate a virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and provide your `data.gov.in` API key:

```env
DATAGOV_API_KEY=your_datagov_api_key_here
MANDI_RESOURCE_ID=9ef84268-d588-465a-a308-a864a43d0070
CACHE_TTL_SECONDS=3600
```

> **Note:** A free API key can be obtained by creating an account at [data.gov.in](https://data.gov.in/). If no key is provided, the backend seamlessly serves verified Karnataka APMC benchmark fallback data.

### Running the Server

Start the development server with hot-reload enabled:

```bash
uvicorn app.main:app --reload --port 8000
```

- **API Base URL**: `http://localhost:8000`
- **Interactive Swagger Documentation**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

### Running with Docker

Build and run using Docker CLI:

```bash
docker build -t raitabazzar-backend .
docker run -p 8000:8000 --env-file .env raitabazzar-backend
```

Or using Docker Compose:

```bash
docker compose up --build
```

---

## 📡 API Reference

### 1. Health Check

Verifies server status and uptime.

- **Endpoint**: `GET /api/v1/health`
- **Response (`200 OK`)**:
  ```json
  {
    "status": "ok"
  }
  ```

---

### 2. Live Mandi Rates

Fetches AGMARKNET mandi rates for Karnataka markets with optional district and commodity filters.

- **Endpoint**: `GET /api/v1/mandi-rates`
- **Query Parameters**:
  | Parameter | Type | Required | Description | Example |
  | :--- | :--- | :--- | :--- | :--- |
  | `district` | `string` | No | District filter | `Mandya`, `Koppal`, `Bangalore` |
  | `commodity` | `string` | No | Crop name filter | `Tomato`, `Onion` |
  | `refresh` | `boolean` | No | Force bypass cache | `true`, `false` (default) |
- **Example Request**:
  ```bash
  curl "http://localhost:8000/api/v1/mandi-rates?district=Koppal"
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "count": 5,
    "source": "AGMARKNET (data.gov.in)",
    "data": [
      {
        "id": "gov_koppal_maize_0",
        "commodity": "Maize",
        "variety": "Hybrid/Local",
        "market": "Kustagi APMC",
        "district": "Koppal",
        "state": "Karnataka",
        "min_price": 30.0,
        "max_price": 33.0,
        "modal_price": 31.1,
        "unit": "Kg",
        "trend": "stable",
        "trend_pct": 0.0,
        "arrival_date": "15/11/2026 (Live)",
        "is_live": true
      }
    ]
  }
  ```

---

### 3. Vernacular Crop Search & NLP

Translates search input across Kannada, Hindi, English, and Kanglish into standardized crop metadata with APMC benchmark pricing.

- **Endpoint**: `GET /api/v1/crops/search`
- **Query Parameters**:
  | Parameter | Type | Required | Description | Example |
  | :--- | :--- | :--- | :--- | :--- |
  | `q` | `string` | **Yes** | Search query in any script | `ಈರುಳ್ಳಿ`, `eerulli`, `pyaz`, `tomato` |
  | `district` | `string` | No | Preferred benchmark district | `Mandya`, `Bangalore` |
- **Example Request**:
  ```bash
  curl "http://localhost:8000/api/v1/crops/search?q=%E0%B3%88%E0%B2%B0%E0%B3%81%E0%B2%B3%E0%B3%8D%E0%B2%B3%E0%B2%BF&district=Mandya"
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "query": "ಈರುಳ್ಳಿ",
    "matched_crop": {
      "standard_name": "Onion",
      "kannada_name": "ಈರುಳ್ಳಿ",
      "hindi_name": "प्याज",
      "category": "Vegetables",
      "unit": "Kg",
      "synonyms_matched": [
        "ಈರುಳ್ಳಿ",
        "eerulli",
        "onion"
      ],
      "benchmark": {
        "district": "Bangalore",
        "market": "Yeshwanthpur APMC",
        "modal_price": 34.0,
        "min_price": 28.0,
        "max_price": 38.0,
        "unit": "Kg"
      }
    }
  }
  ```
- **Error Response (`404 Not Found`)**:
  ```json
  {
    "success": false,
    "query": "unknown_item",
    "matched_crop": null,
    "message": "No matching Karnataka crop found for 'unknown_item'"
  }
  ```

---

### 4. Master Crops Catalog

Returns the master list of 29 supported Karnataka crops with bilingual labels, categories, and icons for UI dropdowns.

- **Endpoint**: `GET /api/v1/crops/master`
- **Query Parameters**:
  | Parameter | Type | Required | Description | Example |
  | :--- | :--- | :--- | :--- | :--- |
  | `category` | `string` | No | Category filter | `Vegetables`, `Grains`, `Fruits`, `Pulses`, `Commercial`, `Spices` |
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "total": 29,
    "crops": [
      {
        "id": "tomato",
        "name_en": "Tomato",
        "name_kn": "ಟೊಮೇಟೊ",
        "name_hi": "टमाटर",
        "category": "Vegetables",
        "default_unit": "Kg",
        "icon": "🍅"
      },
      {
        "id": "ragi",
        "name_en": "Ragi (Finger Millet)",
        "name_kn": "ರಾಗಿ",
        "name_hi": "रागी",
        "category": "Grains",
        "default_unit": "Quintal",
        "icon": "🌾"
      }
    ]
  }
  ```

---

### 5. Agricultural Weather Service

Fetches hyper-local meteorological conditions from Open-Meteo with automated bilingual farming advisories.

- **Endpoint**: `GET /api/v1/weather`
- **Query Parameters**:
  | Parameter | Type | Required | Description | Example |
  | :--- | :--- | :--- | :--- | :--- |
  | `district` | `string` | No | Karnataka district | `Mandya`, `Kolar`, `Bangalore` (default: `Mandya`) |
  | `lat` | `float` | No | Custom latitude | `12.52` |
  | `lon` | `float` | No | Custom longitude | `76.89` |
  | `refresh` | `boolean` | No | Force refresh cache | `true`, `false` (default) |
- **Example Request**:
  ```bash
  curl "http://localhost:8000/api/v1/weather?district=Mandya"
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "district": "Mandya",
    "temperature_c": 28.5,
    "humidity_pct": 62,
    "wind_speed_kmh": 11.2,
    "rain_chance_pct": 15,
    "condition": "Partly Cloudy",
    "advisory_en": "Dry and favorable weather. Ideal for harvesting, drying grains, and spraying.",
    "advisory_kn": "ಒಣ ಹವೆ ಮತ್ತು ಅನುಕೂಲಕರ ವಾತಾವರಣ. ಕಟಾವು, ಧಾನ್ಯ ಒಣಗಿಸಲು ಮತ್ತು ಸಿಂಪಡಣೆಗೆ ಸೂಕ್ತವಾಗಿದೆ.",
    "source": "Open-Meteo (Live)",
    "is_live": true
  }
  ```

---

## 🧪 Running Automated Tests

The backend includes a comprehensive suite of unit and integration tests using Python's built-in `unittest` runner and FastAPI's `TestClient`:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

### Test Coverage Highlights:
- **`test_crops.py`**: Router tests verifying Kannada script, Hindi, Kanglish transliterations, APMC district benchmarks, and 404 responses.
- **`test_crop_services.py`**: Unit tests for the search NLP and master crop service functions.
- **`test_mandi_services.py`**: AGMARKNET live feeds, district filtering, and APMC baseline fallbacks.
- **`test_weather.py`**: Open-Meteo data parsing, rain probability advisory shifts, caching, and offline fallbacks.

---

## 🗺 Roadmap

Refer to [API_ENDPOINTS_GUIDE.md](file:///D:/Learning/raitabazzar-backend/API_ENDPOINTS_GUIDE.md) for full implementation details:
- [ ] **Indian Phone Authentication (`/api/v1/auth`)**: Fast2SMS / MSG91 OTP generation and JWT authentication.
- [ ] **Farmer & Buyer Profiles (`/api/v1/users`)**: Profile management with FRUITS ID and APMC licenses.
- [ ] **Marketplace Produce Listings (`/api/v1/listings`)**: Farmer harvest publishing and Cloudinary image attachments.
- [ ] **Direct Negotiations & Offers (`/api/v1/offers`)**: Buyer counter-offers and farmer acceptance workflows.
- [ ] **Instant Alerts (`/api/v1/notifications`)**: Automated WhatsApp & SMS deal notifications.

---

## 📄 License

This project is licensed under the MIT License.
