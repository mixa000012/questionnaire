from enum import Enum
from sqlalchemy import Column, ForeignKey
from sqlalchemy import DateTime
import uuid
from sqlalchemy import String, ARRAY, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.db.base_class import Base


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"
    ROLE_PORTAL_SUPERADMIN = "ROLE_PORTAL_SUPERADMIN"


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    password = Column(String, nullable=False)
    admin_role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'))
    admin_role = relationship("Roles", backref="User", lazy='noload')
    surveys = relationship('Survey', backref='User', lazy='noload')

    @property
    def is_admin(self) -> bool:
        return self.admin_role.role == PortalRole.ROLE_PORTAL_ADMIN

    @property
    def is_superadmin(self) -> bool:
        return self.admin_role.role == PortalRole.ROLE_PORTAL_SUPERADMIN


class Roles(Base):
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String)

    def enrich_admin_roles_by_admin_role(self):
        if not self.is_admin:
            return PortalRole.ROLE_PORTAL_ADMIN

    def remove_admin_privileges_from_model(self):
        if self.is_admin:
            return {role for role in self.roles if role != PortalRole.ROLE_PORTAL_ADMIN}
