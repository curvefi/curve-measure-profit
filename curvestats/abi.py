import json

ABI = json.loads("""[
 {
  "name": "TokenExchange",
  "inputs": [
   {
    "type": "address",
    "name": "buyer",
    "indexed": true
   },
   {
    "type": "int128",
    "name": "sold_id",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "tokens_sold",
    "indexed": false
   },
   {
    "type": "int128",
    "name": "bought_id",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "tokens_bought",
    "indexed": false
   }
  ],
  "anonymous": false,
  "type": "event"
 },
 {
  "name": "TokenExchangeUnderlying",
  "inputs": [
   {
    "type": "address",
    "name": "buyer",
    "indexed": true
   },
   {
    "type": "int128",
    "name": "sold_id",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "tokens_sold",
    "indexed": false
   },
   {
    "type": "int128",
    "name": "bought_id",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "tokens_bought",
    "indexed": false
   }
  ],
  "anonymous": false,
  "type": "event"
 },
 {
  "name": "AddLiquidity",
  "inputs": [
   {
    "type": "address",
    "name": "provider",
    "indexed": true
   },
   {
    "type": "uint256[2]",
    "name": "token_amounts",
    "indexed": false
   },
   {
    "type": "uint256[2]",
    "name": "fees",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "invariant",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "token_supply",
    "indexed": false
   }
  ],
  "anonymous": false,
  "type": "event"
 },
 {
  "name": "RemoveLiquidity",
  "inputs": [
   {
    "type": "address",
    "name": "provider",
    "indexed": true
   },
   {
    "type": "uint256[2]",
    "name": "token_amounts",
    "indexed": false
   },
   {
    "type": "uint256[2]",
    "name": "fees",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "token_supply",
    "indexed": false
   }
  ],
  "anonymous": false,
  "type": "event"
 },
 {
  "name": "RemoveLiquidityImbalance",
  "inputs": [
   {
    "type": "address",
    "name": "provider",
    "indexed": true
   },
   {
    "type": "uint256[2]",
    "name": "token_amounts",
    "indexed": false
   },
   {
    "type": "uint256[2]",
    "name": "fees",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "invariant",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "token_supply",
    "indexed": false
   }
  ],
  "anonymous": false,
  "type": "event"
 },
 {
  "name": "CommitNewAdmin",
  "inputs": [
   {
    "type": "uint256",
    "name": "deadline",
    "indexed": true,
    "unit": "sec"
   },
   {
    "type": "address",
    "name": "admin",
    "indexed": true
   }
  ],
  "anonymous": false,
  "type": "event"
 },
 {
  "name": "NewAdmin",
  "inputs": [
   {
    "type": "address",
    "name": "admin",
    "indexed": true
   }
  ],
  "anonymous": false,
  "type": "event"
 },
 {
  "name": "CommitNewParameters",
  "inputs": [
   {
    "type": "uint256",
    "name": "deadline",
    "indexed": true,
    "unit": "sec"
   },
   {
    "type": "uint256",
    "name": "A",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "fee",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "admin_fee",
    "indexed": false
   }
  ],
  "anonymous": false,
  "type": "event"
 },
 {
  "name": "NewParameters",
  "inputs": [
   {
    "type": "uint256",
    "name": "A",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "fee",
    "indexed": false
   },
   {
    "type": "uint256",
    "name": "admin_fee",
    "indexed": false
   }
  ],
  "anonymous": false,
  "type": "event"
 },
 {
  "outputs": [],
  "inputs": [
   {
    "type": "address[2]",
    "name": "_coins"
   },
   {
    "type": "address[2]",
    "name": "_underlying_coins"
   },
   {
    "type": "address",
    "name": "_pool_token"
   },
   {
    "type": "uint256",
    "name": "_A"
   },
   {
    "type": "uint256",
    "name": "_fee"
   }
  ],
  "constant": false,
  "payable": false,
  "type": "constructor"
 },
 {
  "name": "get_virtual_price",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 1084167
 },
 {
  "name": "calc_token_amount",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [
   {
    "type": "uint256[2]",
    "name": "amounts"
   },
   {
    "type": "bool",
    "name": "deposit"
   }
  ],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 4239939
 },
 {
  "name": "add_liquidity",
  "outputs": [],
  "inputs": [
   {
    "type": "uint256[2]",
    "name": "amounts"
   },
   {
    "type": "uint256",
    "name": "min_mint_amount"
   }
  ],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 6479997
 },
 {
  "name": "get_dy",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [
   {
    "type": "int128",
    "name": "i"
   },
   {
    "type": "int128",
    "name": "j"
   },
   {
    "type": "uint256",
    "name": "dx"
   }
  ],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2543681
 },
 {
  "name": "get_dx",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [
   {
    "type": "int128",
    "name": "i"
   },
   {
    "type": "int128",
    "name": "j"
   },
   {
    "type": "uint256",
    "name": "dy"
   }
  ],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2543687
 },
 {
  "name": "get_dy_underlying",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [
   {
    "type": "int128",
    "name": "i"
   },
   {
    "type": "int128",
    "name": "j"
   },
   {
    "type": "uint256",
    "name": "dx"
   }
  ],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2543506
 },
 {
  "name": "get_dx_underlying",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [
   {
    "type": "int128",
    "name": "i"
   },
   {
    "type": "int128",
    "name": "j"
   },
   {
    "type": "uint256",
    "name": "dy"
   }
  ],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2543512
 },
 {
  "name": "exchange",
  "outputs": [],
  "inputs": [
   {
    "type": "int128",
    "name": "i"
   },
   {
    "type": "int128",
    "name": "j"
   },
   {
    "type": "uint256",
    "name": "dx"
   },
   {
    "type": "uint256",
    "name": "min_dy"
   }
  ],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 5184573
 },
 {
  "name": "exchange_underlying",
  "outputs": [],
  "inputs": [
   {
    "type": "int128",
    "name": "i"
   },
   {
    "type": "int128",
    "name": "j"
   },
   {
    "type": "uint256",
    "name": "dx"
   },
   {
    "type": "uint256",
    "name": "min_dy"
   }
  ],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 5200817
 },
 {
  "name": "remove_liquidity",
  "outputs": [],
  "inputs": [
   {
    "type": "uint256",
    "name": "_amount"
   },
   {
    "type": "uint256[2]",
    "name": "min_amounts"
   }
  ],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 153898
 },
 {
  "name": "remove_liquidity_imbalance",
  "outputs": [],
  "inputs": [
   {
    "type": "uint256[2]",
    "name": "amounts"
   },
   {
    "type": "uint256",
    "name": "max_burn_amount"
   }
  ],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 6479708
 },
 {
  "name": "commit_new_parameters",
  "outputs": [],
  "inputs": [
   {
    "type": "uint256",
    "name": "amplification"
   },
   {
    "type": "uint256",
    "name": "new_fee"
   },
   {
    "type": "uint256",
    "name": "new_admin_fee"
   }
  ],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 146105
 },
 {
  "name": "apply_new_parameters",
  "outputs": [],
  "inputs": [],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 133512
 },
 {
  "name": "revert_new_parameters",
  "outputs": [],
  "inputs": [],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 21835
 },
 {
  "name": "commit_transfer_ownership",
  "outputs": [],
  "inputs": [
   {
    "type": "address",
    "name": "_owner"
   }
  ],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 74512
 },
 {
  "name": "apply_transfer_ownership",
  "outputs": [],
  "inputs": [],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 60568
 },
 {
  "name": "revert_transfer_ownership",
  "outputs": [],
  "inputs": [],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 21925
 },
 {
  "name": "withdraw_admin_fees",
  "outputs": [],
  "inputs": [],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 12831
 },
 {
  "name": "kill_me",
  "outputs": [],
  "inputs": [],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 37878
 },
 {
  "name": "unkill_me",
  "outputs": [],
  "inputs": [],
  "constant": false,
  "payable": false,
  "type": "function",
  "gas": 22015
 },
 {
  "name": "coins",
  "outputs": [
   {
    "type": "address",
    "name": "out"
   }
  ],
  "inputs": [
   {
    "type": "int128",
    "name": "arg0"
   }
  ],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2190
 },
 {
  "name": "underlying_coins",
  "outputs": [
   {
    "type": "address",
    "name": "out"
   }
  ],
  "inputs": [
   {
    "type": "int128",
    "name": "arg0"
   }
  ],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2220
 },
 {
  "name": "balances",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [
   {
    "type": "int128",
    "name": "arg0"
   }
  ],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2250
 },
 {
  "name": "A",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2081
 },
 {
  "name": "fee",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2111
 },
 {
  "name": "admin_fee",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2141
 },
 {
  "name": "owner",
  "outputs": [
   {
    "type": "address",
    "name": "out"
   }
  ],
  "inputs": [],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2171
 },
 {
  "name": "admin_actions_deadline",
  "outputs": [
   {
    "type": "uint256",
    "unit": "sec",
    "name": "out"
   }
  ],
  "inputs": [],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2201
 },
 {
  "name": "transfer_ownership_deadline",
  "outputs": [
   {
    "type": "uint256",
    "unit": "sec",
    "name": "out"
   }
  ],
  "inputs": [],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2231
 },
 {
  "name": "future_A",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2261
 },
 {
  "name": "future_fee",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2291
 },
 {
  "name": "future_admin_fee",
  "outputs": [
   {
    "type": "uint256",
    "name": "out"
   }
  ],
  "inputs": [],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2321
 },
 {
  "name": "future_owner",
  "outputs": [
   {
    "type": "address",
    "name": "out"
   }
  ],
  "inputs": [],
  "constant": true,
  "payable": false,
  "type": "function",
  "gas": 2351
 }
]""")
TOKEN_ABI = json.loads("""[
    {
        "constant": true,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_spender",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_from",
                "type": "address"
            },
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            },
            {
                "name": "_spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "payable": true,
        "stateMutability": "payable",
        "type": "fallback"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": true,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": false,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": true,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": false,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    }
]""")

NEW_ABI = json.loads("""
[{"anonymous": false, "inputs": [{"indexed": true, "name": "buyer", "type": "address"}, {"indexed": false, "name": "sold_id", "type": "int128"}, {"indexed": false, "name": "tokens_sold", "type": "uint256"}, {"indexed": false, "name": "bought_id", "type": "int128"}, {"indexed": false, "name": "tokens_bought", "type": "uint256"}], "name": "TokenExchange", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "buyer", "type": "address"}, {"indexed": false, "name": "sold_id", "type": "int128"}, {"indexed": false, "name": "tokens_sold", "type": "uint256"}, {"indexed": false, "name": "bought_id", "type": "int128"}, {"indexed": false, "name": "tokens_bought", "type": "uint256"}], "name": "TokenExchangeUnderlying", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "provider", "type": "address"}, {"indexed": false, "name": "token_amounts", "type": "uint256[3]"}, {"indexed": false, "name": "fees", "type": "uint256[3]"}, {"indexed": false, "name": "invariant", "type": "uint256"}, {"indexed": false, "name": "token_supply", "type": "uint256"}], "name": "AddLiquidity", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "provider", "type": "address"}, {"indexed": false, "name": "token_amounts", "type": "uint256[3]"}, {"indexed": false, "name": "fees", "type": "uint256[3]"}, {"indexed": false, "name": "token_supply", "type": "uint256"}], "name": "RemoveLiquidity", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "provider", "type": "address"}, {"indexed": false, "name": "token_amount", "type": "uint256"}, {"indexed": false, "name": "coin_amount", "type": "uint256"}], "name": "RemoveLiquidityOne", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "provider", "type": "address"}, {"indexed": false, "name": "token_amounts", "type": "uint256[3]"}, {"indexed": false, "name": "fees", "type": "uint256[3]"}, {"indexed": false, "name": "invariant", "type": "uint256"}, {"indexed": false, "name": "token_supply", "type": "uint256"}], "name": "RemoveLiquidityImbalance", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "deadline", "type": "uint256"}, {"indexed": true, "name": "admin", "type": "address"}], "name": "CommitNewAdmin", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "admin", "type": "address"}], "name": "NewAdmin", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "deadline", "type": "uint256"}, {"indexed": false, "name": "fee", "type": "uint256"}, {"indexed": false, "name": "admin_fee", "type": "uint256"}, {"indexed": false, "name": "offpeg_fee_multiplier", "type": "uint256"}], "name": "CommitNewFee", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "fee", "type": "uint256"}, {"indexed": false, "name": "admin_fee", "type": "uint256"}, {"indexed": false, "name": "offpeg_fee_multiplier", "type": "uint256"}], "name": "NewFee", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "old_A", "type": "uint256"}, {"indexed": false, "name": "new_A", "type": "uint256"}, {"indexed": false, "name": "initial_time", "type": "uint256"}, {"indexed": false, "name": "future_time", "type": "uint256"}], "name": "RampA", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "A", "type": "uint256"}, {"indexed": false, "name": "t", "type": "uint256"}], "name": "StopRampA", "type": "event"}, {"inputs": [{"name": "_coins", "type": "address[3]"}, {"name": "_underlying_coins", "type": "address[3]"}, {"name": "_pool_token", "type": "address"}, {"name": "_A", "type": "uint256"}, {"name": "_fee", "type": "uint256"}, {"name": "_admin_fee", "type": "uint256"}, {"name": "_offpeg_fee_multiplier", "type": "uint256"}], "outputs": [], "stateMutability": "nonpayable", "type": "constructor", "name": "constructor"}, {"gas": 5174, "inputs": [], "name": "A", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 5136, "inputs": [], "name": "A_precise", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 11513, "inputs": [{"name": "i", "type": "int128"}, {"name": "j", "type": "int128"}], "name": "dynamic_fee", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 3358, "inputs": [{"name": "i", "type": "uint256"}], "name": "balances", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2682167, "inputs": [], "name": "get_virtual_price", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 5348262, "inputs": [{"name": "_amounts", "type": "uint256[3]"}, {"name": "is_deposit", "type": "bool"}], "name": "calc_token_amount", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"name": "_amounts", "type": "uint256[3]"}, {"name": "_min_mint_amount", "type": "uint256"}], "name": "add_liquidity", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"name": "_amounts", "type": "uint256[3]"}, {"name": "_min_mint_amount", "type": "uint256"}, {"name": "_use_underlying", "type": "bool"}], "name": "add_liquidity", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"}, {"gas": 6241974, "inputs": [{"name": "i", "type": "int128"}, {"name": "j", "type": "int128"}, {"name": "dx", "type": "uint256"}], "name": "get_dy", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 6242004, "inputs": [{"name": "i", "type": "int128"}, {"name": "j", "type": "int128"}, {"name": "dx", "type": "uint256"}], "name": "get_dy_underlying", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 6383108, "inputs": [{"name": "i", "type": "int128"}, {"name": "j", "type": "int128"}, {"name": "dx", "type": "uint256"}, {"name": "min_dy", "type": "uint256"}], "name": "exchange", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"}, {"gas": 6390358, "inputs": [{"name": "i", "type": "int128"}, {"name": "j", "type": "int128"}, {"name": "dx", "type": "uint256"}, {"name": "min_dy", "type": "uint256"}], "name": "exchange_underlying", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"name": "_amount", "type": "uint256"}, {"name": "_min_amounts", "type": "uint256[3]"}], "name": "remove_liquidity", "outputs": [{"name": "", "type": "uint256[3]"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"name": "_amount", "type": "uint256"}, {"name": "_min_amounts", "type": "uint256[3]"}, {"name": "_use_underlying", "type": "bool"}], "name": "remove_liquidity", "outputs": [{"name": "", "type": "uint256[3]"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"name": "_amounts", "type": "uint256[3]"}, {"name": "_max_burn_amount", "type": "uint256"}], "name": "remove_liquidity_imbalance", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"name": "_amounts", "type": "uint256[3]"}, {"name": "_max_burn_amount", "type": "uint256"}, {"name": "_use_underlying", "type": "bool"}], "name": "remove_liquidity_imbalance", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"}, {"gas": 4451330, "inputs": [{"name": "_token_amount", "type": "uint256"}, {"name": "i", "type": "int128"}], "name": "calc_withdraw_one_coin", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"name": "_token_amount", "type": "uint256"}, {"name": "i", "type": "int128"}, {"name": "_min_amount", "type": "uint256"}], "name": "remove_liquidity_one_coin", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"name": "_token_amount", "type": "uint256"}, {"name": "i", "type": "int128"}, {"name": "_min_amount", "type": "uint256"}, {"name": "_use_underlying", "type": "bool"}], "name": "remove_liquidity_one_coin", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"}, {"gas": 151659, "inputs": [{"name": "_future_A", "type": "uint256"}, {"name": "_future_time", "type": "uint256"}], "name": "ramp_A", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 148420, "inputs": [], "name": "stop_ramp_A", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 146209, "inputs": [{"name": "new_fee", "type": "uint256"}, {"name": "new_admin_fee", "type": "uint256"}, {"name": "new_offpeg_fee_multiplier", "type": "uint256"}], "name": "commit_new_fee", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 133471, "inputs": [], "name": "apply_new_fee", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 21712, "inputs": [], "name": "revert_new_parameters", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 74450, "inputs": [{"name": "_owner", "type": "address"}], "name": "commit_transfer_ownership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 60527, "inputs": [], "name": "apply_transfer_ownership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 21802, "inputs": [], "name": "revert_transfer_ownership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 73781, "inputs": [], "name": "withdraw_admin_fees", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 62003, "inputs": [], "name": "donate_admin_fees", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 37785, "inputs": [], "name": "kill_me", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 21922, "inputs": [], "name": "unkill_me", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 37052, "inputs": [{"name": "referral_code", "type": "uint256"}], "name": "set_aave_referral", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 37085, "inputs": [{"name": "_reward_receiver", "type": "address"}], "name": "set_reward_receiver", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 37115, "inputs": [{"name": "_admin_fee_receiver", "type": "address"}], "name": "set_admin_fee_receiver", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"gas": 2097, "inputs": [{"name": "arg0", "type": "uint256"}], "name": "coins", "outputs": [{"name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"gas": 2127, "inputs": [{"name": "arg0", "type": "uint256"}], "name": "underlying_coins", "outputs": [{"name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"gas": 2157, "inputs": [{"name": "arg0", "type": "uint256"}], "name": "admin_balances", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2078, "inputs": [], "name": "fee", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2108, "inputs": [], "name": "offpeg_fee_multiplier", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2138, "inputs": [], "name": "admin_fee", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2168, "inputs": [], "name": "owner", "outputs": [{"name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"gas": 2198, "inputs": [], "name": "lp_token", "outputs": [{"name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"gas": 2228, "inputs": [], "name": "initial_A", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2258, "inputs": [], "name": "future_A", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2288, "inputs": [], "name": "initial_A_time", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2318, "inputs": [], "name": "future_A_time", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2348, "inputs": [], "name": "admin_actions_deadline", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2378, "inputs": [], "name": "transfer_ownership_deadline", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2408, "inputs": [], "name": "future_fee", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2438, "inputs": [], "name": "future_admin_fee", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2468, "inputs": [], "name": "future_offpeg_fee_multiplier", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"gas": 2498, "inputs": [], "name": "future_owner", "outputs": [{"name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"gas": 2528, "inputs": [], "name": "reward_receiver", "outputs": [{"name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"gas": 2558, "inputs": [], "name": "admin_fee_receiver", "outputs": [{"name": "", "type": "address"}], "stateMutability": "view", "type": "function"}]
""")

IDLE_ABI = json.loads("""[{"name":"TokenExchange","inputs":[{"type":"address","name":"buyer","indexed":true},{"type":"int128","name":"sold_id","indexed":false},{"type":"uint256","name":"tokens_sold","indexed":false},{"type":"int128","name":"bought_id","indexed":false},{"type":"uint256","name":"tokens_bought","indexed":false}],"anonymous":false,"type":"event"},{"name":"TokenExchangeUnderlying","inputs":[{"type":"address","name":"buyer","indexed":true},{"type":"int128","name":"sold_id","indexed":false},{"type":"uint256","name":"tokens_sold","indexed":false},{"type":"int128","name":"bought_id","indexed":false},{"type":"uint256","name":"tokens_bought","indexed":false}],"anonymous":false,"type":"event"},{"name":"AddLiquidity","inputs":[{"type":"address","name":"provider","indexed":true},{"type":"uint256[3]","name":"token_amounts","indexed":false},{"type":"uint256[3]","name":"fees","indexed":false},{"type":"uint256","name":"invariant","indexed":false},{"type":"uint256","name":"token_supply","indexed":false}],"anonymous":false,"type":"event"},{"name":"RemoveLiquidity","inputs":[{"type":"address","name":"provider","indexed":true},{"type":"uint256[3]","name":"token_amounts","indexed":false},{"type":"uint256[3]","name":"fees","indexed":false},{"type":"uint256","name":"token_supply","indexed":false}],"anonymous":false,"type":"event"},{"name":"RemoveLiquidityOne","inputs":[{"type":"address","name":"provider","indexed":true},{"type":"uint256","name":"token_amount","indexed":false},{"type":"uint256","name":"coin_amount","indexed":false}],"anonymous":false,"type":"event"},{"name":"RemoveLiquidityImbalance","inputs":[{"type":"address","name":"provider","indexed":true},{"type":"uint256[3]","name":"token_amounts","indexed":false},{"type":"uint256[3]","name":"fees","indexed":false},{"type":"uint256","name":"invariant","indexed":false},{"type":"uint256","name":"token_supply","indexed":false}],"anonymous":false,"type":"event"},{"name":"CommitNewAdmin","inputs":[{"type":"uint256","name":"deadline","indexed":true},{"type":"address","name":"admin","indexed":true}],"anonymous":false,"type":"event"},{"name":"NewAdmin","inputs":[{"type":"address","name":"admin","indexed":true}],"anonymous":false,"type":"event"},{"name":"CommitNewFee","inputs":[{"type":"uint256","name":"deadline","indexed":true},{"type":"uint256","name":"fee","indexed":false},{"type":"uint256","name":"admin_fee","indexed":false}],"anonymous":false,"type":"event"},{"name":"NewFee","inputs":[{"type":"uint256","name":"fee","indexed":false},{"type":"uint256","name":"admin_fee","indexed":false}],"anonymous":false,"type":"event"},{"name":"RampA","inputs":[{"type":"uint256","name":"old_A","indexed":false},{"type":"uint256","name":"new_A","indexed":false},{"type":"uint256","name":"initial_time","indexed":false},{"type":"uint256","name":"future_time","indexed":false}],"anonymous":false,"type":"event"},{"name":"StopRampA","inputs":[{"type":"uint256","name":"A","indexed":false},{"type":"uint256","name":"t","indexed":false}],"anonymous":false,"type":"event"},{"outputs":[],"inputs":[{"type":"address","name":"_owner"},{"type":"address","name":"_reward_admin"},{"type":"address","name":"_reward_claimant"},{"type":"address[3]","name":"_coins"},{"type":"address[3]","name":"_underlying_coins"},{"type":"address","name":"_pool_token"},{"type":"uint256","name":"_A"},{"type":"uint256","name":"_fee"},{"type":"uint256","name":"_admin_fee"}],"stateMutability":"nonpayable","type":"constructor"},{"name":"A","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":5199},{"name":"A_precise","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":5161},{"name":"get_virtual_price","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1194016},{"name":"calc_token_amount","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256[3]","name":"amounts"},{"type":"bool","name":"is_deposit"}],"stateMutability":"view","type":"function","gas":4725859},{"name":"add_liquidity","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256[3]","name":"_amounts"},{"type":"uint256","name":"_min_mint_amount"}],"stateMutability":"nonpayable","type":"function"},{"name":"add_liquidity","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256[3]","name":"_amounts"},{"type":"uint256","name":"_min_mint_amount"},{"type":"bool","name":"_use_underlying"}],"stateMutability":"nonpayable","type":"function"},{"name":"get_dy","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"int128","name":"i"},{"type":"int128","name":"j"},{"type":"uint256","name":"dx"}],"stateMutability":"view","type":"function","gas":2809093},{"name":"get_dx","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"int128","name":"i"},{"type":"int128","name":"j"},{"type":"uint256","name":"dy"}],"stateMutability":"view","type":"function","gas":2808954},{"name":"get_dy_underlying","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"int128","name":"i"},{"type":"int128","name":"j"},{"type":"uint256","name":"dx"}],"stateMutability":"view","type":"function","gas":2808933},{"name":"get_dx_underlying","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"int128","name":"i"},{"type":"int128","name":"j"},{"type":"uint256","name":"dy"}],"stateMutability":"view","type":"function","gas":2808794},{"name":"exchange","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"int128","name":"i"},{"type":"int128","name":"j"},{"type":"uint256","name":"dx"},{"type":"uint256","name":"min_dy"}],"stateMutability":"nonpayable","type":"function","gas":5769355},{"name":"exchange_underlying","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"int128","name":"i"},{"type":"int128","name":"j"},{"type":"uint256","name":"dx"},{"type":"uint256","name":"min_dy"}],"stateMutability":"nonpayable","type":"function","gas":5773227},{"name":"remove_liquidity","outputs":[{"type":"uint256[3]","name":""}],"inputs":[{"type":"uint256","name":"_amount"},{"type":"uint256[3]","name":"_min_amounts"}],"stateMutability":"nonpayable","type":"function"},{"name":"remove_liquidity","outputs":[{"type":"uint256[3]","name":""}],"inputs":[{"type":"uint256","name":"_amount"},{"type":"uint256[3]","name":"_min_amounts"},{"type":"bool","name":"_use_underlying"}],"stateMutability":"nonpayable","type":"function"},{"name":"remove_liquidity_imbalance","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256[3]","name":"_amounts"},{"type":"uint256","name":"_max_burn_amount"}],"stateMutability":"nonpayable","type":"function"},{"name":"remove_liquidity_imbalance","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256[3]","name":"_amounts"},{"type":"uint256","name":"_max_burn_amount"},{"type":"bool","name":"_use_underlying"}],"stateMutability":"nonpayable","type":"function"},{"name":"calc_withdraw_one_coin","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256","name":"_token_amount"},{"type":"int128","name":"i"}],"stateMutability":"view","type":"function"},{"name":"calc_withdraw_one_coin","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256","name":"_token_amount"},{"type":"int128","name":"i"},{"type":"bool","name":"_use_underlying"}],"stateMutability":"view","type":"function"},{"name":"remove_liquidity_one_coin","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256","name":"_token_amount"},{"type":"int128","name":"i"},{"type":"uint256","name":"_min_amount"}],"stateMutability":"nonpayable","type":"function"},{"name":"remove_liquidity_one_coin","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256","name":"_token_amount"},{"type":"int128","name":"i"},{"type":"uint256","name":"_min_amount"},{"type":"bool","name":"_use_underlying"}],"stateMutability":"nonpayable","type":"function"},{"name":"ramp_A","outputs":[],"inputs":[{"type":"uint256","name":"_future_A"},{"type":"uint256","name":"_future_time"}],"stateMutability":"nonpayable","type":"function","gas":151924},{"name":"stop_ramp_A","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":148685},{"name":"commit_new_fee","outputs":[],"inputs":[{"type":"uint256","name":"new_fee"},{"type":"uint256","name":"new_admin_fee"}],"stateMutability":"nonpayable","type":"function","gas":110521},{"name":"apply_new_fee","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":97302},{"name":"revert_new_parameters","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":21955},{"name":"commit_transfer_ownership","outputs":[],"inputs":[{"type":"address","name":"_owner"}],"stateMutability":"nonpayable","type":"function","gas":74693},{"name":"apply_transfer_ownership","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":60770},{"name":"revert_transfer_ownership","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":22045},{"name":"admin_balances","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256","name":"i"}],"stateMutability":"view","type":"function","gas":3541},{"name":"withdraw_admin_fees","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":14528},{"name":"donate_admin_fees","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":111449},{"name":"kill_me","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":38058},{"name":"unkill_me","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":22195},{"name":"claim_rewards","outputs":[{"type":"bool","name":""}],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":27334},{"name":"set_reward_claimant","outputs":[],"inputs":[{"type":"address","name":"_reward_claimant"}],"stateMutability":"nonpayable","type":"function","gas":37358},{"name":"set_reward_admin","outputs":[],"inputs":[{"type":"address","name":"_reward_admin"}],"stateMutability":"nonpayable","type":"function","gas":37388},{"name":"set_rewards","outputs":[],"inputs":[{"type":"address[8]","name":"_rewards"}],"stateMutability":"nonpayable","type":"function","gas":296715},{"name":"coins","outputs":[{"type":"address","name":""}],"inputs":[{"type":"uint256","name":"arg0"}],"stateMutability":"view","type":"function","gas":2400},{"name":"underlying_coins","outputs":[{"type":"address","name":""}],"inputs":[{"type":"uint256","name":"arg0"}],"stateMutability":"view","type":"function","gas":2430},{"name":"balances","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256","name":"arg0"}],"stateMutability":"view","type":"function","gas":2460},{"name":"fee","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2381},{"name":"admin_fee","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2411},{"name":"owner","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2441},{"name":"lp_token","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2471},{"name":"initial_A","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2501},{"name":"future_A","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2531},{"name":"initial_A_time","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2561},{"name":"future_A_time","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2591},{"name":"admin_actions_deadline","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2621},{"name":"transfer_ownership_deadline","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2651},{"name":"future_fee","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2681},{"name":"future_admin_fee","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2711},{"name":"future_owner","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2741},{"name":"reward_tokens","outputs":[{"type":"address","name":""}],"inputs":[{"type":"uint256","name":"arg0"}],"stateMutability":"view","type":"function","gas":2880},{"name":"reward_claimant","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2801},{"name":"reward_admin","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2831}]""")

