"""Adaptador para correr la API de Auditor-Agent en AWS Lambda.

Usa Mangum para envolver la app de FastAPI y exponerla vía API Gateway.
"""

from mangum import Mangum

from auditor_agent.api.app import app

handler = Mangum(app)
