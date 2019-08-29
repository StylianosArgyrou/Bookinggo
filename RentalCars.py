import sys
import requests
import json
import ast

url = "https://techtest.rideways.com/dave"
suppliers = ["dave", "eric", "jeff"]
typeOfCar = {
  "STANDARD": 4,
  "EXECUTIVE": 4,
  "LUXURY": 4,
  "PEOPLE_CARRIER": 6,
  "LUXURY_PEOPLE_CARRIER": 6,
  "MINIBUS": 16
}

def connect(list):

	params = {
	    "pickup": list[1]+","+list[2],
	    "dropoff": list[3]+","+list[4]
	}
	min = list[5]
	max  = list[6]


	try:
		for supp in suppliers:

			options = get_options(supp, params)

			nextOptions = maximumPassengers(options,min, max)

			print_options(supp, options)
	except Exception as ex:
		print("An error occured with the supplier: ", supp)
		exit()

def print_options(supplier, options):
  for (car_type, price) in options.items():
      print("{} - {} - {}".format(car_type, supplier, price))


def get_options(supplier, params):

	try:
		response = requests.get(url, params=params, timeout=2)
		if response.ok:
			body = response.json()
			return { option['car_type']:option['price'] for option in body['options'] }
		else:
			print ("Error occured! Please try again!")
			exit()

	except Exception as e:
		print("Could not retrieve options from supplier " + supplier)

def maximumPassengers(options, min_passengers, max_passengers):
  filtered = dict()
  for (car_type, price) in options.items():
    passengers = typeOfCar[car_type]
    minValid = int(min_passengers) >= passengers
    maxValid = int(max_passengers) <= passengers
    if minValid and maxValid:
      filtered[car_type] = price
  return filtered


def main(argv):

    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))

    li = []
    
    stringList = str(sys.argv).replace("[", "").replace("\'", "").replace("]", "")
    stringList = stringList.replace(" ", "")
    print (stringList)

    list = stringList.split(",")

    print (list)

    while("" in list):
    	list.remove("")

    connect(list)

if __name__ == "__main__":
    main(sys.argv)
