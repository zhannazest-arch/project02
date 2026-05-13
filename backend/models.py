from sqlalchemy import Column, Integer, String, Float, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

university_specialties = Table(
    "university_specialties",
    Base.metadata,
    Column("university_id", Integer, ForeignKey("universities.id"), primary_key=True),
    Column("specialty_id", Integer, ForeignKey("specialties.id"), primary_key=True),
)


class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False)
    description = Column(Text)
    logo_url = Column(String)
    image_url = Column(String)
    website = Column(String)
    ranking = Column(Integer)
    founded_year = Column(Integer)
    tuition_min = Column(Integer)
    tuition_max = Column(Integer)
    students_count = Column(Integer)

    specialties = relationship(
        "Specialty", secondary=university_specialties, back_populates="universities"
    )
    admission = relationship(
        "AdmissionRequirement", back_populates="university", uselist=False, cascade="all, delete-orphan"
    )


class Specialty(Base):
    __tablename__ = "specialties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    universities = relationship(
        "University", secondary=university_specialties, back_populates="specialties"
    )


class AdmissionRequirement(Base):
    __tablename__ = "admission_requirements"

    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"), unique=True, nullable=False)
    description = Column(Text)
    min_gpa = Column(Float)
    language_requirement = Column(String)

    university = relationship("University", back_populates="admission")
    exams = relationship(
        "AdmissionExam", back_populates="requirement", cascade="all, delete-orphan", order_by="AdmissionExam.id"
    )


class AdmissionExam(Base):
    __tablename__ = "admission_exams"

    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("admission_requirements.id"), nullable=False)
    exam_name = Column(String, nullable=False)
    min_score = Column(String)
    max_score = Column(String)
    notes = Column(String)

    requirement = relationship("AdmissionRequirement", back_populates="exams")
