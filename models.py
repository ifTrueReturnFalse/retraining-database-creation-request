from sqlalchemy import String, ForeignKey, Integer, Float, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
from datetime import date


class Base(DeclarativeBase):
  pass


class Region(Base):
  #Declaration
  __tablename__ = "region"
  id_region: Mapped[int] = mapped_column(primary_key=True)
  nom: Mapped[str] = mapped_column(String(100))
  #Relations
  departements: Mapped[List["Departement"]
                       ] = relationship(back_populates="region")


class Departement(Base):
  #Declaration
  __tablename__ = "departement"
  id_departement: Mapped[str] = mapped_column(String(3), primary_key=True)
  id_region: Mapped[int] = mapped_column(ForeignKey("region.id_region"))
  nom: Mapped[str] = mapped_column(String(100))
  #Relations
  region: Mapped["Region"] = relationship(back_populates="departements")
  communes: Mapped[List["Commune"]] = relationship(back_populates="departement")


class Commune(Base):
  #Declaration
  __tablename__ = "commune"
  id_commune: Mapped[int] = mapped_column(Integer, primary_key=True)
  id_departement: Mapped[int] = mapped_column(
      ForeignKey("departement.id_departement"))
  nom: Mapped[str] = mapped_column(String(50))
  code_commune: Mapped[int] = mapped_column(Integer)
  code_insee: Mapped[str] = mapped_column(String(6))
  #Relations
  departement: Mapped["Departement"] = relationship(back_populates="communes")
  adresses: Mapped[List["Adresse"]] = relationship(back_populates="commune")


class Adresse(Base):
  #Declaration
  __tablename__ = "adresse"
  id_adresse: Mapped[int] = mapped_column(Integer, primary_key=True)
  id_commune: Mapped[int] = mapped_column(ForeignKey("commune.id_commune"))
  numero_voie: Mapped[int | None] = mapped_column(Integer)
  nom_voie: Mapped[str | None] = mapped_column(String(100))
  id_voie: Mapped[int] = mapped_column(
      Integer, ForeignKey("type_voie.id_voie"))
  #Relations
  type_voie: Mapped["TypeVoie"] = relationship(back_populates="adresses")
  commune: Mapped["Commune"] = relationship(back_populates="adresses")
  biens: Mapped[List["Bien"]] = relationship(back_populates="adresse")


class TypeVoie(Base):
  #Declaration
  __tablename__ = "type_voie"
  id_voie: Mapped[int] = mapped_column(Integer, primary_key=True)
  voie: Mapped[str] = mapped_column(String(5))
  #Relations
  adresses: Mapped[List["Adresse"]] = relationship(back_populates="type_voie")


class Bien(Base):
  #Declaration
  __tablename__ = "bien"
  id_bien: Mapped[int] = mapped_column(Integer, primary_key=True)
  id_adresse: Mapped[int] = mapped_column(ForeignKey("adresse.id_adresse"))
  btq: Mapped[str | None] = mapped_column(String(5))
  nombre_pieces: Mapped[int] = mapped_column(Integer)
  surface_carrez: Mapped[float] = mapped_column(Float)
  surface_local: Mapped[int] = mapped_column(Integer)
  type_bien: Mapped[str] = mapped_column(String(20))
  lot: Mapped[int] = mapped_column(Integer)
  #Relations
  adresse: Mapped["Adresse"] = relationship(back_populates="biens")
  ventes: Mapped[List["Vente"]] = relationship(back_populates="bien")


class Vente(Base):
  #Declaration
  __tablename__ = "vente"
  id_vente: Mapped[int] = mapped_column(Integer, primary_key=True)
  id_bien: Mapped[int] = mapped_column(ForeignKey("bien.id_bien"))
  date_vente: Mapped[date] = mapped_column(Date)
  valeur: Mapped[float] = mapped_column(Float)
  #Relations
  bien: Mapped["Bien"] = relationship(back_populates="ventes")
