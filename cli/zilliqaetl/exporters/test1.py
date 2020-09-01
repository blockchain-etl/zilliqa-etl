from pyzil.account import Account

acc = Account(address='7Aa7eA9f4534d8D70224b9c2FB165242F321F12b')
print(acc.bech32_address)

acc = Account(public_key='039fbf7df13d0b6798fa16a79daabb97d4424062d2f8bd4e9a7c7851e732a25e1d')
print(acc.bech32_address)
