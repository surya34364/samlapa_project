import uvicorn
from fastapi import FastAPI
from finmkt.fastapi import uvicorn_kwargs_from_settings, create_app_from_settings
from app.controllers.item_controller import router as item_router
from app.controllers.user_controller import router as user_router
from app.database import Base, engine
from app.middleware import add_process_time

# Automatically create tables in MySQL if they do not exist
Base.metadata.create_all(bind=engine)

app = create_app_from_settings()

app.middleware("http")(add_process_time)

app.include_router(user_router)
app.include_router(item_router)

if __name__ == "__main__":
    uvicorn.run("main:app", **uvicorn_kwargs_from_settings())