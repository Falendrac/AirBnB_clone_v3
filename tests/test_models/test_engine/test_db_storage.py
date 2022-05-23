#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pycodestyle
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_valid_case(self):
        """
        Test the get method of file_storage.
        In the valid way by take the first State of DB
        We need to create a new state before that.
        """
        state = State()
        state.name = "Test of State"
        models.storage.new(state)
        all_state = models.storage.all(State)
        key = list(all_state.keys())[0]
        state_get = models.storage.get(State, all_state[key].id)
        self.assertTrue(state_get is all_state[key])

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_unvalide_case_insert_none(self):
        """
        Test the get method of file_storage.
        But passes none in method.
        """
        state_get = models.storage.get(None, None)
        self.assertEqual(None, state_get)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_unvalid_case_instance_doesnt_exist(self):
        """
        Test the get method of file_storage.
        But passes an invalid id
        """
        state_get = models.storage.get(State, "dsjghp-sogihs-ezfzi3234")
        self.assertEqual(None, state_get)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all_objects(self):
        """
        Test the count method of file_storage.
        Test all objects.
        """
        all_objects = models.storage.all()
        count_objects = models.storage.count()

        self.assertEqual(count_objects, len(all_objects))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all_state(self):
        """
        Test the count method of file_storage.
        Pass State in argument.
        """
        all_states = models.storage.all(State)
        count_states = models.storage.count(State)

        self.assertEqual(count_states, len(all_states))
