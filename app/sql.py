from sqlalchemy import (
    Column, String, Integer, Float, Date, Text, ForeignKey,
    PrimaryKeyConstraint, Index, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from .config import POSTGRES_URL

Base = declarative_base()


# ------------------------------------------------------------
# Committee Table
# ------------------------------------------------------------
class Committee(Base):
    __tablename__ = "committees"

    committee_id = Column(String, primary_key=True)
    name = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    treasurer_name = Column(String)
    street_1 = Column(String)
    street_2 = Column(String)
    organization_type = Column(String)
    designation = Column(String)
    party = Column(String)

    # Relationships
    independent_expenditures = relationship(
        "IndependentExpenditure",
        back_populates="committee"
    )

    contributions = relationship(
        "Contribution",
        back_populates="committee"
    )


# ------------------------------------------------------------
# Independent Expenditures (IE)
# Composite PK: unique_id + filing_id
# ------------------------------------------------------------
class IndependentExpenditure(Base):
    __tablename__ = "independent_expenditures"
    __table_args__ = (
        PrimaryKeyConstraint("unique_id", "filing_id"),
        Index("ix_ie_committee", "fec_committee_id"),
        Index("ix_ie_candidate", "fec_candidate_id"),
        Index("ix_ie_date", "date"),
    )

    unique_id = Column(String, nullable=False)
    filing_id = Column(String, nullable=False)

    # Committee link
    fec_committee_id = Column(
        String,
        ForeignKey("committees.committee_id"),
        nullable=True
    )

    fec_committee_name = Column(String)
    fec_candidate = Column(String)
    fec_candidate_id = Column(String)
    candidate_name = Column(String)

    amount = Column(Float)
    office = Column(String)
    state = Column(String)
    district = Column(String)
    date = Column(Date)
    date_received = Column(Date)
    dissemination_date = Column(Date)
    purpose = Column(Text)
    payee = Column(String)
    support_or_oppose = Column(String)
    form_type = Column(String)
    amended_from = Column(String)
    miscellaneous_text = Column(Text)
    transaction_id = Column(String)

    # ORM relationship
    committee = relationship(
        "Committee", back_populates="independent_expenditures")


# ------------------------------------------------------------
# Schedule A Contributions
# No natural primary key → autoincrement surrogate key
# ------------------------------------------------------------
class Contribution(Base):
    __tablename__ = "contributions"
    __table_args__ = (
        Index("ix_contrib_committee", "committee_id"),
        Index("ix_contrib_date", "contribution_receipt_date"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    committee_id = Column(
        String,
        ForeignKey("committees.committee_id"),
        nullable=False
    )

    contributor_name = Column(String)
    contributor_city = Column(String)
    contributor_state = Column(String)
    contributor_zip = Column(String)
    contributor_employer = Column(String)
    contributor_occupation = Column(String)

    contribution_receipt_amount = Column(Float)
    contribution_receipt_date = Column(Date)
    memo_text = Column(Text)

    # ORM relationship
    committee = relationship("Committee", back_populates="contributions")


# ------------------------------------------------------------
# Database Initialization Helper
# ------------------------------------------------------------


def init_db(database_url: str = POSTGRES_URL):
    """
    Create all tables and return a session factory.
    """
    engine = create_engine(database_url, echo=True)

    # Create tables
    Base.metadata.create_all(engine)

    return sessionmaker(bind=engine)
