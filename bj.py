import numpy as np

global allCards
global player
global dealer
global remainingCards

def shuffleDeck():
    numDecks = 8
    deck = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10])
    global remainingCards
    remainingCards = np.array([numDecks*4, numDecks*4, numDecks*4, numDecks*4, numDecks*4, numDecks*4, numDecks*4, numDecks*4, numDecks*4, numDecks * 16])
    global allCards
    allCards = np.array([])
    for i in range(0, numDecks):
        allCards = np.append(allCards, deck)
    np.random.shuffle(allCards)


def deal():
    global player
    global dealer
    global allCards
    hand = np.array([])
    dealer = np.array([])
    hand = hit(hand)
    dealer = hit(dealer)
    hand = hit(hand)
    dealer = hit(dealer)
    player = [hand]

def hitDontShow(person):
    global allCards
    person = np.append(person, allCards[-1])
    allCards = allCards[:-1]
    return person

def hit(person):
    global allCards
    person = np.append(person, allCards[-1])
    print(int(allCards[-1]))
    remainingCards[int(allCards[-1])-1] -= 1
    allCards = allCards[:-1]
    return person

def split(handIndex):
    global player
    hand = player[handIndex]
    del player[handIndex]
    newHand1 = np.array([hand[0]])
    newHand2 = np.array([hand[1]])
    hit(newHand1)
    hit(newHand2)
    player.append(newHand1)
    player.append(newHand2)

def calcHitOdds(remainingCards, hand, dealerCard, removeCardIndex):
    if removeCardIndex > -1:
        remainingCards[removeCardIndex] -= 1
        hand = np.append(hand, removeCardIndex + 1)
    total = np.sum(remainingCards)
    hitEv = 0
    for i in range(0, 10):
        if remainingCards[i] == 0:
            continue
        if i + 1 + np.sum(hand) > 21:
            hitEv -= (remainingCards[i]/total)
        else:
            handTotal = np.sum(hand)
            if handTotal < 12 and np.isin(1, hand):
                handTotal += 10
            hitEv += (remainingCards[i]/total) * max(calcHitOdds(remainingCards, hand, dealerCard, i), \
                calcStandOdds(remainingCards, handTotal, dealerCard, removeCardIndex, dealerCard==1))
    return hitEv

def calcStandOdds(remainingCards, handTotal, dealerCard, removeCardIndex, hasA):
    standEv = 0
    if removeCardIndex > -1:
        remainingCards[removeCardIndex] -= 1
    total = np.sum(remainingCards)
    for i in range(0,10):
        if remainingCards[i] == 0:
            continue
        if i + 1 + dealerCard > 21:
            standEv += remainingCards[i]/total
        elif i + 1 + dealerCard < 12 and i + 1 + dealerCard > 6 and (i == 0 or hasA):
            if handTotal > i + 11 + dealerCard:
                standEv += remainingCards[i]/total
            elif handTotal < i + 11 + dealerCard:
                standEv -= remainingCards[i]/total
        elif i + 1 + dealerCard > 16:
            if handTotal > i + 1 + dealerCard:
                standEv += remainingCards[i]/total
            elif handTotal < i + 1 + dealerCard:
                standEv -= remainingCards[i]/total
        else:
            standEv += remainingCards[i]/total * calcStandOdds(remainingCards, handTotal, dealerCard + i + 1, i, hasA or i == 0)
    return standEv

    
def calculateOdds(remainingCards, hand, dealerCard, removeCardIndex):
    hitEv = calcHitOdds(remainingCards, hand, dealerCard, removeCardIndex)
    handTotal = np.sum(hand)
    if handTotal < 12 and np.isin(1, hand):
        handTotal += 10
    standEv = calcStandOdds(remainingCards, handTotal, dealerCard, removeCardIndex, dealerCard == 1)

    doubleEv = 0
    splitEv = 0
    if len(hand) == 2:
        doubleEv = 0
        if hand[0] == hand[1]:
            splitEv = 0
    return hitEv, standEv


shuffleDeck()
deal()
print(player)
print(dealer)
print(calculateOdds(remainingCards, player[0], dealer[0], -1))