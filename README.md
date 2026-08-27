\# Personal Finance Intelligence



An AI-powered personal finance web app that lets users upload bank/UPI transaction data, automatically categorizes spending, visualizes trends, forecasts future expenses, tracks savings goals, and answers natural-language questions about their finances using an AI analyst with real tool-calling.



\*\*Live demo:\*\* https://personal-finance-intelligence-two.vercel.app

\*\*API:\*\* https://personal-finance-intelligence-j7xz.onrender.com/docs



> Note: the backend is hosted on a free tier and may take 30–60 seconds to wake up on first request after inactivity.



\## Features



\- \*\*Authentication\*\* — JWT-based signup/login

\- \*\*Transaction Upload\*\* — CSV/Excel import with automatic cleaning, deduplication, and rule-based categorization

\- \*\*Dashboard\*\* — income, expenses, savings, and savings rate at a glance, with monthly trend, category breakdown, and top merchant charts

\- \*\*Insights\*\* — month-over-month comparisons, category spending changes, recurring expense detection, and statistical unusual-transaction detection

\- \*\*Forecasting\*\* — predicts next month's expenses using moving average or exponential smoothing, whichever backtests more accurately on the user's own history

\- \*\*AI Financial Analyst\*\* — natural language Q\&A powered by Google Gemini with multi-round tool-calling; answers are always grounded in real data pulled from the user's own transactions, never invented

\- \*\*Financial Goals\*\* — set savings targets with deadlines; the app calculates required monthly savings and flags whether the user is realistically on track



\## Tech Stack



\*\*Backend:\*\* FastAPI, SQLAlchemy, PostgreSQL, Pydantic, JWT (python-jose), bcrypt, pandas, Google Gemini API

\*\*Frontend:\*\* React 19, TypeScript, Vite, Tailwind CSS, React Router, Axios, Recharts

\*\*Testing:\*\* pytest (22 unit tests covering forecasting, goal calculations, and categorization logic)

\*\*Deployment:\*\* Vercel (frontend), Render (backend), Neon (PostgreSQL)



\## Architecture

frontend/ React + TypeScript SPA

backend/

app/

models/ SQLAlchemy ORM models

schemas/ Pydantic request/response schemas

routers/ FastAPI route handlers

services/ Business logic (analytics, forecasting, categorization, AI tool-calling, etc.)

tests/ pytest unit tests





The AI Analyst uses a controlled tool-calling architecture: Gemini can only answer questions by calling one of eight predefined functions (e.g. `get\_category\_spending`, `compare\_months`, `forecast\_spending`) that query the user's real transaction data. This guarantees the AI never fabricates financial figures.



\## Running Locally



\### Backend

```bash

cd backend

python -m venv venv

venv\\Scripts\\activate       # Windows

pip install -r requirements.txt

\# Create a .env file with DATABASE\_URL, SECRET\_KEY, GEMINI\_API\_KEY

uvicorn app.main:app --reload

```



\### Frontend

```bash

cd frontend

npm install

npm run dev

```



\### Tests

```bash

cd backend

python -m pytest -v

```



\## Environment Variables



\*\*Backend (`.env`)\*\*

| Variable | Description |

|---|---|

| `DATABASE\_URL` | PostgreSQL connection string |

| `SECRET\_KEY` | JWT signing secret |

| `GEMINI\_API\_KEY` | Google Gemini API key |

| `FRONTEND\_URL` | Deployed frontend URL (for CORS) |



\*\*Frontend (`.env.production`)\*\*

| Variable | Description |

|---|---|

| `VITE\_API\_URL` | Deployed backend API URL |



\## Project Status



All 11 planned phases complete: foundation, auth, transaction upload/categorization, dashboard, intelligence/insights, forecasting, AI analyst, financial goals, testing, and deployment.





