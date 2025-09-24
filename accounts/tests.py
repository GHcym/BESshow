from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, time

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

    def test_bazi_calculation_on_save(self):
        """
        Tests that the bazi calculation is correctly performed when a user is saved.
        """
        User = get_user_model()
        solar_date = date(2024, 5, 19)  # 甲辰年
        birth_time = time(14, 30, 0)  # 下午2:30

        user = User.objects.create(
            username="bazitestuser",
            email="bazitest@example.com",
            first_name="Bazi",
            last_name="Test",
            gender="O",
            gregorian_birth_date=solar_date,
            gregorian_birth_time=birth_time,
        )

        # Refresh the instance from the database to get the computed values
        user.refresh_from_db()

        # Test bazi fields are populated
        self.assertIsNotNone(user.bazi_year, "Bazi year should not be None.")
        self.assertIsNotNone(user.bazi_month, "Bazi month should not be None.")
        self.assertIsNotNone(user.bazi_day, "Bazi day should not be None.")
        self.assertIsNotNone(user.zodiac_animal, "Zodiac animal should not be None.")

        # Test bazi format (should end with 年/月/日)
        self.assertTrue(user.bazi_year.endswith("年"), "Bazi year should end with '年'")
        self.assertTrue(user.bazi_month.endswith("月"), "Bazi month should end with '月'")
        self.assertTrue(user.bazi_day.endswith("日"), "Bazi day should end with '日'")

        # Test lunar birth time includes both gan and zhi
        self.assertTrue("時" in user.lunar_birth_time, "Lunar birth time should contain '時'")
        self.assertNotEqual(user.lunar_birth_time, "吉時", "Lunar birth time should not be default when time is provided")

    def test_get_complete_bazi_method(self):
        """
        Tests the get_complete_bazi method directly.
        """
        User = get_user_model()
        solar_date = date(2024, 5, 19)  # 甲辰年

        user = User(
            gregorian_birth_date=solar_date,
        )

        bazi_data = user.get_complete_bazi()

        self.assertIsNotNone(bazi_data, "Bazi data should not be None.")
        self.assertIn('year', bazi_data, "Bazi data should contain 'year'")
        self.assertIn('month', bazi_data, "Bazi data should contain 'month'")
        self.assertIn('day', bazi_data, "Bazi data should contain 'day'")
        self.assertIn('zodiac', bazi_data, "Bazi data should contain 'zodiac'")

        # Test specific values for 2024-05-19 (甲辰年)
        self.assertEqual(bazi_data['year'], "甲辰年", "Year should be Jia Chen (甲辰年)")
        self.assertEqual(bazi_data['zodiac'], "龙", "Zodiac animal for 2024 should be Dragon")

    def test_bazi_without_birth_date(self):
        """
        Tests that get_complete_bazi returns None when no birth date is provided.
        """
        User = get_user_model()

        user = User()

        bazi_data = user.get_complete_bazi()

        self.assertIsNone(bazi_data, "Bazi data should be None when no birth date is provided.")