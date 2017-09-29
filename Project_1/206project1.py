import os
import filecmp
from operator import itemgetter
from datetime import datetime
from datetime import date

import csv


def getData(file):
	lst =[]
	with open(file, 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			d = dict(row)
			lst.append(d)
	return lst

def mySort(data,col):
	 x = sorted(data,key= itemgetter(col))
	 person = x[0]
	 return(person["First"] + " " +person["Last"])


def classSizes(data):
	d = {}
	for cl in data:
		d[cl['Class']]= d.get(cl['Class'],0) + 1
	class_list = d.items()
	return sorted(class_list, key = lambda tup: tup[1], reverse = True)

def findDay(a):
	d = {}
	#check tuples slides - slide 13
	for day in a:
		d[int(day["DOB"].split("/")[1])] = d.get(int(day["DOB"].split("/")[1]), 0) + 1



	lst = list(d.items())
	lst_1 = sorted(lst, key = lambda x: x[1], reverse = True)
	return int(lst_1[0][0])

def findAge(a):
	lst = []
	for d in a:
		date = d["DOB"]
		today = datetime.today()
		born = datetime.strptime(date,'%m/%d/%Y')
		lst.append(today.year - born.year - ((today.month, today.day) < (born.month, born.day)))
	print (sum(lst)/len(lst))


def mySortPrint(a,col,fileName):
	x = sorted(a,key= itemgetter(col))
	f = open(fileName, 'w')
	person = x[0]
	for person in x:
		f.write(person["First"] + "," +person["Last"] + "," +person["Email"] +"\n")
	f.close()

	#c = Counter
	#loop through data
	# for d in data:
	# with get avoid errors - always be clean data and it will loop through
	#d.get(K,o)+1  a counter is similar
	# c[]+=1
	# data is a huge list in dictionary a single list of multiple dictionaries - F, L, Class, DOB, Email
	# we are counting the class - senior 2, junior 1 - data structure is not attached
	#c [d['class']] += 1
	#c = Counter
	#for d in data:
	#	c[d['class']] += 1
	#print c



################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ",end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),40)
	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',15)
	total += test(mySort(data2,'First'),'Adam Rocha',15)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',15)
	total += test(mySort(data2,'Last'),'Elijah Adams',15)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',15)
	total += test(mySort(data2,'Email'),'Orli Humphrey',15)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],10)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],10)

	print("\nThe most common day of the year to be born is:")
	total += test(findDay(data),13,10)
	total += test(findDay(data2),26,10)

	print("\nThe average age is:")
	total += test(findAge(data),39,10)
	total += test(findAge(data2),41,10)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,10)


	print("Your final score is: ",total)
# Standard boilerplate to call the main() function that tests all your code.
if __name__ == '__main__':
    main()
