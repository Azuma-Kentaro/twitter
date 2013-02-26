#coding:utf_8
import urllib
import urllib.request
import urllib.parse
import hmac
import base64
import hashlib
import time
import random

consumer_key = 'QPo9yiumJcjZI2EvYX5w'
consumer_secret = 'Etoe6vyfNS3ktL5Pe46Hy9IzKCHDG0hsfKhfRUMMg'
oauth_token = '347236498-smKN3u3fDyP0459HLxQlxABDHfEmf3eRXjGGPER4'
oauth_token_secret = 'WdXkPUG7e3hW9HM8GCGCnpqDNK4fhm01VTcaPtOQnIc'


def init_params():
    return {"oauth_consumer_key":consumer_key,
            "oauth_token":oauth_token,
            "oauth_signature_method":'HMAC-SHA1',
            "oauth_timestamp":str(int(time.time())),
            "oauth_nonce":str(random.getrandbits(64)),
            "oauth_version":'1.0'
            }

def make_signature(method, url, oauth_params, extra_params):
    baseStringURI = url
    params = dict()
    params.update(oauth_params)
    params.update(extra_params)
    normalized_params = '&'.join(['%s=%s' % (urllib.parse.quote(key, '~'), urllib.parse.quote(val, '~')) for key, val in sorted(params.items())])
    signature_BaseString = '%s&%s&%s' % (method, urllib.parse.quote(baseStringURI, '~'), urllib.parse.quote(normalized_params, '~'))
    h = hmac.new(('%s&%s' % (urllib.parse.quote(consumer_secret, '~'), urllib.parse.quote(oauth_token_secret, '~'))).encode('utf_8'), signature_BaseString.encode('utf_8'), hashlib.sha1)
    signature = base64.b64encode(h.digest())
    return signature.decode('utf_8')

if __name__ == '__main__':
    url = 'http://api.twitter.com/1.1/statuses/update.json'
    extra_params = {'status':'縺翫＠縺ｾ縺'}

    req = urllib.request.Request(url, method='POST')
    oauth_params = init_params()
    
    oauth_params['oauth_signature'] = make_signature(req.get_method(), req.get_full_url(), oauth_params, extra_params)
    req.add_header('Authorization', 'OAuth %s' % (', '.join(['%s="%s"' % (key, urllib.parse.quote(val, '~')) for key, val in oauth_params.items()])))
    req.add_data('&'.join(['%s=%s' % (key, urllib.parse.quote(val, '~')) for key, val in extra_params.items()]).encode('utf_8'))
    
    res = urllib.request.urlopen(req)
    print(res.read())
