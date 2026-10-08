import requests
import hashlib
import sys


def request_api_data(query_char = str):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url=url)
    if res.status_code != 200:
        raise RuntimeError(f' Please check the api again as we are facing {res.status_code}')
    return res

def get_password_leaks_count(hash, hash_to_check):
    hash = (line.split(':') for line in hash.text.splitlines())
    for h, count in hash:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sh1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_char, tail = sh1password[:5], sh1password[5:]
    response = request_api_data(first_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password=password)
        if count:
            print(f'{password} was found !! {count} time. Please change the password')
        else:
            print(f'{password} is safe ;)')
    return 'done !'

main(sys.argv[1:])