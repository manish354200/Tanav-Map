"""SQLAlchemy ORM entities."""

from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="counselor")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Victim(Base):
    __tablename__ = "victims"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    case_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="registered")
    current_distress_score: Mapped[float] = mapped_column(Float, default=50.0)
    risk_level: Mapped[str] = mapped_column(String(20), default="medium")
    registration_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    interactions: Mapped[list["Interaction"]] = relationship(back_populates="victim", cascade="all, delete-orphan")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="victim", cascade="all, delete-orphan")
    interventions: Mapped[list["Intervention"]] = relationship(back_populates="victim", cascade="all, delete-orphan")
    distress_history: Mapped[list["DistressHistory"]] = relationship(back_populates="victim", cascade="all, delete-orphan")


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    victim_id: Mapped[int] = mapped_column(ForeignKey("victims.id"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), default="text")
    message: Mapped[str | None] = mapped_column(Text)
    channel: Mapped[str] = mapped_column(String(50), default="chatbot")
    audio_file_path: Mapped[str | None] = mapped_column(String(255))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)

    victim: Mapped["Victim"] = relationship(back_populates="interactions")


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    victim_id: Mapped[int] = mapped_column(ForeignKey("victims.id"), nullable=False, index=True)
    level: Mapped[str] = mapped_column(String(20), default="low")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)

    victim: Mapped["Victim"] = relationship(back_populates="alerts")


class Intervention(Base):
    __tablename__ = "interventions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    victim_id: Mapped[int] = mapped_column(ForeignKey("victims.id"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), default="counseling")
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    victim: Mapped["Victim"] = relationship(back_populates="interventions")


class DistressHistory(Base):
    __tablename__ = "distress_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    victim_id: Mapped[int] = mapped_column(ForeignKey("victims.id"), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False)
    sentiment_score: Mapped[float] = mapped_column(Float, default=0.0)
    voice_score: Mapped[float] = mapped_column(Float, default=0.0)
    behavior_score: Mapped[float] = mapped_column(Float, default=0.0)
    threat_score: Mapped[float] = mapped_column(Float, default=0.0)
    history_score: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    victim: Mapped["Victim"] = relationship(back_populates="distress_history")
