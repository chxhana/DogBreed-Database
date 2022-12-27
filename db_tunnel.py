from sshtunnel import SSHTunnelForwarder

DB_HOST = 'cs.westminstercollege.edu'
DB_SSH_PORT = 2322
DB_SSH_USER = 'student'
DB_PORT = 3306

# Private RSA key used for the ssh connection
PRIVATE_KEY = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIAKECpzSOaxE0IesSj0VSEK4bKTP9bvn7nsALuqw1dmqoAoGCCqGSM49
AwEHoUQDQgAE/SJqcz4fi52Pad9aC4mZSGZ8oWnyba7qiIHr304C25b2FfMZNGJG
s6/k7cTNhbn6L1ggEceH4X9Ojd7uu5OocA==
-----END EC PRIVATE KEY-----

"""

class DatabaseTunnel:
    
    def __init__(self):
        pass
    
    def open(self):
        self.tunnel = SSHTunnelForwarder(
            DB_HOST,
            ssh_username=DB_SSH_USER,
            ssh_port=DB_SSH_PORT,
            ssh_pkey=self.getKeyfile(),
            remote_bind_address=('127.0.0.1', DB_PORT)
        )
        
        self.tunnel.start()
    
    def close(self):
        self.tunnel.stop()
        
    def getForwardedPort(self):
        return self.tunnel.local_bind_port
    
    def getKeyfile(self):
        import os.path
        keyfile = 'id_ecdsa.cmpt307.tunnel'
        if not os.path.isfile(keyfile):
            with open(keyfile, 'w') as f:
                print(PRIVATE_KEY, file=f, end='')
        return keyfile
    
    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, *args):
        self.close()
