from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('0.0.0.0', 12000),
                         requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Function to compute complex number operations
    def compute_complex(c1, c2, op):
        try:
            # Reconstruct complex numbers: z = real + imag*j
            z1 = complex(c1['re'], c1['im'])
            z2 = complex(c2['re'], c2['im'])
            
            if op == 'add': 
                res = z1 + z2
            elif op == 'sub': 
                res = z1 - z2
            elif op == 'prod': 
                res = z1 * z2
            elif op == 'div': 
                if z2 == 0:
                    return "Error: Division by zero"
                res = z1 / z2
            else: 
                return "Error: Invalid operation"
            
            # Return as a dictionary for XML-RPC compatibility
            return {'re': res.real, 'im': res.imag}
        except Exception as e:
            return f"Server-side error: {str(e)}"

    server.register_function(compute_complex, 'compute')

    # Run the server's main loop
    print("Complex Number Manager is listening on port 12000...")
    server.serve_forever()