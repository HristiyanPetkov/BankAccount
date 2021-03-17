import random
import os
import yaml

code = "abcdefghijklmnopqrstuvwxyz0123456789"

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def get_balance(self):
        print(self.balance)
        return self.balance


class Client():

    num_clients = 0

    def __init__(self, account_path, client_id=None, balance=None):
        Client.num_clients += 1
        self.account_id = []
        self.bank_accounts = []
        self.num_accounts = 0
        self.account_path = account_path

        if os.path.exists(account_path):
            with open(self.account_path, 'r') as file:
                self.account_dict = yaml.full_load(file)
                self.client_id = client_id
            if self.client_id in self.account_dict.keys():
                self.num_accounts = len(self.account_dict[self.client_id])
                self.account_id.extend(self.account_dict[self.client_id])
                self.bank_accounts.extend(self.account_dict[self.client_id])
            else:
                self.client_id = ''
                for i in range(8):
                    self.client_id += random.choice(code)
                self.add_bank_account(balance)
                self.account_dict.update({self.client_id : i for i in self.bank_accounts})
                with open(self.account_path, "a") as file:
                    yaml.dump({self.client_id : [i for i in self.bank_accounts]}, file)

        else:
            self.add_bank_account(balance)  
            self.client_id = ""
            for i in range(8):
                self.client_id += random.choice(code)
            self.account_dict = {self.client_id:self.bank_accounts[0]}
            with open(account_path, "w") as fw:
                yaml.dump(self.account_dict, fw)

    def add_bank_account(self, amount, mod=False, account_id=None):
        b = BankAccount(amount)

        account_id = ''
        account_id = random.randint(100000, 999999)
        self.account_id.append(account_id)
        self.bank_accounts.append({self.account_id[self.num_accounts]: b.balance})
        self.num_accounts += 1

        if mod:
            with open(self.account_path, "r") as fr:

                self.account_dict = yaml.load(fr, Loader=yaml.FullLoader)
                self.account_dict[self.client_id] = self.bank_accounts

                with open(self.account_path, "w") as fw:
                    yaml.dump(self.account_dict, fw)

    def deposit(self, amount, account_id): 
        if not self.bank_accounts:
            raise ValueError("No bank accounts")
        with open(self.account_path, "r") as fr:
            self.account_dict = yaml.load(fr, Loader=yaml.FullLoader)
        for y in range(0, self.num_accounts):
                for i in self.account_dict[self.client_id][y].keys():
                    if i == account_id:
                        self.account_dict[self.client_id][y][account_id] += amount
                    break
        with open(self.account_path, "w") as fw:
            yaml.dump(self.account_dict, fw)

    def withdraw(self, amount, account_id):
        if not self.bank_accounts:
            raise ValueError("No bank accounts")
        with open(self.account_path, "r") as fr:
            self.account_dict = yaml.load(fr, Loader=yaml.FullLoader)
        for y in range(0, self.num_accounts):
            for i in self.account_dict[self.client_id][y].keys():
                if i == account_id:
                    if amount > self.account_dict[self.client_id][y][account_id]:
                        raise ValueError("Not enought money")
        else:
            for y in range(0, self.num_accounts):
                for i in self.account_dict[self.client_id][y].keys():
                    if i == account_id:
                        self.account_dict[self.client_id][y][account_id] -= amount
                    break
            with open(self.account_path, "w") as fw:
                yaml.dump(self.account_dict, fw)

    def transfer(self, account1_id, client, account2_id, amount, operation="deposit"):
        if not isinstance(client, Client):
            print("Not a client")
            return
        if operation == "deposit":
            client.withdraw(amount, account2_id)
            with open(self.account_path, "r") as fr:
                self.account_dict = yaml.full_load(fr)
            self.deposit(amount, account1_id)
        elif operation == "withdraw":
            with open(self.account_path, "r") as fr:
                self.account_dict = yaml.full_load(fr)
            self.withdraw(amount, account1_id)
            client.deposit(amount, account2_id)
        else:
            raise ValueError("No such function")

client1 = Client("Smetka.yaml", "1nd4hxwq")
# client1.add_bank_account(2000, True)
client2 = Client("Smetka.yaml", "f7w87dqm")
# client2.add_bank_account(2000, True)
client2.transfer(214742, client1, 128098, 500, "withdraw")