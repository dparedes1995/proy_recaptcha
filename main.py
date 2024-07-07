import logging
from fastapi import FastAPI
from routers.recaptcha_router import router as recaptcha_router

# Configurar el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(title="reCAPTCHA Solver API")

# Incluir el router de reCAPTCHA en la aplicación FastAPI
app.include_router(recaptcha_router)

# Iniciar la aplicación con el logging
@app.on_event("startup")
async def startup_event():
    logging.info("Iniciando la aplicación reCAPTCHA Solver API...")

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API reCAPTCHA Solver"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
