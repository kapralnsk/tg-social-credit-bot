from collections import namedtuple


Transaction = namedtuple('Transaction', 'amount message_template')
TRANSACTIONS = {
    '😄': Transaction(20, 'Good! {username} Social Credit Score is now {score}'),
    '😞': Transaction(-20, 'Public shame! {username} Social Credit Score is now {score}'),
}
