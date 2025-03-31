# blockchain.py (Estrutura básica)
class MobileCoinWallet:
    def __init__(self):
        self.balances = {}  # Dicionário temporário

    def get_balance(self, user_id):
        # Implemente aqui a conexão real com a blockchain depois
        return self.balances.get(user_id, 0)

# Instância global
wallet = MobileCoinWallet()
