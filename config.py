TOKEN = '322979405:AAFV6DsxbxK5obMxVfk5skYVD8QQQNPkwwU'

DB_CHAT_NAME = 'chat'
DB_INVITE_NAME = 'invite'


WEBHOOK_HOST = '89.223.31.83'
WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = 'cert/webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = 'cert/webhook_pkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)
