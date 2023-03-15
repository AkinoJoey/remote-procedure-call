const net = require('net');

class SocketClient{

  constructor(server_address){
    this.client = new net.Socket();
    this.server_address = server_address;
    this.client.setTimeout(2000);
    this.client.on("data",this.receveResponse.bind(this));
    this.client.on("timeout",this.handleTimeout.bind(this));
    this.client.on("error",this.handleError.bind(this));
  }

  connect(){
    console.log('connecting to server');
    try{
      this.client.connect(server_address);
    }catch(err){
      console.log(err);
      process.exit(1);
    }
  }

  sentData(data){
    const jsonData = JSON.stringify(data);
    this.client.write(jsonData);
    console.log("sending data:")
    console.log(data)
  }

  receveResponse(response){
    console.log()
      console.log("receving response from sever:")
      console.log()
      console.log(JSON.parse(response))
  }

  handleTimeout(){
    console.log('Socket timeout, ending listening for server messages');
    this.client.destroy();
  }

  handleError(error) {
      console.error('Socket error:', error);
  }
}


const data = [
  {"method": "floor", "params": 10.5, "param_types": "double","id": 1},
  {"method": "nroot", "params": [6,132], "param_types": ["int","int"],"id": 2},
  {"method": "reverse", "params": "testString", "param_types": "string","id": 3},
  {"method": "validAnagram", "params": ["test","estt"], "param_types": ["string","string"],"id": 4},
  {"method": "sort", "params": ["Banana","Apple","Cider","Anagram"], "param_types": "string[]","id": 5}
]

const server_address = '/tmp/socket_file';

const client = new SocketClient(server_address);
client.connect();
client.sentData(data);
