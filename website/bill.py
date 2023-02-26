
# calculator function
# INPUT -> list of transactions
#   each transaction -> user(name) + expense(remarks) + cost(dollar)
'''
  transactions = [
     {"user": "Sam", "cost":25, remarks:""}
  ]

'''
# OUTPUT -> dictionary of payments
'''
  {
     "Sam":{}
     "TZ":{"Sam":value}
     "KJ":{"Sam":value, "TZ":value}
  }

'''
def calculate(transactions, users):
  
  paymentByEachUser = {}  # dict
  for tx in transactions:
    currentUser = tx["user"]
    #to filter unique user
    if currentUser not in paymentByEachUser:
      paymentByEachUser[currentUser] = 0
    #tie the cost to the user
    paymentByEachUser[currentUser] += tx["cost"]
  #even if user did not pay for anything, have to add user to count so set value of that user paid to 0
  for user in users:
    if user not in paymentByEachUser:
      paymentByEachUser[user] = 0

  #total transaction
  totalCost = 0
  for tx in transactions:
    totalCost += tx["cost"]

  costPerUser = totalCost / len(paymentByEachUser)
  
  # BILL SPLITTING

  # sort by ascending
  tuplesArray = sorted(paymentByEachUser.items(), key=lambda x: x[1])
  
  # normalize deducting costPerUser
  paidArray = [tup[1] - costPerUser for tup in tuplesArray]
  #to allow drawing of name of the keys in the dict
  names = [tup[0] for tup in tuplesArray]
  #["Sam", "TZ", "KJ"]

  bill = {name:{} for name in names}
  # [{}, {"Sam":5}, {"Sam": 10, "TZ":8}]

  payeeIdx = 0
  excessIdx = len(paidArray) - 1
  balance = 0
  while payeeIdx < excessIdx:

    payeeAmt = paidArray[payeeIdx]
    excessAmt = paidArray[excessIdx]

    # names of people
    excessName = names[excessIdx]
    payeeName = names[payeeIdx]
    #less people lacking as need to draw excess from others to fill up to costPerUser
    if balance < 0: 
      payeeAmt = balance
      #more people lacking as still have excess from top payer to fill up next index
    elif balance > 0: 
      excessAmt = balance
    # case 1: payee has balance remaining (cannot fill)
    if excessAmt < abs(payeeAmt):
      # payee already return X amt to excess
      # but payee owes Y amt and Y > X
      bill[payeeName][excessName] = excessAmt
      bill[excessName][payeeName] = -excessAmt
      balance = excessAmt - abs(payeeAmt)
      excessIdx -= 1
    # case 2: excess not fully paid up (can fill)
    elif excessAmt > abs(payeeAmt):
      bill[payeeName][excessName] = abs(payeeAmt)
      bill[excessName][payeeName] = -abs(payeeAmt)
      balance = excessAmt - abs(payeeAmt)
      # go to next lacking fella
      payeeIdx += 1
    # case 3: just nice (exact fill)
    else:
      bill[payeeName][excessName] = excessAmt
      bill[excessName][payeeName] = -excessAmt
      balance = 0
      excessIdx -= 1
      payeeIdx +=1


  return bill
    

  