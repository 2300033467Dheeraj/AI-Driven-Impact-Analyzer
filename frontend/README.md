# AI-Driven Impact Analyzer - Frontend

Production-ready Next.js 14 frontend for the AI-Driven Impact Analyzer for Cloud-Native Systems. Connects to a FastAPI backend at `http://localhost:8000`.

## Tech Stack

- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **Recharts**
- **Axios**
- **Lucide Icons**

## Installation

### Option 1: Fresh Setup (if starting from scratch)

```bash
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir=false --import-alias="@/*"
cd frontend
npm install axios recharts lucide-react
```

Then replace the generated files with the project structure provided.

### Option 2: Use This Project Directly

```bash
cd frontend
npm install
```

## Run

```bash
npm run dev
```

## Visit

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx           # Dashboard
│   ├── globals.css
│   ├── deployments/page.tsx
│   └── services/page.tsx
├── components/
│   ├── Sidebar.tsx
│   ├── RiskCard.tsx
│   ├── RiskGauge.tsx
│   ├── MetricsChart.tsx
│   ├── DeploymentTable.tsx
│   ├── BlastRadiusList.tsx
│   └── DecisionBadge.tsx
├── lib/
│   └── api.ts
├── types/
│   └── index.ts
└── ...
```

## API Endpoints

The frontend expects a FastAPI backend at `http://localhost:8000`:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/risk-score/latest` | Latest risk score and decision |
| GET | `/metrics` | Metrics time series (latency, error rate, etc.) |
| GET | `/service-blast-radius/{service}` | Blast radius for a given service |

If the backend is unavailable, the app uses mock/fallback data so you can run it fully on localhost.

## Features

- **Dashboard**: Risk score card, risk gauge, metrics chart, blast radius list, deployment decision badge. Auto-refresh every 10 seconds.
- **Deployments**: Table of past deployments with risk scores and decisions.
- **Services**: Enter a service name and fetch blast radius from the API.

## Development

```bash
npm run dev   # Start dev server
npm run build # Production build
npm run start # Start production server
npm run lint  # Run ESLint
```
