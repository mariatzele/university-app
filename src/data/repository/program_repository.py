"""
program_repository.py
Module for managing program records
"""
from ..db import DB
from .base_repository import BaseRepository


class ProgramRepository(BaseRepository):
    """
    Repository for managing program records.
    """

    def __init__(self, db: DB):
        super().__init__(db, "programs")
