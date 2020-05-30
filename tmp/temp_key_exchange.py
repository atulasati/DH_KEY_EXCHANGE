import requests
import random
import json

API_BASE_URL = "https://shortrndexercise.singular.net/get-key"


class DiffieHellmanKeyExchange(object):
	def __init__(self, email):
		self.email = email
		self.p = None
		self.g = None
		self._set_shared_params()

	def _set_shared_params(self):
		res = self.call_api()
		if res:
			res = json.loads(res)
			self.p = int(res.get('p', 0))
			self.g = int(res.get('g', 0))
			self.A_public = int(res.get('A_public', 0))
		else:
			print ("could not set prime & generator")

	@staticmethod
	def generate_private_key():
		return random.randint(1,9)

	def call_api(self, public_key=None, shared_secret=None):
		params = {'email': self.email}

		if public_key:
			params['B_public'] = str(public_key)
		if shared_secret:
			params['solution'] = str(shared_secret)

		response = requests.get(
			url=API_BASE_URL, 
			params=params
		)
		if response.status_code == 200:
			return response.content
		else:
			print ("api call was failed!")
		return None

	def geenrate_pub_key(self, private_key, data=None):
		#sign algo
		if not data:
			data = self.g

		return (data ** private_key) % self.p

if __name__ == '__main__':
	key_exchange = DiffieHellmanKeyExchange(email='atulasati@gmail.com')

	A_private_key = DiffieHellmanKeyExchange.generate_private_key()
	B_private_key = DiffieHellmanKeyExchange.generate_private_key()

	A_public_key = key_exchange.A_public
	B_public_key = key_exchange.geenrate_pub_key(B_private_key)
	# print("B_public_key: ", B_public_key)

	B_shared_secret = key_exchange.geenrate_pub_key(B_private_key, A_public_key)
	# print("B_shared_secret: ", B_shared_secret)

	result = key_exchange.call_api(public_key=B_public_key, shared_secret=B_shared_secret)
	# print("\nresult:: \n \t", result)

	print ("done!")