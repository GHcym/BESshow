from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date

class CustomUserTests(TestCase):
    """Test suite for the CustomUser model."""

    def test_lunar_conversion_on_save(self):
        """
        Tests that the solar-to-lunar birth date conversion
        is correctly performed when a new user is saved.
        """
        User = get_user_model()
        solar_date = date(2024, 5, 19)
        
        # According to online converters, 2024-05-19 is the 12th day of the 4th month
        # in the Jia Chen (甲辰) year of the lunar calendar.
        expected_lunar_year = 2024
        expected_lunar_month = 4
        expected_lunar_day = 12

        user = User.objects.create(
            username="testuser",
            email="testuser@example.com",
            first_name="User",
            last_name="Test",
            gender="O",
            gregorian_birth_date=solar_date,
        )
        
        # Refresh the instance from the database to get the computed values
        user.refresh_from_db()

        self.assertIsNotNone(user.lunar_birth_date, "Lunar birth date should not be None.")
        
        # Assuming lunar_birth_date is a string in "YYYY-MM-DD" format
        lunar_date_parts = str(user.lunar_birth_date).split('-')
        
        self.assertEqual(int(lunar_date_parts[0]), expected_lunar_year)
        self.assertEqual(int(lunar_date_parts[1]), expected_lunar_month)
        self.assertEqual(int(lunar_date_parts[2]), expected_lunar_day)
        
        # Test that lunar_birth_time defaults to "吉時" (Auspicious Hour)
        self.assertEqual(user.lunar_birth_time, "吉時")