
import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


# =========================================================
# USER
# =========================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    avatar_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    github_connections = relationship(
        "GithubConnection",
        back_populates="user",
    )


# =========================================================
# GITHUB CONNECTION
# =========================================================

class GithubConnection(Base):
    __tablename__ = "github_connections"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    github_user_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    github_username: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    access_token: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="github_connections",
    )

    repositories = relationship(
        "Repository",
        back_populates="github_connection",
    )


# =========================================================
# REPOSITORY
# =========================================================

class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    github_connection_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "github_connections.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    github_repo_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    clone_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    html_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    default_branch: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_private: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    language: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    github_connection = relationship(
        "GithubConnection",
        back_populates="repositories",
    )

    scans = relationship(
        "Scan",
        back_populates="repository",
        cascade="all, delete-orphan",
    )


# =========================================================
# SCAN
# =========================================================

class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    repository_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "repositories.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    branch: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    commit_sha: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="QUEUED",
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    overall_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    security_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    quality_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    performance_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    maintainability_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    reliability_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    total_files: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    total_issues: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    critical_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    high_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    medium_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    low_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    info_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    repository = relationship(
        "Repository",
        back_populates="scans",
    )

    issues = relationship(
        "Issue",
        back_populates="scan",
        cascade="all, delete-orphan",
    )


# =========================================================
# RULE
# =========================================================

class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    rule_code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    default_severity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    language: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    is_security: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    issues = relationship(
        "Issue",
        back_populates="rule",
    )


# =========================================================
# ISSUE
# =========================================================

class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "scans.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    rule_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "rules.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    fingerprint: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    severity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    language: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    file_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    line_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    end_line_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    column_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    code_snippet: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    suggestion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    impact: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_security_issue: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="OPEN",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    scan = relationship(
        "Scan",
        back_populates="issues",
    )

    rule = relationship(
        "Rule",
        back_populates="issues",
    )

    explanations = relationship(
        "IssueExplanation",
        back_populates="issue",
        cascade="all, delete-orphan",
    )


# =========================================================
# ISSUE EXPLANATION
# =========================================================

class IssueExplanation(Base):
    __tablename__ = "issue_explanations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    issue_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "issues.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    recommended_fix: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ai_generated: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    issue = relationship(
        "Issue",
        back_populates="explanations",
    )

