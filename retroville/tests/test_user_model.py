

#
# class CreateUserTest(APITestCase):
#     def setUp(self):
#         self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
#         self.client.login(username='john', password='johnpassword')
#         self.data = {'username': 'mike', 'first_name': 'Mike', 'last_name': 'Tyson'}
#
#     def test_can_create_user(self):
#         response = self.client.post(reverse('user-list'), self.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
