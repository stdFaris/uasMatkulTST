from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth, customers, partners, bookings, reviews, notifications

app = FastAPI()

# Konfigurasi CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Daftar origin yang diizinkan
    allow_credentials=True,     # Mengizinkan credentials
    allow_methods=["*"],        # Mengizinkan semua method HTTP
    allow_headers=["*"],        # Mengizinkan semua headers
)

# Include routers
app.include_router(auth.router)
app.include_router(customers.router) 
app.include_router(partners.router)
app.include_router(bookings.router)
app.include_router(reviews.router)
app.include_router(notifications.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Service Booking API"}
