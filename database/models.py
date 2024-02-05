from sqlalchemy import DECIMAL, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from database.database import Base


class Menu(Base):
    __tablename__ = 'menu'

    submenus: Mapped[list['Submenu']] = relationship('Submenu', back_populates='menu', cascade='all, delete-orphan',
                                                     passive_deletes=True,
                                                     lazy='selectin')


class Submenu(Base):
    __tablename__ = 'submenu'

    menu_id = Column(UUID(as_uuid=True), ForeignKey('menu.id', ondelete='CASCADE'))

    menu: Mapped['Menu'] = relationship('Menu', back_populates='submenus', lazy='selectin')
    dishes: Mapped[list['Dish']] = relationship('Dish', back_populates='submenu', cascade='all, delete-orphan',
                                                passive_deletes=True, lazy='selectin')


class Dish(Base):
    __tablename__ = 'dish'

    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenu.id', ondelete='CASCADE'))
    price = Column(DECIMAL(10, 2), nullable=False)

    submenu: Mapped['Submenu'] = relationship('Submenu', back_populates='dishes', lazy='selectin')
