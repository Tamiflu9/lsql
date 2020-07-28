# -*- coding: utf-8 -*-
"""
Copyright Enrique Martín <emartinm@ucm.es> 2020

Unit tests for the LSQL
"""

from django.test import TestCase

from .feedback import pretty_type, header_to_str, compare_select_results, compare_db_results, compare_function_results
from .types import VeredictCode


class FeedbackTest(TestCase):
    """Tests for module feedback"""

    @staticmethod
    def test_class_names():
        """Test for function pretty_type"""
        assert pretty_type("<class 'cx_Oracle.INTEGER'>") == 'INTEGER'
        assert pretty_type("otro tipo") == 'otro tipo'

    @staticmethod
    def test_header_to_str():
        """Test for header_to_str"""
        header = [['ID', "<class 'cx_Oracle.NUMBER'>"], ['NOMBRE', "<class 'cx_Oracle.STRING'>"]]
        expected = "(ID: NUMBER, NOMBRE: STRING)"
        assert header_to_str(header) == expected

    @staticmethod
    def test_compare_select():
        """Test for compare_select_results"""
        expected = {'header': [['ID', "<class 'cx_Oracle.NUMBER'>"], ['NOMBRE', "<class 'cx_Oracle.STRING'>"]],
                    'rows': [[1, 'a'], [2, 'b']]}
        obtained1 = {'header': [['ID', "<class 'cx_Oracle.NUMBER'>"], ['NOMBRE', "<class 'cx_Oracle.STRING'>"]],
                     'rows': [[2, 'b'], [1, 'a']]}
        obtained2 = {'header': [['ID', "<class 'cx_Oracle.NUMBER'>"], ['NOMBRE', "<class 'cx_Oracle.STRING'>"]],
                     'rows': [[1, 'a']]}
        obtained3 = {'header': [['ID', "<class 'cx_Oracle.NUMBER'>"], ['NOMBRE', "<class 'cx_Oracle.STRING'>"]],
                     'rows': [[1, 'a'], [2, 'b'], [3, 'a']]}
        obtained4 = {'header': [['ID', "<class 'cx_Oracle.NUMBER'>"], ['NOMBRE', "<class 'cx_Oracle.STRING'>"]],
                     'rows': [[1, 'a'], [2, 'b'], [1, 'a']]}
        obtained5 = {'header': [['IDi', "<class 'cx_Oracle.NUMBER'>"], ['NOMBRE', "<class 'cx_Oracle.STRING'>"]],
                     'rows': [[1, 'a'], [2, 'b']]}
        obtained6 = {'header': [['ID', "<class 'cx_Oracle.NUMBER'>"], ['NOMBRE', "<class 'cx_Oracle.NUMBER'>"]],
                     'rows': [[1, 'a'], [2, 'b']]}
        obtained7 = {'header': [['ID', "<class 'cx_Oracle.NUMBER'>"]],
                     'rows': [[1], [2]]}
        obtained8 = {'header': [['ID', "<class 'cx_Oracle.NUMBER'>"], ['NOMBRE', "<class 'cx_Oracle.STRING'>"],
                                ['NOMBRE', "<class 'cx_Oracle.STRING'>"]],
                     'rows': [[1, 'a', 'a'], [2, 'b', 'b']]}

        # Expected equal to obtained
        assert compare_select_results(expected, expected, True)[0] == VeredictCode.AC
        assert compare_select_results(expected, expected, False)[0] == VeredictCode.AC
        # Obtained rows are correct but in other order
        assert compare_select_results(expected, obtained1, False)[0] == VeredictCode.AC
        assert compare_select_results(expected, obtained1, True)[0] == VeredictCode.WA
        # Missing row in obtained
        assert compare_select_results(expected, obtained2, False)[0] == VeredictCode.WA
        assert compare_select_results(expected, obtained2, True)[0] == VeredictCode.WA
        # Extra row in obtained
        assert compare_select_results(expected, obtained3, False)[0] == VeredictCode.WA
        assert compare_select_results(expected, obtained3, True)[0] == VeredictCode.WA
        # Extra row in obtained, and the extra row is a duplicate of other row
        assert compare_select_results(expected, obtained4, False)[0] == VeredictCode.WA
        assert compare_select_results(expected, obtained4, True)[0] == VeredictCode.WA
        # Obtained headers have a row with a different name
        assert compare_select_results(expected, obtained5, False)[0] == VeredictCode.WA
        assert compare_select_results(expected, obtained5, True)[0] == VeredictCode.WA
        # Obtained headers have a row with a different type
        assert compare_select_results(expected, obtained6, False)[0] == VeredictCode.WA
        assert compare_select_results(expected, obtained6, True)[0] == VeredictCode.WA
        # Obtained headers have less columns
        assert compare_select_results(expected, obtained7, False)[0] == VeredictCode.WA
        assert compare_select_results(expected, obtained7, True)[0] == VeredictCode.WA
        # Obtained headers have more columns
        assert compare_select_results(expected, obtained8, False)[0] == VeredictCode.WA
        assert compare_select_results(expected, obtained8, True)[0] == VeredictCode.WA

    @staticmethod
    def test_compare_db():
        """Tests for compare_db_results"""
        table1 = {'header': [['ID', "<class 'cx_Oracle.NUMBER'>"], ['NOMBRE', "<class 'cx_Oracle.STRING'>"]],
                  'rows': [[1, 'a'], [2, 'b']]}
        table2 = {'header': [['ID', "<class 'cx_Oracle.NUMBER'>"], ['NOMBRE', "<class 'cx_Oracle.STRING'>"]],
                  'rows': [[1, 'zzzz'], [2, 'b']]}
        table3 = {'header': [['ID', "<class 'cx_Oracle.NUMBER'>"], ['NOMBRE', "<class 'cx_Oracle.STRING'>"]],
                  'rows': [[2, 'b'], [1, 'a']]}
        expected = {'table1': table1, 'table2': table1}
        obtained1 = {'table1': table1}
        obtained2 = {'table1': table1, 'table2': table1, 'table3': table1}
        obtained3 = {'table1': table1, 'table2': table2}
        obtained4 = {'table1': table1, 'table2': table3}

        # Identical DB
        assert compare_db_results(expected, expected)[0] == VeredictCode.AC
        # Missing table
        assert compare_db_results(expected, obtained1)[0] == VeredictCode.WA
        # Extra table
        assert compare_db_results(expected, obtained2)[0] == VeredictCode.WA
        # Number and types of tables correct, but one table has different tuples
        assert compare_db_results(expected, obtained3)[0] == VeredictCode.WA
        # Number and types of tables correct, but one differs in order
        assert compare_db_results(expected, obtained4)[0] == VeredictCode.AC

    @staticmethod
    def test_compare_function():
        """Tests for compare_function_results"""
        expected = {'fun(1)': 3, 'fun(2)': 56}
        obtained1 = {'fun(1)': 3, 'fun(2)': 5}
        obtained2 = {'fun(1)': 33, 'fun(2)': 56}

        # Identical
        assert compare_function_results(expected, expected)[0] == VeredictCode.AC
        # Wrong result in first call
        assert compare_function_results(expected, obtained2)[0] == VeredictCode.WA
        # Wrong result in second call
        assert compare_function_results(expected, obtained1)[0] == VeredictCode.WA
