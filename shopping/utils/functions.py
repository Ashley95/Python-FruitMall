import random


def get_ticket():
    s = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    ticket = ''
    for i in range(28):
        ticket += random.choice(s)
    ticket =  'TK_' + ticket
    return ticket

