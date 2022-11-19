from app import app,settings,uvicorn
from api.endpoints import router as api_router

app.include_router(api_router)

def start():
    uvicorn.run(
        'app:app',
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
        log_level='info'
    )

if __name__ == '__main__':
    start()