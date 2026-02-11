import xmlrpc.client

# Create a client proxy
proxy = xmlrpc.client.ServerProxy("http://172.23.208.66:12000/RPC2")

# Call the remote method 'add'
result = proxy.add(5, 3)
print("5 + 3 =", result)

