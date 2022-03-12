import enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Method(enum.Enum):
    pour_over = "1"
    aeropress = "2"
    espresso = "3"
    flair = "4"
    moka = "5"
    cupping = "6"


class Roast(enum.Enum):
    light = "1"
    medium = "2"
    dark = "3"


class Grinder(enum.Enum):
    jx_pro = "1"
    baratza_encore = "2"


class Brew(Base):
    __tablename__ = "brew"
    id = Column(Integer, primary_key=True, autoincrement=True)
    coffee = Column(ForeignKey("coffee.id"))
    method = Column(String)
    grinder = Column(String)
    grind_setting = Column(String)
    dose = Column(Numeric)
    temperature = Column(Integer, primary_key=True)
    coffee_out = Column(Numeric)
    duration = Column(String)
    thoughts = Column(String)
    date = Column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return (
            f"{self.method} @ {self.temperature}ºF made with the {self.grinder} set at"
            f" {self.grind_setting} on"
            f" {self.date.strftime('%Y-%m-%d at %H:%M:%S')}\n"
            f"{self.thoughts} It took {self.duration}."
        )


class Coffee(Base):
    __tablename__ = "coffee"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    roaster = Column(ForeignKey("roaster.id"))
    roast = Column(String)

    def __str__(self):
        return f"{self.name} ({self.roast} roast)"


class EspressoDetail(Base):
    __tablename__ = "espresso_detail"
    brew = Column(ForeignKey("brew.id"), primary_key=True, autoincrement=True)
    ratio = Column(String)
    preinfusion_duration = Column(String)

    def __str__(self):
        return f"{self.brew}. ratio of {self.ratio} with {self.preinfusion_duration} preinfusion"


class Roaster(Base):
    __tablename__ = "roaster"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    location = Column(String)

    def __str__(self):
        return f"{self.name} from {self.location}"
