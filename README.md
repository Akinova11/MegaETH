# MegaETH Testnet Interaction Script

Welcome to the **MegaETH Testnet Interaction Script**! This Python-based project enables seamless interaction with the MegaETH Testnet by performing various randomized actions across multiple wallets. Whether you're minting tokens, swapping assets, adding liquidity, or requesting test ETH, this script has you covered!

## 📌 Overview

This repository contains a Python script designed to automate interactions with the MegaETH Testnet. For each wallet, the script randomly selects **5 to 10 unique actions** from a pool of **10 possible operations**, including:

- **Minting Tokens**: Via one of 4 minting contracts.
- **Swapping Tokens**: Using one of 4 swap contracts.
- **Adding Liquidity**: To a pool after a swap.
- **Requesting Test ETH**: From a faucet when needed.

## 📂 Project Structure

- **`main.py`** – The core script that drives all wallet interactions.
- **`contracts.py`** – Contains contract addresses and ABI definitions.
- **`pk.txt`** – A user-provided file listing private keys (one per line).

## 🔧 Requirements

Ensure you have the following:

- Python **3.10+** installed.
- The **web3.py** library.
- A `pk.txt` file with your wallet private keys (each 64 characters long).

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

Begin by cloning the repository to your local machine:

```bash
git clone https://github.com/Akinova11/MegaETH.git
cd MegaETH
```

### 2️⃣ Set Up a Virtual Environment

Keep your dependencies tidy with a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3️⃣ Install Dependencies

Install the necessary Python package:

```bash
pip install web3
```

### 4️⃣ Prepare Your Private Keys

Create a file named `pk.txt` in the project’s root directory.

- Add your private keys, **one per line** (e.g., `64-character-hex-key-here`).
- **Security Note:** Never commit `pk.txt` to GitHub. Add it to `.gitignore`:

```plaintext
pk.txt
```

## ⚙️ Configuration

- **RPC Endpoint**: The script connects to the MegaETH Testnet via:
  ```plaintext
  https://carrot.megaeth.com/rpc
  ```
- **Contracts**: All contract addresses and ABIs are stored in `contracts.py`. Check or adjust them as needed.

## ▶️ Running the Script

Launch the script with:

```bash
python main.py
```

### What Happens:

1. The script reads private keys from `pk.txt`.
2. For each wallet, it performs **5–10 random actions**, such as:
   - **Minting Tokens**: Uses one of 4 minting contracts.
   - **Swapping Tokens**: Exchanges ETH for tokens via one of 4 swap contracts.
   - **Swap + Liquidity**: Swaps tokens and adds liquidity to a pool.
   - **Faucet Request**: Requests test ETH if the wallet balance is low.

## 💡 Usage Examples

- **Faucet Request**: Checks the wallet balance and requests ETH if necessary.
- **Token Minting**: Randomly selects a minting contract and mints tokens.
- **Token Swapping**: Swaps a random amount of ETH for tokens.
- **Liquidity Addition**: Adds liquidity to a pool after a swap.

## 🔒 Notes

- **Security First**: Always keep `pk.txt` private and out of version control.
- **Customization**: Modify `main.py` or update `contracts.py` to tailor the script to your needs.

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

🚀 **Happy Testing on MegaETH!** 🎉
