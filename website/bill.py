
# calculator function
# INPUT -> list of transactions
#   each transaction -> user(name) + expense(remarks) + cost(dollar)
'''
	transactions = [
 		{"user": "Sam", "cost":25, remarks:""}
   		.
		.
	oh ya i wanted to ask you the backend logic should be in main.py ah ? not app.py?		
 Yea it should be in a separate python file
 I would name it like "formula.py" or smth
 auGH
I EXPECT A COMPLETE REPORT OF THIS CODE Y TONIGHT
then what should be in app.py 
ok here's how i wld structure it
main.py -> the entry point of the application
app.py -> the app routes / view routes
bill.py calculation of the bill
db.py -> for storing / reading from] the database of transactions
login.py -> for logging in etc.
  		. right okok later i go try do hang men game to upload to github
    uhhh tonight 9 pm again? <3
		yus 9pm :D
	ok i need go bake now



ake for me ?
 
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
def calculate(transactions):
	
	paymentByEachUser = {}  # dict
	for tx in transactions:
		currentUser = tx["user"]
    #to filter unique user
		if currentUser not in paymentByEachUser:
			paymentByEachUser[currentUser] = 0
    #tie the cost to the user
		paymentByEachUser[currentUser] += tx["cost"]

  #total transaction
	totalCost = 0
	for tx in transactions:
		totalCost += tx["cost"]

	costPerUser = totalCost / len(paymentByEachUser)
	
	# BILL SPLITTING

	# sort by ascending
	paymentByEachUser = sorted(paymentByEachUser.items(), key=lambda x:x[1])
	# normalize deducting costPerUser
	paidArray = [val - costPerUser for val in list(paymentByEachUser.values())]
  #to allow drawing of name of the keys in the dict
	names = [name for name in list(paymentByEachUser.keys())]
	#["Sam", "TZ", "KJ"]

	amountReturnByUser = [{} for _ in range(len(paidArray))]
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
			amountReturnByUser[payeeIdx][excessName] = excessAmt
			balance = excessAmt - abs(payeeAmt)
			excessIdx -= 1
		# case 2: excess not fully paid up (can fill)
		elif excessAmt > abs(payeeAmt):
			amountReturnByUser[payeeIdx][excessName] = abs(payeeAmt)
			balance = excessAmt - abs(payeeAmt)
			# go to next lacking fella
      payeeIdx += 1
		# case 3: just nice (exact fill)
		else:
			amountReturnByUser[payeeIdx][excessName] = excessAmt
			balance = 0
			excessIdx -= 1
			payeeIdx +=1

	bill = {}
	for i in range(len(names)):
    bill[names[i]]=amountReturnByUser[i]

  return bill
    

	