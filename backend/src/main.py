# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth, customer, partner, booking
from src.config.database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(
    title="Service Booking API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(customer.router, prefix="/api/customers", tags=["Customers"])
app.include_router(partner.router, prefix="/api/partners", tags=["Partners"])
app.include_router(booking.router, prefix="/api/bookings", tags=["Bookings"])
