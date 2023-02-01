from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, user, form
from app.routers import formData,userLogo

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(formData.router, tags=['formdatas'], prefix ='/api/formdatas')
app.include_router(userLogo.router,tags=['userlogos'], prefix ='/api/profilelogo')
app.include_router(form.router, tags=['forms'], prefix='/api/forms')

@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to Recuirement portal application"}

@app.get("/test")
def test():
    return {"status": "test working"}