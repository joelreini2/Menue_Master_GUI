"""Einfache Tests für die Kernlogik.

Diese Tests sind bewusst klein gehalten, aber decken die wichtigsten Fachregeln ab.
"""

import unittest

from app.models.mealplan import WEEKDAYS
from app.models.shopping_list import ShoppingList


class ShoppingListTest(unittest.TestCase):
    def test_amounts_are_summed_per_name_and_unit(self):
        shopping_list = ShoppingList()
        shopping_list.add_item("Tomate", "Stück", 1)
        shopping_list.add_item("Tomate", "Stück", 2)
        shopping_list.add_item("Milch", "ml", 200)

        self.assertEqual(shopping_list.items[("Tomate", "Stück")], 3)
        self.assertEqual(shopping_list.items[("Milch", "ml")], 200)

    def test_rows_are_sorted(self):
        shopping_list = ShoppingList()
        shopping_list.add_item("Zwiebel", "Stück", 1)
        shopping_list.add_item("Apfel", "Stück", 2)

        rows = shopping_list.as_rows()
        self.assertEqual(rows[0][0], "Apfel")
        self.assertEqual(rows[1][0], "Zwiebel")


class WeekdayTest(unittest.TestCase):
    def test_week_has_seven_days(self):
        self.assertEqual(len(WEEKDAYS), 7)
        self.assertEqual(WEEKDAYS[0], "Montag")
        self.assertEqual(WEEKDAYS[-1], "Sonntag")


if __name__ == "__main__":
    unittest.main()
