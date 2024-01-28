#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import db_storage
import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    storage = db_storage()
else:
    storage = FileStorage()
storage.reload()
