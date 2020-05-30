import requests
import random
import json

API_BASE_URL = "https://shortrndexercise.singular.net/get-key?email=atulasati@gmail.com&"

def algo_calculation(data, key, prime):
    #  g**p % prime
    result = 1
    while key:
        if key & 1:
            result = result * data % prime
        key >>= 1
        data = data * data % prime

    return result

def gen_private_key():
    return random.randrange(9**10, 10**11)

def call_api_n_get_params(**kw):
    params = ""
    if kw:
        params = "&".join(["%s=%s" %(k, w) for k, w in kw.items()])

    response = requests.get(url=API_BASE_URL+params)
    if response.status_code == 200:
        response = json.loads(response.content)
        if response.get('p'):
            return {
                "p": int(response['p']),
                "g": int(response['g']),
                "a_pub": int(response['A_public'])
            }
        return response
    return {}

def check_key_exchange():
    try:
        api_params = call_api_n_get_params()
        p = api_params.get('p', 0)
        g = api_params.get('g', 0)

        a_private_key = gen_private_key()
        b_private_key = gen_private_key()

        a_public_key = api_params.get('a_pub', 0)
        b_public_key = algo_calculation(g, b_private_key, p)
        print("\tbob_public_key: ", b_public_key)
        
        b_shared_secret = algo_calculation(a_public_key, b_private_key, p)
        print("\tbob_shared_secret: ", b_shared_secret)

        print("\nstart sharing... ")
        # response = call_api_n_get_params(B_public=b_public_key, solution=b_shared_secret)
        url = "https://shortrndexercise.singular.net/submit?email=atulasati@gmail.com&B_public=%s&solution=%s" % (b_public_key, b_shared_secret)
        response = requests.get(url)
        result = json.loads(response.content)
        print("  response: \n\t", result)
        if result.get('success'):
            return True
        return False
    except Exception as err:
        print (err)

if __name__ == '__main__':
    print("start processing....")
    check_key_exchange()
