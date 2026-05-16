# Noorish — start all services
$Root = $PSScriptRoot

# ── 1. Database ───────────────────────────────────────────────────────────────
Write-Host "Starting database..." -ForegroundColor Cyan
docker compose up -d
if (-not $?) { Write-Host "docker compose failed — is Docker running?" -ForegroundColor Red; exit 1 }

# Wait for Postgres to be healthy
Write-Host "Waiting for Postgres..." -ForegroundColor Cyan
$tries = 0
do {
    Start-Sleep -Seconds 2
    $health = docker inspect --format "{{.State.Health.Status}}" (docker compose ps -q db) 2>$null
    $tries++
} while ($health -ne "healthy" -and $tries -lt 15)

if ($health -ne "healthy") {
    Write-Host "Postgres did not become healthy in time." -ForegroundColor Red; exit 1
}

# ── 2. Backend ────────────────────────────────────────────────────────────────
Write-Host "Starting backend..." -ForegroundColor Cyan
$backendDir = Join-Path $Root "backend"
$uvicorn    = Join-Path $backendDir ".venv\Scripts\uvicorn.exe"

if (-not (Test-Path $uvicorn)) {
    Write-Host "venv not found — run: cd backend; python -m venv .venv; pip install -r requirements.txt" -ForegroundColor Red
    exit 1
}

# Run migrations before starting
& (Join-Path $backendDir ".venv\Scripts\alembic.exe") --config (Join-Path $backendDir "alembic.ini") upgrade head
if (-not $?) { Write-Host "Alembic migration failed." -ForegroundColor Red; exit 1 }

$backend = Start-Process -FilePath $uvicorn `
    -ArgumentList "app.main:app", "--reload", "--port", "8000" `
    -WorkingDirectory $backendDir `
    -PassThru -NoNewWindow
Write-Host "Backend PID $($backend.Id) — http://localhost:8000" -ForegroundColor Green

# ── 3. Frontend ───────────────────────────────────────────────────────────────
Write-Host "Starting frontend..." -ForegroundColor Cyan
$frontendDir = Join-Path $Root "frontend"

$frontend = Start-Process -FilePath "npm" `
    -ArgumentList "run", "dev" `
    -WorkingDirectory $frontendDir `
    -PassThru -NoNewWindow
Write-Host "Frontend PID $($frontend.Id) — http://localhost:5173" -ForegroundColor Green

# ── Wait ──────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "All services running. Press Ctrl+C to stop." -ForegroundColor Yellow

try {
    while ($true) { Start-Sleep -Seconds 5 }
} finally {
    Write-Host "`nStopping..." -ForegroundColor Cyan
    Stop-Process -Id $backend.Id  -ErrorAction SilentlyContinue
    Stop-Process -Id $frontend.Id -ErrorAction SilentlyContinue
    docker compose stop
    Write-Host "Done." -ForegroundColor Green
}
