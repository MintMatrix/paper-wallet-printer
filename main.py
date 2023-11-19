import argparse
import time
import credentials
import paper

# Paper Wallet Configuration
templateFile = "templates/ADA.pdf"
config = {
  'assetName': { # To do
    'value': 'ADA',
    'position': ''
  },
  'assetImg': {
    'value': 'img/ada.png', # To do
    'position': [479, 290, 98]  
  },
  'address': {
    'value': '', # Generated value
    'position': [470, 280, 88]
  },
  'qr': {
    'value': '', # Generated value
    'position': [479, 290, 98]
  },
  'm': {
    'value': '', # Generated value
    'position': [529, 338, 148]
  },
  'policy_id': {
    'value': '', # Generated value
    'position': [529, 338, 148]
  },
}

# Primary execution sequence
def main(args):

  walletInfo = credentials.generateWallet(args.quantity, args.network, args.verbose)
  paper.fillTemplate(args.quantity, walletInfo, templateFile, config, args.verbose) 
  
# CLI Wrapping
if __name__ == '__main__':
 
  # Parse CLI arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--quantity', type=int, default=1, help='Set the quantity')
  parser.add_argument('--network', type=int, default=1, help='Set the network')
  parser.add_argument('--verbose', action='store_true', default=False, help='Enable verbose mode')
  args = parser.parse_args() 

  # Begin script execution timer
  start_time = time.time()

  # Call main function
  main(args)

  # Caulcate and display execition time
  end_time = time.time()
  execution_time = end_time - start_time
  if args.verbose:
    print(f"Execution time: {execution_time:.2f} seconds")
