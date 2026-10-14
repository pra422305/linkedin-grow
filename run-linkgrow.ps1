Set-Location -LiteralPath "$PSScriptRoot\LinkGrowAI"

if (-not (Test-Path -LiteralPath ".venv\Scripts\Activate.ps1")) {
    python -m venv .venv
}

.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
flask --app app:create_app init-db
flask --app app:create_app run
