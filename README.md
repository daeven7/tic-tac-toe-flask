# Tic-Tac-Toe Full Stack Application

##  Architecture

- **Flask API** - Game logic and AI moves
- **Node.js Backend** - Authentication, game sessions, and user management
- **React Frontend** - Web interface
- **React Native App** - Mobile interface

## 🚀 Quick Start

### 1. Run Flask Application (Game Logic API)

```bash
# Clone the Flask repository
git clone https://github.com/daeven7/tic-tac-toe-flask

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The Flask server will start on `http://localhost:5000`

### 2. Run Node.js Backend

```bash
# Clone the backend repository
git clone https://github.com/daeven7/tic-tac-toe-backend.git

# Install dependencies
npm install

```

Create a `.env` file in the backend directory with:
```bash
PORT=3000
MONGODB_URI=your_mongodb_uri
JWT_ACCESS_SECRET=your-access-secret-key
JWT_REFRESH_SECRET=your-refresh-secret-key
PYTHON_API_URL=http://localhost:5000
```

```bash
# Start the development server
npm run dev
```

The Node.js server will run on `http://localhost:3000`

### 3. Run React Frontend

```bash
# Clone the Frontend repository
https://github.com/daeven7/tic-tac-toe-frontend.git

# Install dependencies
npm install

```

Create a `.env` file in the frontend directory with:
```bash
# Base URL for API endpoints
VITE_BASE_URL=http://localhost:3000
```

```bash
# Start the development server
npm run dev
```

The React frontend will run on `http://localhost:5173/`

### 4. Run React Native App

```bash
# Clone the react-native repository
https://github.com/daeven7/tic-tac-toe-native.git

# Install dependencies
npm install

# Start the development server
npm run start
```

The React Native app will run on `http://localhost:8081/`



## 🛠️ Technologies Used

### Frontend
- **React:** Component-based library for building user interfaces
- **Vite:** Fast build tool and development server
- **Redux:** State management library for React
- **React-Query:** Data fetching and state management for API state
- **Modular SCSS:** Modular styles for better code organization
- **TypeScript:** Enforces type safety for clean and maintainable code
- **Ant Design (antd):** UI framework for polished, professional design

### Backend
- **Node.js:** JavaScript runtime for building efficient, scalable server-side applications
- **TypeScript:** Enforces type safety for clean and maintainable code
- **Mongoose:** ODM for MongoDB integration
- **Express:** Web application framework for Node.js
- **JWT:** JSON Web Tokens for authentication

### Mobile
- **React Native:** Cross-platform mobile development framework
- **Expo:** Development platform for React Native

### Database
- **MongoDB:** NoSQL database for high scalability and performance



##  Security Practices

### 1. JWT Refresh Token Strategy
- Refresh tokens enable secure re-authentication by generating short-lived access tokens without re-entering credentials
- Implemented token rotation to enhance security
- Blacklists previously used refresh tokens to prevent reuse, even if someone gains access to the token

### 2. Persistent Authentication and Silent Refresh
- Ensures the user remains authenticated even after refreshing the page
- Refresh tokens are refreshed automatically when the access token expires, without the user noticing
