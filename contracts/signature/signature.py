from boa.interop.Ontology.Runtime import AddressToBase58, Base58ToAddress
from boa.interop.Ontology.Native import Invoke
from boa.interop.System.Action import RegisterAction
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash
from boa.interop.System.Storage import Delete, Get, GetContext, Put
from boa.interop.System.Runtime import CheckWitness, Notify, Serialize, Deserialize
from boa.builtins import concat, ToScriptHash, append, state
# punica compile --contracts signature.py --local true

# Ont contract
OntContract = Base58ToAddress('AFmseVrdL9f9oyCzZefL9tG6UbvhUMqNMV')

# contract INFO CONSTANTS
selfContractAddress = GetExecutingScriptHash()

DEPLOYER = Base58ToAddress('AJKNkXMm9FpqwwvKzSq9B76CoTNSp9GVwh')
PUBLISHER = Base58ToAddress('AJKNkXMm9FpqwwvKzSq9B76CoTNSp9GVwh')

################################################################################
# STORAGE KEY CONSTANT
# Belows are storage key for some variable token information.

DEPLOYED_KEY = 'DEPLOYED_SPKZ03'
OWNER_KEY = '___OWNER_SPKZ03'

################################################################################
# STORAGE KEY PREFIX
# Since all data are stored in the key-value storage, the data need to be
# classified by key prefix. All key prefixes length must be the same.

OWN_PREFIX = '_____own_spkz03'

PLAYER_PREFIX = b'\x01'
SIGN_PREFIX = b'\x02'

################################################################################
def Main(operation, args):
    """
    :param operation:
    :param args:
    :return:
    """
    # 'init' has to be invokded first after deploying the contract to store the necessary and important info into the blockchain
    if operation == 'init':
        return init()
    if operation == 'publish':
        if len(args) != 7:
            return False
        else:
            acct = args[0]
            # id author fissionFactor ipfs_hash public_key signature
            return publish(acct, [args[1], args[2], args[3], args[4], args[5], args[6]]);
    if operation == 'createShare':
        if len(args) != 3 or len(args) != 4:
            return False
        else:
            owner = args[0]
            signId = args[1]
            income = args[2]
            if len(args) == 4:
                referral = args[4]
                return createShare(owner, signId, income, referral)
            else:
                return createShare(owner, signId, income, '')

def init():
    """
    Constructor of this contract. Only deployer hard-coded can call this function
    and cannot call this function after called once.
    Followings are initialization list for SS.
    """
    RequireWitness(DEPLOYER)                           # only can be initialized by deployer
    Require(not Get(GetContext(), DEPLOYED_KEY))                # only can deploy once
    #if is_deployed:
    #    Notify("Already initialized!")
    #    return False

    # disable to deploy again
    saveData(DEPLOYED_KEY, 1)

    # the first owner is the deployer
    # can transfer ownership to other by calling `TransferOwner` function
    saveData(OWNER_KEY, DEPLOYER)
    return True


def publish(acct, rawSign):
    signId = rawSign[0]
    author = rawSign[1]
    fissionFactor = rawSign[2]
    ipfsHash = rawSign[3]
    publicKey = rawSign[4]
    signature = rawSign[5]

    RequireScriptHash(acct)    
    RequireScriptHash(author)
    RequireWitness(acct)
    Require(acct == PUBLISHER)

    saveSign(signId, [author, fissionFactor, ipfsHash, publicKey, signature])
    
    Notify(concat(signId, " publish success."))
    #PublishEvent(sign)
    return True

def createShare(owner, signId, income, referral):
    # owner
    RequireScriptHash(owner)
    RequireWitness(owner)
    ownerPInfo = GetPlayerInfo(owner) 

    # sign
    sSign = Get(GetContext(), concat(SIGN_PREFIX, signId))
    Require(sSign)
    sign = Deserialize(sSign)
    author = sign[0]
    fissionFactor = sign[1]
    authorPInfo = GetPlayerInfo(author)

    # owner sign share
    Require(not signId in ownerPInfo[2])

    param = state(Base58ToAddress(owner), selfContractAddress, income)
    res = Invoke(0, OntContract, "transfer", [param])
    if res != b'\x01':
        Notify("buy error.")
        return False

    #paramContract = state(Base58ToAddress(fromAcc), selfContractAddress, 1)
    #resContract = Invoke(0, OntContract, 'transfer', [paramContract])
    income = 0
    if referral != '':
        RequireScriptHash(referral)
        if referral != owner:
            referralPInfo = GetPlayerInfo(referral)
            quota = referralPInfo[2][signId]
            if quota:
                delta = quota if quota < income else income
                SubQuota(referral, referralPInfo, signId, delta)
                AddShareIncome(referral, referralPInfo, delta)
                income -= delta
                
    ownerPInfo[2][signId] = Div(Mul(income, fissionFactor), 1000)
    savePlayer(owner, ownerPInfo)
    AddSignIncome(author, authorPInfo, income)
    Notify(concat(owner, " create a share success."))
    return True

################################################################################
def SubQuota(ownerAcct, ownerInfo, signId, quantity):
    ownerInfo[2][signId] = Sub(ownerInfo[2][signId], quantity)
    savePlayer(ownerAcct, ownerInfo)

def AddShareIncome(ownerAcct, ownerInfo, quantity):
    ownerInfo[0] = Add(ownerInfo[0], quantity)
    savePlayer(ownerAcct, ownerInfo)

def AddSignIncome(ownerAcct, ownerInfo, quantity):
    ownerInfo[1] = Add(ownerInfo[1], quantity)
    savePlayer(ownerAcct, ownerInfo)

def GetPlayerInfo(acct):
    sp = Get(GetContext(), concat(PLAYER_PREFIX, acct)) 
    return Deserialize(sp) if sp else newPlayerInfo()

def newPlayerInfo(): # shareIncome, signIncome, shares
   return [0, 0, {}]

def saveSign(signId, signData):
    saveData(concat(SIGN_PREFIX, signId), Serialize(signData))

def savePlayer(playerAcct, playerData):
    saveData(concat(PLAYER_PREFIX, playerAcct), Serialize(playerData))

def saveData(key, value):
    Put(GetContext(), key, value)

################################################################################
def Require(condition):
	"""
	If condition is not satisfied, return false
	:param condition: required condition
	:return: True or false
	"""
	if not condition:
		Revert()
	return True

def RequireScriptHash(key):
    """
    Checks the bytearray parameter is script hash or not. Script Hash
    length should be equal to 20.
    :param key: bytearray parameter to check script hash format.
    :return: True if script hash or revert the transaction.
    """
    Require(len(key) == 20)
    return True

def RequireWitness(witness):
	"""
	Checks the transaction sender is equal to the witness. If not
	satisfying, revert the transaction.
	:param witness: required transaction sender
	:return: True if transaction sender or revert the transaction.
	"""
	Require(CheckWitness(witness))
	return True

def Add(a, b):
	"""
	Adds two numbers, throws on overflow.
	"""
	c = a + b
	Require(c >= a)
	return c

def Sub(a, b):
	"""
	Substracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
	"""
	Require(a>=b)
	return a-b

def Mul(a, b):
	"""
	Multiplies two numbers, throws on overflow.
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
	"""
	if a == 0:
		return 0
	c = a * b
	Require(c / a == b)
	return c

def Div(a, b):
	"""
	Integer division of two numbers, truncating the quotient.
	"""
	Require(b > 0)
	c = a / b
	return c

def Revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception(0xF1F1F2F2F3F3F4F4)
