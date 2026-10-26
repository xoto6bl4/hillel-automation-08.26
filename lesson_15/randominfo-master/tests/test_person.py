import csv
import unittest
from pathlib import Path

import randominfo


class PersonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (Path(randominfo.__file__).parent / 'data.csv').open(
            encoding='utf-8-sig', newline=''
        ) as data_file:
            rows = list(csv.DictReader(data_file))
        cls.names = {row['firstname']: row['gender'] for row in rows if row['firstname']}
        cls.hobbies = {row['hobbies'] for row in rows if row['hobbies']}
        cls.addresses = {
            (row['street address'], row['landmark'], row['area'], row['city'],
             row['state'], row['pincode'])
            for row in rows if row['street address'] and row['landmark']
        }

    def test_person_details_match_dataset(self):
        for gender in ('male', 'female'):
            for _ in range(10):
                with self.subTest(gender=gender):
                    person = randominfo.Person(gender)
                    self.assertEqual(person.gender, gender)
                    self.assertEqual(self.names[person.first_name], gender)
                    self.assertEqual(person.full_name, person.first_name + ' ' + person.last_name)
                    self.assertEqual(person.country, 'India')
                    self.assertEqual(person.address['country'], person.country)
                    self.assertIn(tuple(person.address[key] for key in
                        ('street', 'landmark', 'area', 'city', 'state', 'pincode')),
                        self.addresses)
                    self.assertTrue(1 <= len(person.hobbies) <= 6)
                    self.assertTrue(set(person.hobbies) <= self.hobbies)

    def test_country_with_and_without_name(self):
        self.assertEqual(randominfo.get_country(), 'India')
        self.assertEqual(randominfo.get_country(next(iter(self.names))), 'India')

    def test_invalid_gender_is_rejected(self):
        with self.assertRaises(ValueError):
            randominfo.Person('other')


if __name__ == '__main__':
    unittest.main()