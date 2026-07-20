# Infraestructura AWS — Auditor-Agent

Este folder despliega la API de Auditor-Agent (`src/auditor_agent/api/app.py`)
como una función **AWS Lambda** detrás de **API Gateway**, usando
**AWS SAM**.

## Requisitos
- AWS CLI configurado (`aws configure`)
- AWS SAM CLI: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
- Una cuenta de AWS (Free Tier es suficiente para la demo)

## Deploy

```bash
cd Auditor-Agent
sam build --template-file infra/template.yaml
sam deploy --guided
```

Durante `sam deploy --guided` te va a preguntar el nombre del stack (ej.
`auditor-agent`), la región, y si confirmar cambios de IAM — respondiendo
"y" a todo es suficiente para la demo.

Al finalizar, SAM imprime la **URL pública de la API** en `Outputs.ApiUrl`.
Esa es la URL que se usa como **"demo en línea"** en el entregable del
hackathon.

## Probar la API desplegada

```bash
curl -X POST "<ApiUrl>audit" \
  -F "file=@ejemplo_inseguro.py"
```

## Correrlo localmente (sin AWS) para desarrollo
```bash
pip install -e .
pip install fastapi uvicorn mangum python-multipart
uvicorn auditor_agent.api.app:app --reload
```
Luego abre http://127.0.0.1:8000/docs para probar la API desde el navegador.
