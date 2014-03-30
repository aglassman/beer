from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from beer_api.models import *

class TestGlassTypePost(APITestCase):
	
	def test_auth_fail(self):
		url = '/glass_types/'
		data = {
		    'glass_type': 'Mug', 
		    'description': 'A cup with a handle.'
		}
		response = self.client.post(url,data,format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(response.data['detail'], 
			'Authentication credentials were not provided.')
	
	def test_auth_pass(self):
		user = User.objects.create_user('test','test@test.com','testpass')
		self.client.login(username='test',password='testpass')
		url = '/glass_types/'
		data = {
		    'glass_type': 'Mug', 
		    'description': 'A cup with a handle.'
		}
		response = self.client.post(url,data,format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		response = self.client.get('/glass_types/1/')
		self.assertEqual(response.data['glass_type'],data['glass_type'])
		self.assertEqual(response.data['description'],data['description'])
		
