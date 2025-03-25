# contracts.py

MINT_CONTRACTS = {
    "tkETH": "0x176735870dc6C22B4EBFBf519DE2ce758de78d94",
    "tkUSDC": "0xFaf334e157175Ff676911AdcF0964D7f54F2C424",
    "tkWBTC": "0xF82ff0799448630eB56cE747dB840a2e02cDe4D8",
    "cUSD": "0xE9b6e75C243B6100ffcb1c66e8f78F96FeeA727f"
}

MINT_ABI = [
    {"constant": False, "inputs": [], "name": "mint", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False, "inputs": [{"name": "amount", "type": "uint256"}], "name": "mint", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False, "inputs": [{"name": "to", "type": "address"}, {"name": "amount", "type": "uint256"}], "name": "mint", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False, "inputs": [], "name": "claim", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [{"name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"}
]

SWAP_CONTRACTS = {
    "WETH": "0x776401b9BC8aAe31A685731B7147D4445fD9FB19",
    "cUSD": "0xE9b6e75C243B6100ffcb1c66e8f78F96FeeA727f",
    "MAFIA": "0x8A411b19dB90987564E6722F1B7Cc1E3C98e4e62",
    "tkUSDC": "0xFaf334e157175Ff676911AdcF0964D7f54F2C424",
    "MEGA": "0x10a6be7d23989D00d528E68cF8051d095f741145"
}

ROUTER_ADDRESS = "0xa6b579684e943f7d00d616a48cf99b5147fc57a5"

SWAP_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "amountOutMin", "type": "uint256"},
            {"name": "path", "type": "address[]"},
            {"name": "to", "type": "address"},
            {"name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactETHForTokens",
        "outputs": [{"name": "amounts", "type": "uint256[]"}],
        "payable": True,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "token", "type": "address"},
            {"name": "amountTokenDesired", "type": "uint256"},
            {"name": "amountTokenMin", "type": "uint256"},
            {"name": "amountETHMin", "type": "uint256"},
            {"name": "to", "type": "address"},
            {"name": "deadline", "type": "uint256"}
        ],
        "name": "addLiquidityETH",
        "outputs": [
            {"name": "amountToken", "type": "uint256"},
            {"name": "amountETH", "type": "uint256"},
            {"name": "liquidity", "type": "uint256"}
        ],
        "payable": True,
        "stateMutability": "payable",
        "type": "function"
    }
]

TOKEN_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]