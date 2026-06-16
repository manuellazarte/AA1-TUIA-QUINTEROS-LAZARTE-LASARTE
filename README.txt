Para crear el entorno virtual vaya a la carpeta contenedora de los archivos y ejecute los siguientes comandos en orden:
python -m venv .\.venv (en Linux usar python3)
Set-ExecutionPolicy Unrestricted -Scope CurrentUser (solo en Windows) — Permite ejecutar scripts en PowerShell cambiando la política de ejecución. Sin este comando no será posible activar el entorno.
.\.venv\Scripts\Activate (en Linux usar source ./.venv/bin/activate) 

pip install -r requirements.txt