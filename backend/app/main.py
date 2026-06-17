# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.api.connectors import router as connector_router

# app = FastAPI(
#     title="Social Listening Platform"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(
#     connector_router,
#     prefix="/connectors",
#     tags=["Connectors"]
# )


# @app.get("/")
# def root():

#     return {
#         "status": "running"
#     }










from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.dashboard import router as dashboard_router
from app.routers import mentions
from app.routers.reports import (
    router as reports_router
)
from app.api.connectors import router as connector_router

app = FastAPI(
    title="Social Listening Platform"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://sml-backend-agdr.onrender.com/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    connector_router,
    prefix="/connectors",
    tags=["Connectors"]
)


@app.get("/")
def root():

    return {
        "status": "running"
    }



# for dashboard page

app.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"]
)

# for route in app.routes:
#     print(route.path)


app.include_router(
    reports_router,
    prefix="/reports",
    tags=["Reports"]
)


app.include_router(
    mentions.router,
    prefix="/mentions",
    tags=["Mentions"]
)
