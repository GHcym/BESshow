from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from epd_management.models import LanternWall, LanternPlayer
from epd_management.forms import LanternWallWithPlayersForm, LanternPlayerFormSet

class LanternWallUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_superuser(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        self.wall = LanternWall.objects.create(name='Test Wall', description='A wall for testing')
        self.player1 = LanternPlayer.objects.create(wall=self.wall, position=1, serial_number='CM20250000AA', is_enabled=True)
        self.player2 = LanternPlayer.objects.create(wall=self.wall, position=2, serial_number='CM20250000BB', is_enabled=False)

        self.update_url = reverse('epd_management:lantern_wall_update', args=[self.wall.id])

    def test_lantern_wall_update_view_get(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'epd_management/lantern_wall_form.html')
        self.assertIsInstance(response.context['form'], LanternWallWithPlayersForm)

    def test_lantern_wall_update_view_post_success(self):
        # Prepare POST data for updating the wall and its players
        # The formset requires specific prefixes and management form data
        post_data = {
            'name': 'Updated Test Wall',
            'description': 'Updated description for testing',
            'players-TOTAL_FORMS': '2',
            'players-INITIAL_FORMS': '2',
            'players-MIN_NUM_FORMS': '0',
            'players-MAX_NUM_FORMS': '1000',

            # Data for player1 (existing)
            f'players-0-id': str(self.player1.id),
            f'players-0-position': '1',
            f'players-0-serial_number': 'CM20250000AA', # No change
            f'players-0-is_enabled': 'on', # Change to enabled

            # Data for player2 (existing)
            f'players-1-id': str(self.player2.id),
            f'players-1-position': '2',
            f'players-1-serial_number': 'CM20250000CC', # Change serial number
            f'players-1-is_enabled': 'on', # Change to enabled
        }

        response = self.client.post(self.update_url, post_data)
        
        # Check for redirect, indicating success
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('epd_management:lantern_wall_list'))

        # Verify wall update
        self.wall.refresh_from_db()
        self.assertEqual(self.wall.name, 'Updated Test Wall')
        self.assertEqual(self.wall.description, 'Updated description for testing')

        # Verify player updates
        self.player1.refresh_from_db()
        self.assertTrue(self.player1.is_enabled)

        self.player2.refresh_from_db()
        self.assertEqual(self.player2.serial_number, 'CM20250000CC')
        self.assertTrue(self.player2.is_enabled)

    def test_lantern_wall_update_view_post_add_new_player(self):
        # Prepare POST data for adding a new player
        post_data = {
            'name': 'Test Wall',
            'description': 'A wall for testing',
            'players-TOTAL_FORMS': '3', # One new player
            'players-INITIAL_FORMS': '2',
            'players-MIN_NUM_FORMS': '0',
            'players-MAX_NUM_FORMS': '1000',

            # Data for player1 (existing)
            f'players-0-id': str(self.player1.id),
            f'players-0-position': '1',
            f'players-0-serial_number': 'CM20250000AA',
            f'players-0-is_enabled': 'on',

            # Data for player2 (existing)
            f'players-1-id': str(self.player2.id),
            f'players-1-position': '2',
            f'players-1-serial_number': 'CM20250000BB',
            f'players-1-is_enabled': 'on',

            # Data for new player (no id)
            f'players-2-position': '3',
            f'players-2-serial_number': 'CM20250000DD',
            f'players-2-is_enabled': 'on',
        }

        response = self.client.post(self.update_url, post_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('epd_management:lantern_wall_list'))

        # Verify new player was created
        new_player = LanternPlayer.objects.get(wall=self.wall, position=3)
        self.assertEqual(new_player.serial_number, 'CM20250000DD')
        self.assertTrue(new_player.is_enabled)

    def test_lantern_wall_update_view_post_delete_player(self):
        # Prepare POST data for deleting player2
        post_data = {
            'name': 'Test Wall',
            'description': 'A wall for testing',
            'players-TOTAL_FORMS': '2',
            'players-INITIAL_FORMS': '2',
            'players-MIN_NUM_FORMS': '0',
            'players-MAX_NUM_FORMS': '1000',

            # Data for player1 (existing)
            f'players-0-id': str(self.player1.id),
            f'players-0-position': '1',
            f'players-0-serial_number': 'CM20250000AA',
            f'players-0-is_enabled': 'on',

            # Data for player2 (existing) - marked for deletion
            f'players-1-id': str(self.player2.id),
            f'players-1-position': '2',
            f'players-1-serial_number': 'CM20250000BB',
            f'players-1-is_enabled': 'on',
            f'players-1-DELETE': 'on', # Mark for deletion
        }

        response = self.client.post(self.update_url, post_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('epd_management:lantern_wall_list'))

        # Verify player2 was deleted
        with self.assertRaises(LanternPlayer.DoesNotExist):
            LanternPlayer.objects.get(id=self.player2.id)
        
        # Verify player1 still exists
        self.player1.refresh_from_db()
        self.assertIsNotNone(self.player1)

    def test_lantern_wall_update_view_post_invalid_data(self):
        # Prepare POST data with invalid serial number for player1
        post_data = {
            'name': 'Updated Test Wall',
            'description': 'Updated description for testing',
            'players-TOTAL_FORMS': '2',
            'players-INITIAL_FORMS': '2',
            'players-MIN_NUM_FORMS': '0',
            'players-MAX_NUM_FORMS': '1000',

            # Data for player1 (existing) - invalid serial number
            f'players-0-id': str(self.player1.id),
            f'players-0-position': '1',
            f'players-0-serial_number': 'INVALID', # Invalid serial number
            f'players-0-is_enabled': 'on',

            # Data for player2 (existing)
            f'players-1-id': str(self.player2.id),
            f'players-1-position': '2',
            f'players-1-serial_number': 'CM20250000BB',
            f'players-1-is_enabled': 'on',
        }

        response = self.client.post(self.update_url, post_data)
        
        # Should not redirect, should render the form again with errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'epd_management/lantern_wall_form.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('Player ID格式錯誤', str(response.context['form'].errors))
