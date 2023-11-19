from pycardano import key, HDWallet, Address, Network, PaymentSigningKey, PaymentVerificationKey, StakeSigningKey, StakeVerificationKey


def generateWallet(quantity=1, network_id=1, verbose=False):

  if verbose: print('Generating wallet credentials...')
  credentials = []

  for wallet_num in range(0, quantity):  
    # Set up network
    if network_id == 0:
      network = Network.PREVIEW
    else:
      network = Network.MAINNET
      
    # Generate a new mnemonic phrase
    mnemonic = HDWallet.generate_mnemonic()

    # Create a new HDWallet from the mnemonic phrase
    hdWallet = HDWallet.from_mnemonic(mnemonic)

    # Derive the same payment key from the mnemonic phrase
    payment_KeyPath = hdWallet.derive_from_path("m/1852'/1815'/0'/0/0")
    payment_PubKey = payment_KeyPath.public_key
    
    # Derive the payment verification key from the payment key
    payment_vkey = key.PaymentExtendedVerificationKey(payment_PubKey)

    # Generate the address from the payment verification key
    address = Address(payment_part = payment_vkey.hash(), network = network)

    if verbose: print('Generated wallet at address: {}'.format(address))
    
    # Add credentials to list
    credentials.append({
      'address': str(address),
      'mnemonic': str(mnemonic),
    })
  
  return credentials
