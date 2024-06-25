from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase


# Declare a base class
class Base(DeclarativeBase):
    pass


class WorldTable(Base):
    __tablename__ = "world"
    uid = Column(Integer, primary_key=True)
    _max_tree_traverse = Column(Integer)
    _meld_strategy = Column(String)
    _monetary_desc = Column(String)
    _other_credor_pool = Column(Integer)
    _other_debtor_pool = Column(Integer)
    _penny = Column(Float)
    _pixel = Column(Float)
    _weight = Column(Integer)


class OtherUnitTable(Base):
    __tablename__ = "otherunit"

    uid = Column(Integer, primary_key=True)
    other_id = Column(String)
    credor_weight = Column(Integer)
    debtor_weight = Column(Integer)


class BeliefTable(Base):
    __tablename__ = "beliefunit"

    uid = Column(Integer, primary_key=True)
    belief_id = Column(String)


class OtherLinkTable(Base):
    __tablename__ = "otherlink"
    uid = Column(Integer, primary_key=True)
    belief_id = Column(String)
    other_id = Column(String)
    credor_weight = Column(Integer)
    debtor_weight = Column(Integer)


class IdeaTable(Base):
    __tablename__ = "idea"
    uid = Column(Integer, primary_key=True)
    label = Column(String)
    parent_road = Column(String)
    _addin = Column(Float)
    _begin = Column(Float)
    _close = Column(Float)
    _denom = Column(Integer)
    _meld_strategy = Column(String)
    _numeric_road = Column(String)
    _numor = Column(Integer)
    _problem_bool = Column(Integer)
    _range_source_road = Column(String)
    _reest = Column(Integer)
    _weight = Column(Integer)
    pledge = Column(Integer)


class BalanceLinkTable(Base):
    __tablename__ = "balancelink"
    uid = Column(Integer, primary_key=True)
    belief_id = Column(String)
    road = Column(String)
    credor_weight = Column(Float)
    debtor_weight = Column(Float)


class ReasonTable(Base):
    __tablename__ = "reason"
    uid = Column(Integer, primary_key=True)
    base = Column(String)
    road = Column(String)
    suff_idea_active = Column(Integer)


class PremiseTable(Base):
    __tablename__ = "premise"
    uid = Column(Integer, primary_key=True)
    base = Column(String)
    need = Column(String)
    road = Column(String)
    divisor = Column(Integer)
    nigh = Column(Float)
    open = Column(Float)


class SuffBeliefTable(Base):
    __tablename__ = "suffbelief"
    uid = Column(Integer, primary_key=True)
    belief_id = Column(String)
    road = Column(String)


class HealerHoldTable(Base):
    __tablename__ = "healerhold"
    uid = Column(Integer, primary_key=True)
    belief_id = Column(String)
    road = Column(String)


class FactTable(Base):
    __tablename__ = "fact"
    uid = Column(Integer, primary_key=True)
    base = Column(String)
    road = Column(String)
    nigh = Column(Float)
    open = Column(Float)
    pick = Column(String)
