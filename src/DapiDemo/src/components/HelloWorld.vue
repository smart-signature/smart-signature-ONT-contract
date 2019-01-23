<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.hello {
  width: 800px;
  margin: 0 auto;
}
.header-container {
  display: flex;
  flex-direction: row;
}
.header-container div {
  flex-basis: 50%;
  text-align: center;
  border-bottom:2px solid #dddddd;
}
.function-item {
  display:flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  margin:10px 0;
}
.function-item div {
  width:40%;
}

.function-item code {
  width:calc(60% - 80px);
  padding:0 15px;
  text-align: left;
}
</style>
<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div class="header-container">
      <div>Function name</div>
      <div>Response</div>
    </div>
    <div class="function-item" v-for="(f, index) of functions" :key="index" >
      <div>{{f.function}}</div>
      <button @click="handleRun(f.function, index)">Run</button>
      <code>{{f.response}}</code>
    </div>
    
  </div>
</template>

<script>
import {client} from 'ontology-dapi'
const Ont = require('ontology-ts-sdk')

const contract = '16edbe366d1337eb510c2ff61099424c94aeef02';
const gasLimit = 30000;
const gasPrice = 500;
const privateKey = new Ont.Crypto.PrivateKey('274b0b664d9c1e993c1d62a42f78ba84c379e332aa1d050ce9c1840820acee8b');
const password = '123456';
const account = Ont.Account.create(privateKey, password, '');
const payer = account.address;

export default {
  name: 'HelloWorld',
  async mounted() {
    try { // get provider
        const provider = await client.api.provider.getProvider();
        console.log('onGetProvider: ' + JSON.stringify(provider));
        this.provider = provider;
      } catch (e) {
        console.log('No dAPI provider istalled.');
        alert('No provider installed. Please install the Cyano Wallet from Chrome web store.')
        return null;
      }
  },
  data () {
    return {
      msg: 'Dapi demo',
      functions: [
        { function: 'name', response: ''},
        { function: 'hello', response: ''},
        { function: 'testHello', response: ''},
        { function: 'testList', response: ''},
        { function: 'testListAndStr', response: ''},
        { function: 'testStructList', response: ''},
        { function: 'testStructListAndStr', response: ''},
        { function: 'testMap', response: ''},
        { function: 'testGetMap', response: ''},
        { function: 'testMapInMap', response: ''},
        { function: 'testGetMapInMap', response: ''},
        { function: 'transferMulti', response: ''}
      ]
    }
  },
  methods: {
    async handleRun(funcName, index){
      const method = this.functions[index].function
      let parameters, params, result;
      switch (funcName) {
        case 'name':
          parameters = []
          params = {
            contract,
            method,
            parameters,
            gasPrice,
            gasLimit
          }
         result = await this.scInvoke(params, true);
          this.functions[index].response = result;
          break;

          case 'hello':
          parameters = [
            new Ont.Parameter('msg', Ont.ParameterType.String, 'hello world')
          ]
          params = {
            contract,
            method,
            parameters,
            gasPrice,
            gasLimit
          }
          result = await this.scInvoke(params, true);
          this.functions[index].response = result;
          break;

          case 'testHello':
          const address = new Ont.Crypto.Address('AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p');
          const addrByteArr = address.serialize();
          parameters = [
            new Ont.Parameter('msgBool', Ont.ParameterType.Bool, true),
            new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100),
            new Ont.Parameter('msgByteArray', Ont.ParameterType.ByteArray, 'aabb'),
            new Ont.Parameter('msgStr', Ont.ParameterType.String, 'test'),
            new Ont.Parameter('msgAddress', Ont.ParameterType.ByteArray, addrByteArr) 
          ]
          params = {
            contract,
            method,
            parameters,
            gasPrice,
            gasLimit
          }
          result = await this.scInvoke(params, true);
          this.functions[index].response = result;
          break;

          case 'testList':
          parameters = [
            new Ont.Parameter('msgList', Ont.ParameterType.Array, [
                new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100),
                new Ont.Parameter('msgStr', Ont.ParameterType.String, 'test'),
            ])
          ]
          params = {
            contract,
            method,
            parameters,
            gasPrice,
            gasLimit
          }
          result = await this.scInvoke(params, true);
          this.functions[index].response = result;
          break;

          case 'testListAndStr':
          parameters = [
            new Ont.Parameter('msgList', Ont.ParameterType.Array, [
                new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100),
                new Ont.Parameter('msgStr', Ont.ParameterType.String, 'test'),
            ]),
            new Ont.Parameter('msgStr', Ont.ParameterType.String, 'hello'),
          ]
          params = {
            contract,
            method,
            parameters,
            gasPrice,
            gasLimit
          }
          result = await this.scInvoke(params, true);
          this.functions[index].response = result;
          break;

          case 'testStructList':
          parameters = [
            new Ont.Parameter('msgList', Ont.ParameterType.Array, [
                new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100),
                new Ont.Parameter('msgStr', Ont.ParameterType.String, 'test'),
            ])
          ]
          params = {
            contract,
            method,
            parameters,
            gasPrice,
            gasLimit
          }
          result = await this.scInvoke(params, true);
          this.functions[index].response = result;
          break;

          case 'testStructListAndStr':
          parameters = [
            new Ont.Parameter('msgList', Ont.ParameterType.Array, [
                new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100),
                new Ont.Parameter('msgStr', Ont.ParameterType.String, 'test'),
            ]),
            new Ont.Parameter('msgStr', Ont.ParameterType.String, 'hello'),
          ]
          params = {
            contract,
            method,
            parameters,
            gasPrice,
            gasLimit
          }
          result = await this.scInvoke(params, true);
          this.functions[index].response = result;
          break;

          case 'testMap':
          parameters = [
            new Ont.Parameter('map ', Ont.ParameterType.Map, {
                'key': new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100),
            })
          ]
          params = {
            contract,
            method,
            parameters,
            gasPrice,
            gasLimit
          }
          result = await this.scInvoke(params, false);
          this.functions[index].response = result;
          break;

          case 'testGetMap':
          parameters = [
            new Ont.Parameter('key ', Ont.ParameterType.String, 'key')
          ]
          params = {
            contract,
            method,
            parameters,
            gasPrice,
            gasLimit
          }
          result = await this.scInvoke(params, true);
          this.functions[index].response = result;
          break;

          case 'testMapInMap':
          parameters = [
            new Ont.Parameter('map1', Ont.ParameterType.Map, {
                "key": new Ont.Parameter('map2', Ont.ParameterType.Map,{
                    "key2": new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100)
                })
            })
          ]
          params = {
            contract,
            method,
            parameters,
            gasPrice,
            gasLimit
          }
          result = await this.scInvoke(params, false);
          this.functions[index].response = result;
          break;

           case 'testGetMapInMap':
          parameters = [
            new Ont.Parameter('key', Ont.ParameterType.String, 'key2')
          ]
          params = {
            contract,
            method,
            parameters,
            gasPrice,
            gasLimit
          }
          result = await this.scInvoke(params, true);
          this.functions[index].response = result;
          break;

           case 'transferMulti':
           const to = new Ont.Crypto.Address('AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p');
            const toByteArr = to.serialize();
          parameters = [
            new Ont.Parameter('msgList', Ont.ParameterType.Array,[
                new Ont.Parameter('msgList', Ont.ParameterType.Array, [
                    new Ont.Parameter('from', Ont.ParameterType.ByteArray, payer.serialize()),
                    new Ont.Parameter('to', Ont.ParameterType.ByteArray, toByteArr),
                    new Ont.Parameter('amount', Ont.ParameterType.Integer, 100) 
                ])
                
            ]) 
          ]
          params = {
            contract,
            method,
            parameters,
            gasPrice,
            gasLimit
          }
          result = await this.scInvoke(params, false);
          this.functions[index].response = result;
          break;
      
        default:
          break;
      }
    },
    async scInvoke(params, preExec) {
      try {
        let result;
        if(preExec) {
           result = await client.api.smartContract.invokeRead(params);       
        } else {
           result = await client.api.smartContract.invoke(params);
        }
        console.log('onScCall finished, result:' + JSON.stringify(result));        
        return result;
      } catch (e) {
        console.log('onScCall error:', e);
        alert('Some error happens. Please try later.' + e)
        return null;
      }
    }
  }
}
</script>


