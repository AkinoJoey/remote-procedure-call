import socket
import os
import math
import json

class Socket:

    def __init__(self):
        self.sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        self.server_address = '/tmp/socket_file'

    def accept(self):
        try:
            os.unlink(self.server_address)
        except FileNotFoundError:
            pass

        print('Starting up on {}'.format(self.server_address))
        self.sock.bind(self.server_address)

        self.sock.listen(1)
        connection, client_address = self.sock.accept()
        
        while True:
            data = connection.recv(4096)
            
            if not data:
                print('no data from', str(client_address))
                break

            try:
                all_request_data = json.loads(data)
                
                if len(all_request_data) == 0:
                    response_data = json.dumps(Error.inValidRequest)
                    connection.sendall(response_data.encode())
                    continue
                
                print("receving data from client:")
                print(*all_request_data, sep='\n')
                response = Response.serve(all_request_data)
                print()
                print("sending response:")
                print(*response, sep= '\n')
                response_data = json.dumps(response)
                connection.sendall(response_data.encode())
                
            except Exception:
                response_data = json.dumps(Error.inValidRequest)
                connection.sendall(response_data.encode())
            
class Response:
    
    def validateParamType(resultType,paramType):
        return resultType == paramType
    
    def serve(request):
        resultList = []
        
        for currenData in request:
            
            floor = lambda x : round(x)
            nroot = lambda n, x : int(math.pow(x, 1/n))
            reverse = lambda s: s[::-1]
            validAnagram = lambda str1, str2 : sorted(str1) == sorted(str2)
            sort = lambda strArr: sorted(strArr)
            
            try:
                method = currenData['method']
                params = currenData['params']
                param_types = currenData['param_types']
                id = currenData['id']
            
            
                if method == 'floor':
                    if type(params) != float or param_types != 'double':
                        resultList.append(Error.inValidParamTypes)
                        continue
                    
                    result = floor(params)
                    result_type = 'int' 
                    
                elif method == 'nroot':
                    if type(params[0]) != int or type(params[1]) != int or param_types[0] != 'int' or param_types[1] != 'int':
                        resultList.append(Error.inValidParamTypes)
                        continue
                    
                    result = nroot(params[1],params[0])
                    result_type = 'int'
                    
                elif method == 'reverse':
                    if type(params) != str or param_types != 'string':
                        resultList.append(Error.inValidParamTypes)
                        continue
                    
                    result = reverse(params)
                    result_type = 'string'
                    
                elif method == 'validAnagram':
                    if type(params[0]) != str or type(params[1]) != str or param_types[0] != 'string' or param_types[1] != 'string':
                        resultList.append(Error.inValidParamTypes)
                        continue
                    
                    result = validAnagram(params[0],params[1])
                    result_type = 'Boolean'
                    
                elif method == 'sort':
                    if type(params) != list or  param_types != "string[]":
                        resultList.append(Error.inValidParamTypes)
                        continue
                    
                    result = sort(params)
                    result_type = 'string'
                else:
                    resultList.append(Error.methodNotFound)
                    continue
                    
                response = {
                'result': result,
                'result_type': result_type,
                'id': id
                }
            
                resultList.append(response)
                
            except Exception:
                resultList.append(Error.inValidRequest)
                
        
        return resultList

        
class Error:
    methodNotFound = {"message":"Method not found"}
    inValidRequest = {"message":"Invalid request"}
    inValidParamTypes = {"message":"Invalid param types"}

class Main:
    sock = Socket()
    sock.accept()


if __name__ == '__main__':
    Main()

