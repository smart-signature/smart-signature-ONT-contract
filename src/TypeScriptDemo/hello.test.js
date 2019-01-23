const Ont = require('ontology-ts-sdk');

describe('test contract', () => {
    const privateKey = new Ont.Crypto.PrivateKey('274b0b664d9c1e993c1d62a42f78ba84c379e332aa1d050ce9c1840820acee8b');
    const password = '123456';
    const account = Ont.Account.create(privateKey, password, '');
    const payer = account.address;
    const contract = Ont.utils.reverseHex('16edbe366d1337eb510c2ff61099424c94aeef02');

    //Use TestNet. Can also use RestClient or RpcClient here.
    const client = new Ont.WebsocketClient();

    const contractAddr = new Ont.Crypto.Address(contract);

    beforeAll(() => {

    })

    test('name', async () => {
        const method = 'name';
        const tx = Ont.TransactionBuilder.makeInvokeTransaction(method, [], contractAddr, '500', '30000');
        const res = await client.sendRawTransaction(tx.serialize(), true); // preExec
        console.log(JSON.stringify(res));
        expect(res.Error).toBe(0);
    })
    test('hello', async () => {
        const method = 'hello'
        const param = new Ont.Parameter('msg', Ont.ParameterType.String, 'hello world')
        const tx = Ont.TransactionBuilder.makeInvokeTransaction(method, [param], contractAddr, '500', '30000');
        const res = await client.sendRawTransaction(tx.serialize(), true); // preExec
        console.log(JSON.stringify(res));
        expect(res.Error).toBe(0);
    });

    test('testHello', async () => {
        const method = 'testHello'
        const address = new Ont.Crypto.Address('AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p');
        const addrByteArr = address.serialize();
        const params = [
            new Ont.Parameter('msgBool', Ont.ParameterType.Bool, true),
            new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100),
            new Ont.Parameter('msgByteArray', Ont.ParameterType.ByteArray, 'aabb'),
            new Ont.Parameter('msgStr', Ont.ParameterType.String, 'test'),
            new Ont.Parameter('msgAddress', Ont.ParameterType.ByteArray, addrByteArr)            
        ]
        const tx = Ont.TransactionBuilder.makeInvokeTransaction(method, params, contractAddr, '500', '30000');
        const res = await client.sendRawTransaction(tx.serialize(), true); // preExec
        console.log(JSON.stringify(res));
        expect(res.Error).toBe(0);
    });

    test('testList', async () => {
        const method = 'testList'
        const params = [
            new Ont.Parameter('msgList', Ont.ParameterType.Array, [
                new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100),
                new Ont.Parameter('msgStr', Ont.ParameterType.String, 'test'),
            ])
        ]
        const tx = Ont.TransactionBuilder.makeInvokeTransaction(method, params, contractAddr, '500', '30000');
        const res = await client.sendRawTransaction(tx.serialize(), true); // preExec
        console.log(JSON.stringify(res));
        expect(res.Error).toBe(0);
    });

    test('testListAndStr', async () => {
        const method = 'testListAndStr'
        const params = [
            new Ont.Parameter('msgList', Ont.ParameterType.Array, [
                new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100),
                new Ont.Parameter('msgStr', Ont.ParameterType.String, 'test'),
            ]),
            new Ont.Parameter('msgStr', Ont.ParameterType.String, 'hello'),
        ]
        const tx = Ont.TransactionBuilder.makeInvokeTransaction(method, params, contractAddr, '500', '30000');
        const res = await client.sendRawTransaction(tx.serialize(), true); // preExec
        console.log(JSON.stringify(res));
        expect(res.Error).toBe(0);
    });

    test('testStructList', async () => { // Use array for StructList
        const method = 'testStructList'
        const params = [
            new Ont.Parameter('msgList', Ont.ParameterType.Array, [
                new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100),
                new Ont.Parameter('msgStr', Ont.ParameterType.String, 'test'),
            ])
        ]
        const tx = Ont.TransactionBuilder.makeInvokeTransaction(method, params, contractAddr, '500', '30000');
        const res = await client.sendRawTransaction(tx.serialize(), true); // preExec
        console.log(JSON.stringify(res));
        expect(res.Error).toBe(0);
    });

    test('testStructListAndStr', async () => { // Use array for StructList
        const method = 'testStructListAndStr'
        const params = [
            new Ont.Parameter('msgList', Ont.ParameterType.Array, [
                new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100),
                new Ont.Parameter('msgStr', Ont.ParameterType.String, 'test'),
            ]),
            new Ont.Parameter('msgStr', Ont.ParameterType.String, 'hello'),
        ]
        const tx = Ont.TransactionBuilder.makeInvokeTransaction(method, params, contractAddr, '500', '30000');
        const res = await client.sendRawTransaction(tx.serialize(), true); // preExec
        console.log(JSON.stringify(res));
        expect(res.Error).toBe(0);
    });

    test('testMap', async () => { 
        const method = 'testMap'
        const params = [
            new Ont.Parameter('map ', Ont.ParameterType.Map, {
                'key': new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100),
            })
        ]
        const tx = Ont.TransactionBuilder.makeInvokeTransaction(method, params, contractAddr, '500', '30000', payer);
        Ont.TransactionBuilder.signTransaction(tx, privateKey);
        const res = await client.sendRawTransaction(tx.serialize(), false);
        console.log(JSON.stringify(res));
        expect(res.Error).toBe(0);
    });

    test('testGetMap', async () => {
        const method = 'testGetMap'
        const params = [
            new Ont.Parameter('key ', Ont.ParameterType.String, 'key')
        ]
        const tx = Ont.TransactionBuilder.makeInvokeTransaction(method, params, contractAddr, '500', '30000');
        const res = await client.sendRawTransaction(tx.serialize(), true); // preExec
        console.log(JSON.stringify(res));
        expect(res.Error).toBe(0);
    });

    test('testMapInMap', async () => {
        const method = 'testMapInMap'
        const params = [
            new Ont.Parameter('map1', Ont.ParameterType.Map, {
                "key": new Ont.Parameter('map2', Ont.ParameterType.Map,{
                    "key2": new Ont.Parameter('msgInt', Ont.ParameterType.Integer, 100)
                })
            })
        ]
        const tx = Ont.TransactionBuilder.makeInvokeTransaction(method, params, contractAddr, '500', '30000', payer);
        Ont.TransactionBuilder.signTransaction(tx, privateKey);
        const res = await client.sendRawTransaction(tx.serialize(), false); // preExec
        console.log(JSON.stringify(res));
        expect(res.Error).toBe(0);
    });

    test('testGetMapInMap', async () => {
        const method = 'testGetMapInMap'
        const params = [
            new Ont.Parameter('key', Ont.ParameterType.String, 'key2')
        ]
        const tx = Ont.TransactionBuilder.makeInvokeTransaction(method, params, contractAddr, '500', '30000');
        const res = await client.sendRawTransaction(tx.serialize(), false, false); // preExec;
        console.log(JSON.stringify(res));
        expect(res.Error).toBe(0);
    }, 6000);

    test('transferMulti', async () => {
        const method = 'transferMulti'
        const to = new Ont.Crypto.Address('AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p');
        const toByteArr = to.serialize();
        const params = [
            new Ont.Parameter('msgList', Ont.ParameterType.Array,[
                new Ont.Parameter('msgList', Ont.ParameterType.Array, [
                    new Ont.Parameter('from', Ont.ParameterType.ByteArray, payer.serialize()),
                    new Ont.Parameter('to', Ont.ParameterType.ByteArray, toByteArr),
                    new Ont.Parameter('amount', Ont.ParameterType.Integer, 100) 
                ])
                
            ])         
        ]
        const tx = Ont.TransactionBuilder.makeInvokeTransaction(method, params, contractAddr, '500', '30000', payer);
        Ont.TransactionBuilder.signTransaction(tx, privateKey);
        const res = await client.sendRawTransaction(tx.serialize(), true, false); // preExec;
        console.log(JSON.stringify(res));
        expect(res.Error).toBe(0);
    }, 6000);
})
