import uvicorn

if __name__ == "__main__":
    uvicorn.run("Trabalho_BD2.IntegrationApplication.integration_api.integration_application:app",  # exemplo: main:app
                host="127.0.0.1",
                port=8000,
                reload=True,
                log_level="debug")