import sys
import os
import random
import time
from web3 import Web3
from contracts import MINT_CONTRACTS, MINT_ABI, SWAP_CONTRACTS, ROUTER_ADDRESS, SWAP_ABI, TOKEN_ABI

# Setting encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Connecting to MegaETH Testnet
RPC_URL = "https://carrot.megaeth.com/rpc"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    raise Exception("Failed to connect to network")
print("Successfully connected to MegaETH Testnet")

chain_id = w3.eth.chain_id
print(f"Chain ID: {chain_id}")

# Reading private keys
private_keys = []
try:
    with open("pk.txt", "r", encoding="utf-8") as file:
        for line in file:
            key = line.strip()
            if key and len(key) == 64:
                private_keys.append(key)
except FileNotFoundError:
    raise Exception("File pk.txt not found")

# Function to request test ETH from faucet
def request_faucet(account):
    print(f"Requesting test ETH for {account.address}...")
    FAUCET_ADDRESS = w3.to_checksum_address("0x22988d807e4487b38e7632f3bb21f2383c3cc6b2")
    try:
        balance = w3.eth.get_balance(account.address)
        balance_eth = w3.from_wei(balance, 'ether')
        print(f"Balance of {account.address}: {balance_eth} ETH")
        
        if balance_eth < 0.00001:
            print(f"Insufficient ETH on {account.address}, skipping...")
            return
        
        gas_price = w3.eth.gas_price
        nonce = w3.eth.get_transaction_count(account.address)
        tx = {
            "from": account.address,
            "to": FAUCET_ADDRESS,
            "data": "0x61ed4648",
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": gas_price,
            "chainId": chain_id,
            "value": 0  # Corrected from "Panzer" to "value"
        }
        signed_tx = w3.eth.account.sign_transaction(tx, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction sent: {w3.to_hex(tx_hash)}")
    except Exception as e:
        print(f"Error for {account.address}: {str(e)}")

# Function to mint tokens (with randomization)
def mint_tokens(account):
    print(f"\nMinting tokens on {account.address}")
    # Random selection of a token for minting
    token_name = random.choice(list(MINT_CONTRACTS.keys()))
    contract_address = w3.to_checksum_address(MINT_CONTRACTS[token_name])
    
    contract = w3.eth.contract(address=contract_address, abi=MINT_ABI)
    balance = w3.eth.get_balance(account.address)
    print(f"Wallet balance {account.address}: {w3.from_wei(balance, 'ether')} ETH")
    
    if balance < w3.to_wei('0.000001', 'ether'):
        print(f"Error: Insufficient ETH for gas on {account.address}. Get gas from https://testnet.megaeth.com/#3")
        return
    
    try:
        decimals = contract.functions.decimals().call()
    except Exception:
        decimals = 18
    
    if token_name == "tkETH":
        amount_to_mint = 10**decimals
    elif token_name == "tkUSDC":
        amount_to_mint = int(2000 * 10**decimals)
    elif token_name == "tkWBTC":
        amount_to_mint = int(0.02 * 10**decimals)
    elif token_name == "cUSD":
        amount_to_mint = 1000 * 10**decimals
    
    try:
        nonce = w3.eth.get_transaction_count(account.address, 'pending')
        tx = contract.functions.mint(account.address, amount_to_mint).build_transaction({
            'from': account.address, 'nonce': nonce, 'gas': 100000, 'gasPrice': w3.to_wei('0.003659501', 'gwei'), 'chainId': chain_id
        })
        signed_tx = w3.eth.account.sign_transaction(tx, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction sent: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print(f"Mint successful: {token_name}")
    except Exception as e:
        print(f"Mint failed: {str(e)}")

# Function to swap tokens (with randomization)
def swap_tokens(account):
    print(f"\nSwapping ETH for a token on {account.address}")
    router_address = w3.to_checksum_address(ROUTER_ADDRESS)
    router = w3.eth.contract(address=router_address, abi=SWAP_ABI)
    
    eth_balance = w3.eth.get_balance(account.address)
    print(f"Wallet balance {account.address}: {w3.from_wei(eth_balance, 'ether')} ETH")
    
    gas_reserve = w3.to_wei('0.000001', 'ether')
    if eth_balance <= gas_reserve:
        print(f"Error: Insufficient ETH for gas on {account.address}. Get gas from https://testnet.megaeth.com/#3")
        return
    
    usable_balance = eth_balance - gas_reserve
    swap_percent = random.uniform(0.02, 0.10)
    amount_eth = int(usable_balance * swap_percent)
    print(f"Using {swap_percent*100:.2f}% of available balance: {w3.from_wei(amount_eth, 'ether')} ETH")
    
    # Random selection of a token for swapping (excluding WETH)
    token_options = [token for token in SWAP_CONTRACTS.keys() if token != "WETH"]
    token_name = random.choice(token_options)
    token_address = w3.to_checksum_address(SWAP_CONTRACTS[token_name])
    
    path = [w3.to_checksum_address(SWAP_CONTRACTS["WETH"]), token_address]
    print(f"Swap path: {path}")
    
    deadline = int(time.time()) + 60 * 20
    nonce = w3.eth.get_transaction_count(account.address, 'pending')
    
    try:
        tx = router.functions.swapExactETHForTokens(
            0, path, account.address, deadline
        ).build_transaction({
            'from': account.address, 'value': amount_eth, 'nonce': nonce, 'gas': 200000, 'gasPrice': w3.to_wei('0.003659501', 'gwei'), 'chainId': chain_id
        })
        signed_tx = w3.eth.account.sign_transaction(tx, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction sent: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print(f"Swap successful: ETH -> {token_name}")
    except Exception as e:
        print(f"Swap failed: {str(e)}")

# Function to add liquidity to MAFIA+ETH (updated for automation)
def add_liquidity_mafia_eth(account):
    print(f"\nAdding liquidity to MAFIA+ETH pool on {account.address}")
    router_address = w3.to_checksum_address(ROUTER_ADDRESS)
    router = w3.eth.contract(address=router_address, abi=SWAP_ABI)
    mafia_address = w3.to_checksum_address(SWAP_CONTRACTS["MAFIA"])
    mafia_contract = w3.eth.contract(address=mafia_address, abi=TOKEN_ABI)
    
    eth_balance = w3.eth.get_balance(account.address)
    print(f"Wallet balance {account.address}: {w3.from_wei(eth_balance, 'ether')} ETH")
    
    gas_reserve = w3.to_wei('0.000002', 'ether')
    if eth_balance <= gas_reserve:
        print(f"Error: Insufficient ETH for gas on {account.address}. Get gas from https://testnet.megaeth.com/#3")
        return
    
    usable_balance = eth_balance - gas_reserve
    liquidity_percent = random.uniform(0.02, 0.10)
    amount_eth = int(usable_balance * liquidity_percent)
    print(f"Using {liquidity_percent*100:.2f}% of available balance: {w3.from_wei(amount_eth, 'ether')} ETH")
    
    nonce = w3.eth.get_transaction_count(account.address, 'pending')
    deadline = int(time.time()) + 60 * 20
    
    # Step 1: Swap ETH to MAFIA
    amount_out_min = 0
    path = [w3.to_checksum_address(SWAP_CONTRACTS["WETH"]), mafia_address]
    print(f"Step 1: Swapping ETH to MAFIA...")
    try:
        tx_swap = router.functions.swapExactETHForTokens(
            amount_out_min, path, account.address, deadline
        ).build_transaction({
            'from': account.address, 'value': amount_eth, 'gas': 150000, 'gasPrice': w3.to_wei('0.003659501', 'gwei'), 'nonce': nonce, 'chainId': chain_id
        })
        signed_tx_swap = w3.eth.account.sign_transaction(tx_swap, account.key)
        tx_hash_swap = w3.eth.send_raw_transaction(signed_tx_swap.raw_transaction)
        print(f"Swap transaction sent: {tx_hash_swap.hex()}")
        receipt_swap = w3.eth.wait_for_transaction_receipt(tx_hash_swap)
        if receipt_swap.status == 0:
            print("Swap failed")
            return
        nonce += 1
    except Exception as e:
        print(f"Swap failed: {str(e)}")
        return
    
    time.sleep(random.uniform(10, 30))
    
    mafia_balance = mafia_contract.functions.balanceOf(account.address).call()
    print(f"MAFIA balance after swap: {w3.from_wei(mafia_balance, 'ether')} MAFIA")
    if mafia_balance == 0:
        print("Error: No MAFIA received from swap")
        return
    
    # Step 2: Approve MAFIA for the router
    print(f"Step 2: Approving MAFIA for router...")
    try:
        tx_approve = mafia_contract.functions.approve(router_address, mafia_balance).build_transaction({
            'from': account.address, 'nonce': nonce, 'gas': 100000, 'gasPrice': w3.to_wei('0.003659501', 'gwei'), 'chainId': chain_id
        })
        signed_tx_approve = w3.eth.account.sign_transaction(tx_approve, account.key)
        tx_hash_approve = w3.eth.send_raw_transaction(signed_tx_approve.raw_transaction)
        print(f"Approve transaction sent: {tx_hash_approve.hex()}")
        receipt_approve = w3.eth.wait_for_transaction_receipt(tx_hash_approve)
        if receipt_approve.status == 0:
            print("Approve failed")
            return
        nonce += 1
    except Exception as e:
        print(f"Approve failed: {str(e)}")
        return
    
    time.sleep(random.uniform(10, 30))
    
    # Step 3: Add liquidity
    print(f"Step 3: Adding liquidity to MAFIA+ETH pool...")
    try:
        tx_liquidity = router.functions.addLiquidityETH(
            mafia_address, mafia_balance, 0, 0, account.address, deadline
        ).build_transaction({
            'from': account.address, 'value': amount_eth, 'gas': 200000, 'gasPrice': w3.to_wei('0.003659501', 'gwei'), 'nonce': nonce, 'chainId': chain_id
        })
        signed_tx_liquidity = w3.eth.account.sign_transaction(tx_liquidity, account.key)
        tx_hash_liquidity = w3.eth.send_raw_transaction(signed_tx_liquidity.raw_transaction)
        print(f"Liquidity transaction sent: {tx_hash_liquidity.hex()}")
        receipt_liquidity = w3.eth.wait_for_transaction_receipt(tx_hash_liquidity)
        if receipt_liquidity.status == 1:
            print("Liquidity added successfully")
    except Exception as e:
        print(f"Liquidity addition failed: {str(e)}")

# List of available actions
actions = [
    ("mint", mint_tokens),
    ("swap", swap_tokens),
    ("liquidity_mafia_eth", add_liquidity_mafia_eth),
    ("faucet", request_faucet)
]

# Main function to process wallets
def process_wallets():
    for key in private_keys:
        account = w3.eth.account.from_key(key)
        print(f"\nProcessing wallet: {account.address}")
        
        # Random number of actions (5-10)
        num_actions = random.randint(5, 10)
        print(f"Selected {num_actions} actions for this wallet")
        
        for _ in range(num_actions):
            # Selection of a random action
            action_name, action_func = random.choice(actions)
            print(f"Performing action: {action_name}")
            try:
                action_func(account)
            except Exception as e:
                print(f"Error during {action_name}: {str(e)}")
            
            # Delay between actions (60-600 seconds)
            delay = random.uniform(60, 600)
            print(f"Waiting {delay:.2f} seconds before next action...")
            time.sleep(delay)
        
        # Delay before the next wallet (6000-20000 seconds)
        wallet_delay = random.uniform(6000, 20000)
        print(f"Waiting {wallet_delay:.2f} seconds before next wallet...")
        time.sleep(wallet_delay)

# Run the script
if __name__ == "__main__":
    process_wallets()