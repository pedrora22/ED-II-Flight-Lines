import json
import os
import threading


flights = {
    'FL100': {
        'origin': 'São Paulo (GRU)',
        'destination': 'Rio de Janeiro (SDU)',
        'airline_miles': 300,
        'plane_model': 'Boeing 737',
        'price': 350.00,
        'available_seats': 150
    },
    'FL254': {
        'origin': 'Belo Horizonte (CNF)',
        'destination': 'Salvador (SSA)',
        'airline_miles': 600,
        'plane_model': 'Airbus A320',
        'price': 780.00,
        'available_seats': 120
    },
    'FL301': {
        'origin': 'Porto Alegre (POA)',
        'destination': 'São Paulo (CGH)',
        'airline_miles': 400,
        'plane_model': 'Embraer E195',
        'price': 550.00,
        'available_seats': 10
    }
}

USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

# ------------------ B-Tree Implementation ------------------

class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Minimum degree
        self.leaf = leaf
        self.keys = []
        self.values = []
        self.children = []

    def search(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        if i < len(self.keys) and self.keys[i] == key:
            return self.values[i]
        if self.leaf:
            return None
        return self.children[i].search(key)

    def insert_non_full(self, key, value):
        i = len(self.keys) - 1
        if self.leaf:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            self.keys.insert(i + 1, key)
            self.values.insert(i + 1, value)
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key, value)

    def split_child(self, i):
        t = self.t
        y = self.children[i]
        z = BTreeNode(t, y.leaf)
        z.keys = y.keys[t:]
        z.values = y.values[t:]
        if not y.leaf:
            z.children = y.children[t:]
        y.keys = y.keys[:t - 1]
        y.values = y.values[:t - 1]
        if not y.leaf:
            y.children = y.children[:t]
        self.children.insert(i + 1, z)
        self.keys.insert(i, y.keys.pop())
        self.values.insert(i, y.values.pop())

class BTree:
    def __init__(self, t=2):
        self.t = t
        self.root = BTreeNode(t, True)

    def search(self, key):
        return self.root.search(key)

    def insert(self, key, value):
        r = self.root
        if len(r.keys) == 2 * self.t - 1:
            s = BTreeNode(self.t, False)
            s.children.append(r)
            s.split_child(0)
            self.root = s
            self._insert_non_full(s, key, value)
        else:
            self._insert_non_full(r, key, value)

    def _insert_non_full(self, node, key, value):
        node.insert_non_full(key, value)

    def traverse(self):
        result = []
        self._traverse(self.root, result)
        return result

    def _traverse(self, node, result):
        for i in range(len(node.keys)):
            if not node.leaf:
                self._traverse(node.children[i], result)
            result.append((node.keys[i], node.values[i]))
        if not node.leaf:
            self._traverse(node.children[-1], result)

# ------------------ User Management with B-Tree ------------------

_lock = threading.RLock()
_users_btree = None

def load_users_into_btree():
    global _users_btree
    with _lock:
        _users_btree = BTree(t=2)
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                users = json.load(f)
                for email, data in users.items():
                    _users_btree.insert(email, data)

def find_user_by_email(email):
    with _lock:
        if _users_btree is None:
            load_users_into_btree()
        return _users_btree.search(email)

def save_user_data(email, password, role):
    global _users_btree
    with _lock:
        if _users_btree is None:
            load_users_into_btree()
        _users_btree.insert(email, {'password': password, 'role': role})
        # Reescreve o arquivo inteiro com os dados da árvore
        users_dict = {k: v for k, v in _users_btree.traverse()}
        with open(USERS_FILE, 'w') as f:
            json.dump(users_dict, f, indent=4)
    return True

def delete_user_data(email):
    # Remover de Árvore B é mais complexo, então aqui apenas remove do arquivo e recarrega a árvore
    global _users_btree
    with _lock:
        if not os.path.exists(USERS_FILE):
            return False
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        if email not in users:
            return False
        del users[email]
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
        # Recarrega a árvore
        load_users_into_btree()
    return True

def get_all_users():
    with _lock:
        if _users_btree is None:
            load_users_into_btree()
        return {k: v for k, v in _users_btree.traverse()}
