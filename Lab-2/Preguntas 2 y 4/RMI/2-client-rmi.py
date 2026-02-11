import xmlrpc.client

# Replace with the Server's IP address
proxy = xmlrpc.client.ServerProxy("http://172.23.208.66:12000/RPC2")

# Complex numbers data (Real and Imaginary parts)
num1 = {'re': 10, 'im': 5}
num2 = {'re': 2, 'im': -3}

try:
    # Call the remote method 'compute' for different operations
    print(f"Numbers: ({num1['re']}+{num1['im']}j) and ({num2['re']}+{num2['im']}j)\n")

    add_result = proxy.compute(num1, num2, 'add')
    print("Addition Result:", add_result)

    sub_result = proxy.compute(num1, num2, 'sub')
    print("Subtraction Result:", sub_result)

    prod_result = proxy.compute(num1, num2, 'prod')
    print("Multiplication Result:", prod_result)

    div_result = proxy.compute(num1, num2, 'div')
    print("Division Result:", div_result)

except ConnectionRefusedError:
    print("Error: Could not connect to the server. Check the IP and Port.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")