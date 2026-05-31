# AlgoVista AI - Adaptive Algorithm Recommendation System

<div align="center">

![AlgoVista AI](https://img.shields.io/badge/Algorithm-Recommendation-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![React](https://img.shields.io/badge/Frontend-React-61DAFB)
![TypeScript](https://img.shields.io/badge/Language-TypeScript%20%2F%20Python-3178C6)
![License](https://img.shields.io/badge/License-MIT-green)

An intelligent system that recommends optimal algorithms based on problem characteristics using both rule-based and machine learning approaches.

[Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [API Documentation](#-api-documentation) • [Usage](#-usage)

</div>

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [🎯 Features](#-features)
- [🏗️ Architecture](#-architecture)
- [📦 Technology Stack](#-technology-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Installation & Setup](#-installation--setup)
- [📚 API Documentation](#-api-documentation)
- [🧮 Supported Algorithms](#-supported-algorithms)
- [🤖 Decision System](#-decision-system)
- [📊 User Interface](#-user-interface)
- [🔧 Configuration](#-configuration)
- [📈 Performance Benchmarking](#-performance-benchmarking)
- [🎨 Diagrams & Flowcharts](#-diagrams--flowcharts)
- [📖 Usage Examples](#-usage-examples)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)

---

## Project Overview

**AlgoVista AI** is an adaptive algorithm recommendation system that uses both **rule-based logic** and **machine learning** to recommend the most optimal algorithms for various computational problems. The system analyzes problem characteristics such as data size, memory constraints, and problem type to provide tailored recommendations.

### Key Capabilities:
- **Smart Recommendations**: Hybrid system combining rules-engine with ML models
- **Performance Benchmarking**: Real-time execution time measurements for algorithms
- **Visual Analytics**: Interactive charts showing complexity analysis and execution times
- **Multi-Algorithm Support**: Supports various sorting, searching, and graph algorithms
- **PDF Export**: Generate detailed algorithm comparison reports
- **Continuous Learning**: ML model training and retraining capabilities

---

## 🎯 Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Sorting Algorithms** | Insertion Sort, Merge Sort, Heap Sort, Quick Sort | ✅ Active |
| **Searching Algorithms** | Linear Search, Binary Search | ✅ Active |
| **Algorithm Benchmarking** | Real-time performance measurement | ✅ Active |
| **Complexity Analysis** | Visual Big-O complexity charts | ✅ Active |
| **Rule-Based Recommendation** | Deterministic rules for algorithm selection | ✅ Active |
| **ML-Based Recommendation** | scikit-learn RandomForest predictions | ✅ Active |
| **Ensemble Decision Making** | Hybrid rules + ML approach | ✅ Active |
| **PDF Export** | Generate detailed algorithm reports | ✅ Active |
| **MongoDB Integration** | Persistent storage and caching | ✅ Active |
| **Interactive UI** | React + TypeScript dashboard | ✅ Active |
| **CORS Enabled** | Frontend-backend communication | ✅ Active |
| **Health Check Endpoint** | System monitoring | ✅ Active |

---

## 🏗️ Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AlgoVista AI System                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  FRONTEND (React + TypeScript)        BACKEND (FastAPI)      │
│  ┌──────────────────────────┐         ┌────────────────────┐│
│  │  - Header                │         │  API Routers       ││
│  │  - InputPanel            │◄───────►│  - Benchmark       ││
│  │  - OutputPanel           │         │  - Recommend       ││
│  │  - VisualizationSection   │         │  - Train ML        ││
│  │  - ComplexityChart       │         │  - Export          ││
│  │  - ExecutionTimeChart    │         └────────────────────┘│
│  └──────────────────────────┘                │               │
│          │                                   │               │
│          │                                   ▼               │
│          │                            ┌──────────────────┐   │
│          │                            │ Decision Engine  │   │
│          │                            ├──────────────────┤   │
│          │                            │ - Rules Engine   │   │
│          │                            │ - ML Engine      │   │
│          │                            └──────────────────┘   │
│          │                                   │               │
│          │                                   ▼               │
│          │                            ┌──────────────────┐   │
│          │                            │ Algorithm Impl.  │   │
│          │                            ├──────────────────┤   │
│          │                            │ - Sorting        │   │
│          │                            │ - Searching      │   │
│          │                            └──────────────────┘   │
│          │                                   │               │
│          │                                   ▼               │
│          │                            ┌──────────────────┐   │
│          └───────────────────────────►│  Database        │   │
│                                       │  (MongoDB)       │   │
│                                       └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### System Data Flow

```
User Input (Problem Characteristics)
          │
          ▼
┌─────────────────────────────────┐
│   Validate & Parse Request      │
│   - Problem Type                │
│   - Input Size                  │
│   - Memory Constraints          │
│   - Other Parameters            │
└──────────────┬──────────────────┘
               │
          ┌────┴─────┐
          │           │
          ▼           ▼
    ┌──────────┐  ┌────────────┐
    │Rules     │  │ML Model    │
    │Engine    │  │Engine      │
    └────┬─────┘  └─────┬──────┘
         │              │
         │   ┌─────────┐│
         │   │Confidence│
         │   │Check   ││
         │   └────┬────┘│
         │        │     │
         ▼        ▼     │
    ┌─────────────────────────────┐
    │ Final Recommendation         │
    │ - Algorithm Name            │
    │ - Time Complexity           │
    │ - Space Complexity          │
    │ - Reasoning                 │
    │ - Alternatives              │
    └──────────────┬──────────────┘
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
    ┌──────────┐      ┌──────────┐
    │Benchmark │      │Export    │
    │Data      │      │Report    │
    └──────────┘      └──────────┘
```

---

## 📦 Technology Stack

### Backend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | FastAPI | 0.115.0 | REST API development |
| **Server** | Uvicorn | 0.30.6 | ASGI server |
| **Language** | Python | 3.9+ | Backend logic |
| **Configuration** | python-dotenv | 1.0.1 | Environment management |
| **Data Validation** | Pydantic | 2.8.2 | Request/response schemas |
| **ML Framework** | scikit-learn | 1.5.1 | Machine learning models |
| **Numerical** | NumPy | 2.0.1 | Numerical computations |
| **Model Serialization** | joblib | 1.4.2 | ML model persistence |
| **PDF Generation** | reportlab | 4.2.2 | Report generation |
| **Database** | MongoDB | - | Data persistence |

### Frontend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | React | 19.2.4 | UI component library |
| **Language** | TypeScript | 6.0.2 | Type-safe code |
| **Build Tool** | Vite | 8.0.4 | Fast build bundler |
| **HTTP Client** | Axios | 1.14.0 | API communication |
| **Charting** | Chart.js | 4.5.1 | Data visualization |
| **Chart Wrapper** | react-chartjs-2 | 5.3.1 | React integration |
| **Animation** | Framer Motion | 12.38.0 | Smooth animations |
| **DOM Renderer** | React DOM | 19.2.4 | DOM manipulation |

---

## 📁 Project Structure

```
algo-vista_ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                          # FastAPI application factory
│   │   ├── schemas.py                       # Pydantic models & validation
│   │   ├── algorithms/
│   │   │   ├── __init__.py
│   │   │   ├── sorting.py                   # Sorting algorithms
│   │   │   └── searching.py                 # Searching algorithms
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── benchmark.py                 # Performance benchmarking
│   │   │   ├── export.py                    # PDF report generation
│   │   │   ├── recommend.py                 # Recommendation router
│   │   │   └── train_ml.py                  # ML model training
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py                    # Configuration management
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   └── mongo.py                     # MongoDB integration
│   │   ├── decision/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py                    # Decision orchestration
│   │   │   ├── ml_engine.py                 # ML recommendations
│   │   │   └── rules_engine.py              # Rule-based recommendations
│   │   └── ml/
│   │       └── __init__.py
│   ├── backend/
│   │   └── models/
│   │       └── model.joblib                 # Trained ML model
│   ├── models/                              # Model storage
│   ├── scripts/                             # Utility scripts
│   └── requirements.txt                     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── main.ts                          # Application entry point
│   │   ├── App.tsx                          # Root component
│   │   ├── counter.ts                       # Demo component logic
│   │   ├── style.css                        # Global styles
│   │   ├── aars.css                         # Additional styles
│   │   ├── types.ts                         # TypeScript type definitions
│   │   ├── api/
│   │   │   └── client.ts                    # Axios API client
│   │   ├── components/
│   │   │   ├── Header.tsx                   # Application header
│   │   │   ├── InputPanel.tsx               # User input form
│   │   │   ├── OutputPanel.tsx              # Results display
│   │   │   ├── ComparisonSection.tsx        # Algorithm comparison
│   │   │   └── visualization/
│   │   │       ├── ComplexityChart.tsx      # Big-O complexity chart
│   │   │       ├── ExecutionTimeChart.tsx   # Performance chart
│   │   │       └── VisualizationSection.tsx # Chart container
│   │   └── assets/                          # Images, fonts, etc.
│   ├── public/                              # Static files
│   ├── package.json                         # NPM dependencies
│   ├── package-lock.json                    # Dependency lock file
│   ├── tsconfig.json                        # TypeScript configuration
│   ├── vite.config.ts                       # Vite build configuration
│   └── index.html                           # HTML entry point
│
├── package-lock.json                        # Root lock file
└── README.md                                # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Python**: 3.9 or higher
- **Node.js**: 18.0.0 or higher
- **npm**: 9.0.0 or higher
- **MongoDB**: 5.0 or higher (local or cloud)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**:
   Create a `.env` file in the backend directory:
   ```env
   MONGODB_URI=mongodb://localhost:27017
   DB_NAME=algovia
   ML_ENABLED=true
   ML_AUTO_TRAIN=true
   ML_CONFIDENCE_THRESHOLD=0.75
   ML_MODEL_PATH=./backend/models/model.joblib
   MAX_BENCHMARK_INPUT_SIZE=50000
   LOG_LEVEL=INFO
   ```

6. **Start FastAPI server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   - Interactive API docs: `http://localhost:8000/docs`
   - ReDoc documentation: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

   The UI will be available at `http://localhost:5173`

4. **Build for production**:
   ```bash
   npm run build
   ```

5. **Preview production build**:
   ```bash
   npm run preview
   ```

### Full Stack Setup (Quick Start)

```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "ok"
}
```

---

### Algorithm Recommendation

**Endpoint**: `POST /recommend`

**Request Body**:
```json
{
  "problem_type": "sorting",
  "input_size": 10000,
  "nearly_sorted": false,
  "memory": "medium",
  "recursive_allowed": true,
  "graph_type": null
}
```

**Request Parameters**:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `problem_type` | string | ✅ | Type of problem | `"sorting"`, `"searching"`, `"graph"`, `"dp"` |
| `input_size` | integer | ✅ | Size of input data (1-500000) | `10000` |
| `nearly_sorted` | boolean | ❌ | Is data nearly sorted? | `false` |
| `memory` | string | ✅ | Memory constraint level | `"low"`, `"medium"`, `"high"` |
| `recursive_allowed` | boolean | ❌ | Can use recursive algorithms? | `true` |
| `graph_type` | string | ❌ | Graph type (for graph problems) | `"dense"`, `"sparse"` |

**Response**:
```json
{
  "recommended_algorithm": "Merge Sort",
  "time_complexity": "O(n log n)",
  "space_complexity": "O(n)",
  "reason": "Merge Sort offers consistent O(n log n) performance for large unsorted datasets with adequate memory.",
  "alternatives": [
    {
      "algorithm": "Heap Sort",
      "time_complexity": "O(n log n)",
      "space_complexity": "O(1)",
      "short_reason": "Better space efficiency than Merge Sort"
    }
  ],
  "decision_layer": "rules",
  "model_used": false,
  "ml_confidence": null,
  "complexity_chart": [
    {
      "algorithm": "Merge Sort",
      "time_complexity": "O(n log n)",
      "growth_score": 3.45
    }
  ],
  "comparison_algorithms": [
    {
      "name": "Merge Sort",
      "time": "O(n log n)",
      "space": "O(n)",
      "stability": "yes",
      "best_case": "O(n log n)",
      "worst_case": "O(n log n)",
      "use_case": "Large datasets, stable sort needed",
      "rank": "best"
    }
  ]
}
```

**Response Parameters**:

| Field | Type | Description |
|-------|------|-------------|
| `recommended_algorithm` | string | Name of recommended algorithm |
| `time_complexity` | string | Time complexity Big-O notation |
| `space_complexity` | string | Space complexity Big-O notation |
| `reason` | string | Explanation for recommendation |
| `alternatives` | array | List of alternative algorithms |
| `decision_layer` | string | `"rules"`, `"ml"`, or `"ensemble"` |
| `model_used` | boolean | Was ML model used? |
| `ml_confidence` | float | ML model confidence (0-1) |
| `complexity_chart` | array | Chart data for visualization |
| `comparison_algorithms` | array | Detailed algorithm comparisons |

---

### Performance Benchmarking

**Endpoint**: `POST /benchmark`

**Request Body**:
```json
{
  "problem_type": "sorting",
  "input_size": 5000,
  "nearly_sorted": false,
  "algorithms": ["Merge Sort", "Heap Sort", "Quick Sort"],
  "memory": "medium",
  "recursive_allowed": true
}
```

**Response**:
```json
{
  "timings": [
    {
      "algorithm": "Merge Sort",
      "points": [
        {"x": 1250, "y": 0.0012},
        {"x": 2500, "y": 0.0035},
        {"x": 5000, "y": 0.0089}
      ],
      "time_complexity": "O(n log n)",
      "space_complexity": "O(n)"
    }
  ]
}
```

---

### ML Model Training

**Endpoint**: `POST /train_ml`

**Request Body**:
```json
{
  "n_samples": 5000,
  "force": false
}
```

**Response**:
```json
{
  "success": true,
  "message": "Model trained successfully",
  "model_path": "./backend/models/model.joblib",
  "samples_used": 5000,
  "timestamp": "2024-04-08T15:30:00.000Z"
}
```

---

### PDF Export

**Endpoint**: `POST /export`

**Request Body**:
```json
{
  "recommendation": {
    "recommended_algorithm": "Merge Sort",
    "time_complexity": "O(n log n)",
    "space_complexity": "O(n)",
    "reason": "...",
    "alternatives": [],
    "comparison_algorithms": []
  },
  "problem_details": {
    "problem_type": "sorting",
    "input_size": 10000,
    "memory": "medium"
  }
}
```

**Response**: PDF file binary stream

---

## 🧮 Supported Algorithms

### Sorting Algorithms

| Algorithm | Time Complexity | Space Complexity | Stable | Best For | Worst Case |
|-----------|-----------------|------------------|--------|----------|-----------|
| **Insertion Sort** | O(n²) | O(1) | Yes | Nearly sorted data, small arrays | O(n²) |
| **Merge Sort** | O(n log n) | O(n) | Yes | Large datasets, stable sort needed | O(n log n) |
| **Heap Sort** | O(n log n) | O(1) | No | Space-constrained environments | O(n log n) |
| **Quick Sort** | O(n log n) | O(log n) | No | Average case performance | O(n²) worst |

### Searching Algorithms

| Algorithm | Time Complexity | Space Complexity | Used When | Example |
|-----------|-----------------|------------------|-----------|---------|
| **Linear Search** | O(n) | O(1) | Unsorted data, small arrays | [3, 1, 4, 1, 5, 9] → find 5 |
| **Binary Search** | O(log n) | O(1) | Sorted data, large datasets | [1, 2, 5, 7, 10, 15] → find 7 |

### Complexity Reference Table

| Notation | Meaning | Growth Rate | Example |
|----------|---------|-------------|---------|
| **O(1)** | Constant | No growth | Array index access |
| **O(log n)** | Logarithmic | Very slow growth | Binary search |
| **O(n)** | Linear | Proportional | Simple loop |
| **O(n log n)** | Linearithmic | Efficient | Merge sort, Quick sort |
| **O(n²)** | Quadratic | Fast growth | Nested loops |
| **O(n³)** | Cubic | Faster growth | Triple nested loops |
| **O(2ⁿ)** | Exponential | Very fast growth | Recursive Fibonacci |

---

## 🤖 Decision System

### Architecture Overview

The system uses a **two-layer decision-making approach**:

1. **Rules Engine** (Always Active)
2. **ML Engine** (Optional, with confidence threshold)

#### Rules Engine Logic

```
Input Request
    │
    ▼
Parse Problem Type
    │
    ├─► SORTING ──────► Check nearly_sorted flag
    │                      ├─ Yes ──► Insertion Sort
    │                      └─ No ──► Check memory constraint
    │                                  ├─ Low ──► Heap Sort
    │                                  └─ Medium/High ──► Merge Sort
    │
    ├─► SEARCHING ────► Check if sorted
    │                      ├─ Yes ──► Binary Search
    │                      └─ No ──► Linear Search
    │
    ├─► GRAPH ────────► Check graph_type
    │                      ├─ Dense ──► DFS/BFS
    │                      └─ Sparse ──► Dijkstra
    │
    └─► OTHER ────────► Default recommendation
            │
            ▼
        Recommendation
```

#### ML Engine Logic

```
Input Request
    │
    ▼
Extract Features
┌─────────────────────────┐
│ - problem_type          │
│ - input_size_log        │
│ - memory                │
│ - recursive_allowed     │
│ - nearly_sorted         │
│ - graph_type            │
└─────────────────────────┘
    │
    ▼
    Check ML Model Available
    │
    ├─► Model Exists ─► Load Model
    │                      │
    │                      ▼
    │                  Vectorize Features
    │                      │
    │                      ▼
    │                  Predict Algorithm
    │                      │
    │                      ▼
    │                  Extract Confidence
    │                      │
    │                      ▼
    │                  Check Threshold
    │                      ├─ ≥ Threshold ──► Use ML Recommendation
    │                      └─ < Threshold ──► Fall back to Rules
    │
    └─► Model Missing ─► Auto-train?
                            ├─ Yes ──► Train & Use
                            └─ No ──► Use Rules
```

#### Ensemble Decision Making

```
Rules Recommendation      ML Recommendation
        │                        │
        │          ┌─────────────┘
        │          │
        │          ▼
        │      Confidence ≥ Threshold?
        │          │
        │          ├─ Yes: Override with ML
        │          └─ No: Keep Rules
        │
        └──────────────┬──────────────┘
                       │
                       ▼
            Final Recommendation
         (with decision_layer info)
```

### Decision Layer Types

| Layer | Source | Confidence | Use Case |
|-------|--------|-----------|----------|
| **rules** | Rule Engine | 100% | Default, fallback |
| **ml** | ML Model | Variable | When confidence high |
| **ensemble** | ML overriding Rules | ML provided | Hybrid approach |

---

## 📊 User Interface

### UI Components Hierarchy

```
App.tsx
├── Header
│   ├── Title
│   ├── Logo
│   └── Navigation
│
├── InputPanel
│   ├── Problem Type Selector
│   ├── Input Size Slider
│   ├── Memory Level Toggle
│   ├── Nearly Sorted Checkbox
│   ├── Recursive Allowed Checkbox
│   ├── Graph Type Selector (conditional)
│   └── Submit Button
│
├── OutputPanel
│   ├── Recommended Algorithm Display
│   │   ├── Algorithm Name
│   │   ├── Complexities
│   │   └── Reasoning
│   │
│   ├── Alternative Algorithms
│   │
│   └── Action Buttons
│       ├── Benchmark
│       ├── Explain
│       └── Export PDF
│
├── VisualizationSection
│   ├── ComplexityChart
│   │   └── Big-O visualization
│   │
│   └── ExecutionTimeChart
│       └── Real-time benchmark data
│
└── ComparisonSection
    └── Algorithm Comparison Table
```

### Key UI Features

| Feature | Component | Functionality |
|---------|-----------|---------------|
| **Problem Selection** | InputPanel | Dropdown for problem type selection |
| **Size Input** | InputPanel | Slider for input size (1-500,000) |
| **Constraints** | InputPanel | Toggles for memory, recursion, etc. |
| **Recommendation** | OutputPanel | Display of recommended algorithm |
| **Complexity Chart** | ComplexityChart | Visual Big-O comparison |
| **Performance Chart** | ExecutionTimeChart | Real-time execution time graph |
| **Comparison Table** | ComparisonSection | Side-by-side algorithm details |
| **Export** | OutputPanel | PDF report generation |

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database Configuration
MONGODB_URI=mongodb://localhost:27017
DB_NAME=algovia

# ML Configuration
ML_ENABLED=true
ML_AUTO_TRAIN=true
ML_CONFIDENCE_THRESHOLD=0.75
ML_MODEL_PATH=./backend/models/model.joblib

# API Configuration
MAX_BENCHMARK_INPUT_SIZE=50000
BENCHMARK_TIMEOUT_SECONDS=30

# Logging
LOG_LEVEL=INFO

# Server
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

### Configuration Loading

The system uses Pydantic `BaseSettings` for configuration management. See [core/config.py](backend/app/core/config.py) for implementation details.

---

## 📈 Performance Benchmarking

### Benchmarking Process

1. **Input Validation**: Ensures input size is within limits
2. **Test Point Generation**: Creates 3-5 evenly spaced test sizes
3. **Algorithm Execution**: Runs algorithm with different input sizes
4. **Time Measurement**: Records execution time to millisecond precision
5. **Data Collection**: Aggregates results for visualization

### Benchmark Request Example

```python
# Request
POST /benchmark
{
    "problem_type": "sorting",
    "input_size": 10000,
    "nearly_sorted": false,
    "algorithms": ["Merge Sort", "Quick Sort", "Heap Sort"],
    "memory": "medium",
    "recursive_allowed": true
}

# Response
{
    "timings": [
        {
            "algorithm": "Merge Sort",
            "points": [
                {"x": 2500, "y": 0.00234},
                {"x": 5000, "y": 0.00589},
                {"x": 10000, "y": 0.01342}
            ],
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)"
        },
        ...
    ]
}
```

### Benchmark Test Sizes

```python
# For input_size = 10000:
# Generated test points:
- min(1000, 10000) = 2500 (1/4)
- min(2000, 10000) = 5000 (1/2)
- min(4000, 10000) = 10000 (full)
```

---

## 🎨 Diagrams & Flowcharts

### Application Request Flow

```
User Input (Web Browser)
    │
    ▼
React Component (InputPanel)
    │ Validates input
    ▼
Axios HTTP Request
    │ POST /recommend
    │ Content-Type: application/json
    ▼
FastAPI Router
    │ Validates with Pydantic
    ▼
Decision Engine
    │
    ├─► Rules Engine ──┐
    │                  │
    └─► ML Engine ────►│
                       │
                       ▼
                Generate Response
                       │
                       ▼
                JSON Response
                       │
                       ▼
                Network Response
                       │
                       ▼
            React State Update
                       │
                       ▼
            UI Components Re-render
                       │
                       ▼
        Display Results and Charts
```

### Algorithm Selection Decision Tree

```
START
  │
  ▼
Is problem_type = SORTING?
  │
  ├─ NO ──► Is problem_type = SEARCHING?
  │          │
  │          ├─ NO ──► Is problem_type = GRAPH?
  │          │          │
  │          │          ├─ NO ──► Is problem_type = DP?
  │          │          │          │
  │          │          │          └─ NO ──► Use Default Recommendation
  │          │          │                       │
  │          │          │                       ▼
  │          │          │                      END
  │          │          │
  │          │          ├─ YES ──► Check graph_type
  │          │          │           ├─ dense ──► Use DFS/BFS
  │          │          │           └─ sparse ──► Use Dijkstra
  │          │          │                       │
  │          │          │                       ▼
  │          │          │                      END
  │          │
  │          ├─ YES ──► Is array sorted?
  │                      ├─ YES ──► Binary Search
  │                      └─ NO ──► Linear Search
  │                                │
  │                                ▼
  │                               END
  │
  ├─ YES ──► Is nearly_sorted = TRUE?
              ├─ YES ──► Use Insertion Sort
              │           │
              │           ▼
              │          END
              │
              └─ NO ──► Check memory level
                        ├─ low ──► Use Heap Sort
                        ├─ medium ──► Use Merge Sort
                        └─ high ──► Use Quick Sort / Merge Sort
                                    │
                                    ▼
                                   END
```

### Data Flow Diagram (API)

```
┌──────────────────────────────────────────────────────────────┐
│                     REQUEST LAYER                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  POST /recommend                                     │   │
│  │  {problem_type, input_size, memory, ...}            │   │
│  └──────────────┬───────────────────────────────────────┘   │
└─────────────────┼─────────────────────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────────────────────┐
│                VALIDATION LAYER                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Pydantic Validation                                │   │
│  │  - Type checking                                    │   │
│  │  - Range validation                                │   │
│  │  - Required fields                                 │   │
│  └──────────────┬───────────────────────────────────────┘   │
└─────────────────┼─────────────────────────────────────────────┘
                  │
      ┌───────────┴───────────┐
      │                       │
      ▼                       ▼
┌────────────────┐   ┌─────────────────┐
│ RULES ENGINE   │   │ ML ENGINE       │
│                │   │                 │
│ Deterministic  │   │ Model-based     │
│ Rule Set       │   │ Prediction      │
│ (100% match)   │   │ (confidence%)   │
└────────┬───────┘   └────────┬────────┘
         │                    │
         └────────┬───────────┘
                  │
                  ▼
┌──────────────────────────────────────────────────────────────┐
│                RESPONSE LAYER                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  RecommendationResponse                            │   │
│  │  - algorithm name                                  │   │
│  │  - complexities                                    │   │
│  │  - alternatives                                   │   │
│  │  - metadata                                        │   │
│  └──────────────┬───────────────────────────────────────┘   │
└─────────────────┼─────────────────────────────────────────────┘
                  │
                  ▼
         JSON Response (HTTP 200)
```

### Component Communication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      App.tsx                                 │
│  ┌──────────────┐         ┌──────────────────┐              │
│  │  InputPanel  │────────►│  API Client      │              │
│  │              │  data   │                  │              │
│  └──────────────┘         └────────┬─────────┘              │
│                                    │                        │
│                           HTTP POST│/recommend              │
│                                    │                        │
│                                    ▼                        │
│                            Backend API                      │
│                                    │                        │
│                           JSON Response                     │
│                                    │                        │
│  ┌──────────────┐         ┌────────▼─────────┐              │
│  │ OutputPanel  │◄────────│  API Client      │              │
│  │              │  data   │                  │              │
│  └──────────────┘         └──────────────────┘              │
│         │                                                    │
│         ├──────────────────┬──────────────────┐              │
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│   ┌──────────┐    ┌──────────────┐    ┌──────────────┐     │
│   │ Complexity│    │ExecutionTime │    │Comparison    │     │
│   │Chart     │    │Chart         │    │Section       │     │
│   └──────────┘    └──────────────┘    └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📖 Usage Examples

### Example 1: Sorting Large Unsorted Dataset

**Scenario**: User has 100,000 integers to sort, with medium memory availability

**Request**:
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "problem_type": "sorting",
    "input_size": 100000,
    "nearly_sorted": false,
    "memory": "medium",
    "recursive_allowed": true
  }'
```

**Response**:
```json
{
  "recommended_algorithm": "Merge Sort",
  "time_complexity": "O(n log n)",
  "space_complexity": "O(n)",
  "reason": "Merge Sort provides consistent O(n log n) performance for large unsorted datasets with guaranteed stability.",
  "decision_layer": "rules",
  "alternatives": [
    {
      "algorithm": "Quick Sort",
      "time_complexity": "O(n log n)",
      "space_complexity": "O(log n)",
      "short_reason": "Better space efficiency, but less stable"
    }
  ]
}
```

### Example 2: Finding Element in Sorted Array

**Scenario**: User has 50,000 sorted items and needs to find a specific element

**Request**:
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "problem_type": "searching",
    "input_size": 50000,
    "nearly_sorted": true,
    "memory": "low",
    "recursive_allowed": false
  }'
```

**Response**:
```json
{
  "recommended_algorithm": "Binary Search",
  "time_complexity": "O(log n)",
  "space_complexity": "O(1)",
  "reason": "Binary Search is optimal for sorted arrays, achieving O(log n) performance with minimal space overhead.",
  "decision_layer": "rules"
}
```

### Example 3: Nearly Sorted Data with Space Constraints

**Scenario**: User has 10,000 nearly sorted items with strict memory constraints

**Request**:
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "problem_type": "sorting",
    "input_size": 10000,
    "nearly_sorted": true,
    "memory": "low",
    "recursive_allowed": true
  }'
```

**Response**:
```json
{
  "recommended_algorithm": "Insertion Sort",
  "time_complexity": "O(n)",
  "space_complexity": "O(1)",
  "reason": "Insertion Sort with nearly sorted data has near-linear performance O(n) while using minimal space O(1).",
  "decision_layer": "rules",
  "alternatives": [
    {
      "algorithm": "Heap Sort",
      "time_complexity": "O(n log n)",
      "space_complexity": "O(1)",
      "short_reason": "Also space-efficient, better for unsorted data"
    }
  ]
}
```

### Example 4: Performance Benchmarking

**Scenario**: User wants to see real performance metrics for different sorting algorithms

**Request**:
```bash
curl -X POST http://localhost:8000/benchmark \
  -H "Content-Type: application/json" \
  -d '{
    "problem_type": "sorting",
    "input_size": 5000,
    "nearly_sorted": false,
    "algorithms": ["Merge Sort", "Quick Sort", "Heap Sort", "Insertion Sort"],
    "memory": "medium",
    "recursive_allowed": true
  }'
```

**Response** (excerpt):
```json
{
  "timings": [
    {
      "algorithm": "Merge Sort",
      "points": [
        {"x": 1250, "y": 0.00089},
        {"x": 2500, "y": 0.00234},
        {"x": 5000, "y": 0.00567}
      ],
      "time_complexity": "O(n log n)",
      "space_complexity": "O(n)"
    },
    {
      "algorithm": "Quick Sort",
      "points": [
        {"x": 1250, "y": 0.00067},
        {"x": 2500, "y": 0.00156},
        {"x": 5000, "y": 0.00389}
      ],
      "time_complexity": "O(n log n)",
      "space_complexity": "O(log n)"
    }
  ]
}
```

---

## 🧪 Testing

### Running Tests

Currently, the project uses manual testing through API documentation. To set up automated testing:

1. **Install pytest**:
   ```bash
   pip install pytest pytest-asyncio
   ```

2. **Create test file** (`backend/tests/test_api.py`):
   ```python
   import pytest
   from app.main import app
   from fastapi.testclient import TestClient

   client = TestClient(app)

   def test_health():
       response = client.get("/health")
       assert response.status_code == 200
       assert response.json() == {"status": "ok"}

   def test_recommend_sorting():
       response = client.post("/recommend", json={
           "problem_type": "sorting",
           "input_size": 1000,
           "memory": "medium",
           "recursive_allowed": True
       })
       assert response.status_code == 200
       assert "recommended_algorithm" in response.json()
   ```

3. **Run tests**:
   ```bash
   pytest backend/tests/ -v
   ```

---

## 🤝 Contributing

### Development Guidelines

1. **Code Style**: Follow PEP 8 for Python, ESLint rules for TypeScript/React
2. **Type Hints**: Use Python type hints and TypeScript types
3. **Documentation**: Document complex functions with docstrings
4. **Testing**: Write tests for new features
5. **Commits**: Use meaningful commit messages

### Adding New Algorithms

1. **Backend** ([algorithms/](backend/app/algorithms/)):
   ```python
   def my_algorithm(arr: List[int]) -> List[int]:
       """Implementation with type hints."""
       pass
   ```

2. **Update** [rules_engine.py](backend/app/decision/rules_engine.py):
   ```python
   if alg_name == "My Algorithm":
       return "O(n)", "O(1)"
   ```

3. **Test** through API

### Adding New Problem Types

1. Extend `ProblemType` in [schemas.py](backend/app/schemas.py)
2. Implement rules in [rules_engine.py](backend/app/decision/rules_engine.py)
3. Add UI support in [InputPanel.tsx](frontend/src/components/InputPanel.tsx)

### Submitting Changes

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and test
3. Commit: `git commit -m "Add new feature"`
4. Push: `git push origin feature/new-feature`
5. Create Pull Request

---

## 📄 File Reference

### Backend Key Files

| File | Purpose | Key Functions |
|------|---------|---------------|
| [main.py](backend/app/main.py) | FastAPI app factory | `create_app()` |
| [schemas.py](backend/app/schemas.py) | Data models | `RecommendationRequest`, `RecommendationResponse` |
| [sorting.py](backend/app/algorithms/sorting.py) | Sorting algorithms | `insertion_sort()`, `merge_sort()`, `heap_sort()`, `quick_sort()` |
| [searching.py](backend/app/algorithms/searching.py) | Searching algorithms | `linear_search()`, `binary_search()` |
| [benchmark.py](backend/app/api/benchmark.py) | Benchmarking | `benchmark_endpoint()` |
| [recommend.py](backend/app/api/recommend.py) | Recommendation router | API routing |
| [rules_engine.py](backend/app/decision/rules_engine.py) | Rule-based logic | `recommend_with_rules()` |
| [ml_engine.py](backend/app/decision/ml_engine.py) | ML predictions | `predict_best_algorithm()` |
| [engine.py](backend/app/decision/engine.py) | Decision orchestration | `recommend()` |
| [mongo.py](backend/app/db/mongo.py) | Database access | MongoDB operations |
| [config.py](backend/app/core/config.py) | Configuration | `get_settings()` |

### Frontend Key Files

| File | Purpose | Key Exports |
|------|---------|-------------|
| [App.tsx](frontend/src/App.tsx) | Root component | App component |
| [InputPanel.tsx](frontend/src/components/InputPanel.tsx) | User inputs | Form component |
| [OutputPanel.tsx](frontend/src/components/OutputPanel.tsx) | Results display | Results component |
| [ComplexityChart.tsx](frontend/src/components/visualization/ComplexityChart.tsx) | Big-O visualization | Chart component |
| [ExecutionTimeChart.tsx](frontend/src/components/visualization/ExecutionTimeChart.tsx) | Performance chart | Chart component |
| [client.ts](frontend/src/api/client.ts) | API client | Axios instance |
| [types.ts](frontend/src/types.ts) | TypeScript types | Type definitions |

---

## 🐛 Troubleshooting

### Backend Issues

**MongoDB Connection Error**:
```
MongoError: connect ECONNREFUSED 127.0.0.1:27017
```
- Solution: Ensure MongoDB is running locally or update `MONGODB_URI` in `.env`

**Module Import Error**:
```
ModuleNotFoundError: No module named 'app'
```
- Solution: Ensure you're running from the `backend` directory with activated virtual environment

**Port Already in Use**:
```
OSError: [Errno 48] Address already in use
```
- Solution: Run on different port: `uvicorn app.main:app --port 8001`

### Frontend Issues

**Dependencies Not Found**:
```
npm error: cannot find module 'react'
```
- Solution: Run `npm install` in frontend directory

**CORS Error**:
```
Access to XMLHttpRequest blocked by CORS policy
```
- Solution: Ensure backend CORS is configured for your frontend URL

**Port Conflict**:
```
Port 5173 is already in use
```
- Solution: Vite will use next available port, or specify: `npm run dev -- --port 5174`

---

## 📞 Support

### Getting Help

1. **API Documentation**: Visit `http://localhost:8000/docs` when server is running
2. **ReDoc**: Visit `http://localhost:8000/redoc` for alternative documentation
3. **Code Comments**: Detailed comments throughout codebase
4. **Error Logs**: Check terminal output for error messages

### Common Questions

**Q: How do I train a custom ML model?**
```bash
curl -X POST http://localhost:8000/train_ml \
  -H "Content-Type: application/json" \
  -d '{"n_samples": 10000, "force": true}'
```

**Q: Can I use the system without ML?**
Yes, set `ML_ENABLED=false` in `.env`. System will use rules-based recommendations.

**Q: What's the maximum input size supported?**
Default is 500,000. Configure with `MAX_BENCHMARK_INPUT_SIZE` in `.env`.

---

## 📝 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend with [React](https://react.dev/) and [Vite](https://vitejs.dev/)
- ML with [scikit-learn](https://scikit-learn.org/)
- Charts with [Chart.js](https://www.chartjs.org/)

---

## 📅 Project Timeline

| Phase | Status | Date |
|-------|--------|------|
| **Phase 1** | ✅ Complete | Initial Setup & API Development |
| **Phase 2** | ✅ Complete | Frontend UI Implementation |
| **Phase 3** | ✅ Complete | Rules Engine Integration |
| **Phase 4** | ✅ Complete | ML Model Training |
| **Phase 5** | ✅ Complete | Benchmarking System |
| **Phase 6** | ✅ Complete | Documentation |

---

## 🚀 Future Enhancements

- [ ] Support for additional algorithms (Graph algorithms, DP)
- [ ] Advanced ML model tuning and hyperparameter optimization
- [ ] Real-time collaborative recommendations
- [ ] Multi-language support
- [ ] Mobile application
- [ ] Cloud deployment templates
- [ ] Advanced analytics and usage tracking
- [ ] Community algorithm contributions

---

<div align="center">

**Made with ❤️ for algorithm enthusiasts**

[⬆ Back to Top](#algovia-ai---adaptive-algorithm-recommendation-system)

</div>
