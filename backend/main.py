from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth, customer, partner, booking
from src.config.database import engine, Base, get_db
from src.seed.seed_data import seed_database
from contextlib import asynccontextmanager
from src.services.notification import notification_service
import typer

cli = typer.Typer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    if not notification_service.scheduler.running:
        notification_service.scheduler.start()
    yield
    if notification_service.scheduler.running:
        notification_service.scheduler.shutdown()
    engine.dispose()

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

@cli.command()
def seed():
    """Seed the database with initial data."""
    db = next(get_db())
    try:
        seed_database(db)
        typer.echo("Database seeded successfully!")
    except Exception as e:
        typer.echo(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    cli()