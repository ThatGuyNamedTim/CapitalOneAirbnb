import csv
import json
from flask import Flask, render_template, request
from geopy.distance import vincenty
import threading


listings = []
pieChartData = ''
barGraphNeighborhoodPriceData = ''
barGraphNeighborhoodReviewData = ''
finishData = 0


def makeWebApp():
    global listings
    global finishData
    global pieChartData
    global barGraphNeighborhoodPriceData
    global barGraphNeighborhoodReviewData

    #simple class for a given location
    class Listing:

        def __init__(self, zipCode, id, price, reviewScore, squareFoot, neighborhood, latitude, longitude, listingCount):
            #all the data that I use
            self.latitude = latitude
            self.longitude = longitude
            self.id = id
            self.zipCode = zipCode
            self.neighborhood = neighborhood
            self.price = 0
            self.reviewScore = 0 #start with 0
            self.squareFoot = 0
            self.listingCount = 0

            #now set the data to the actual values if they were properly filled in the form
            if (price != ''):
                self.price = float(price.replace('$','').replace(',',''))
            if (reviewScore != ''):
                self.reviewScore = float(reviewScore)
            if (squareFoot != '' and squareFoot != 0): #some squarefootage was most likely incorrect so it is filtered out
                try:
                    self.squareFoot = float(squareFoot)
                except:
                    pass
            if (listingCount != ''):
                try:
                    self.listingCount = float(listingCount)
                except:
                    pass




    #simple find method
    def find_listing(list, listingID):
        for n in list:
            if (n.id == listingID):
                return n

    #global listings  = [] storing Listing ojects in list

    #Two lists to calculate the pie graph of type of listings
    propertyTypes = []
    propertyTypesCounter = []

    #lists for calculating the review and pricing for neighborhoods
    #two different lists because not all listings with Prices and squarefeet will have reviews and viceversa
    neighborhoodsForReview = []
    neighborhoodsForPricing =[]

    with open('static/data/listings.csv') as csvFile:
        read = csv.reader(csvFile)
        next(read) #ignore header
        for row in read:
            if(row[51] != "Pension (Korea)"): #Pension (Korea) seemed like a fake listing from the other data
                if (row[43].startswith('9')):
                    #read data
                    if (row[51] != ''):
                        #for the pie of property types
                        propertyType = row[51]
                        try:
                            propertyTypesCounter[propertyTypes.index(propertyType)] = propertyTypesCounter[propertyTypes.index(propertyType)] + 1
                        except:
                            propertyTypes.append(propertyType)
                            propertyTypesCounter.append(1)

                    #read in data
                    zipCode = row[43].split('-')[0] #some are formated ####-####
                    listingID = row[0]
                    price = row[60]
                    squareFoot = row[59]
                    reviewScore = row[79]
                    squareFoot = row[59]
                    neighborhood = row[38]
                    latitude = row[48]
                    longitude = row[49]
                    listingCount = row[33]

                    #use data for the neighborhoods vs Price/SQFT
                    #some may have entered the squarefoot incorrectly so there are checked in if statement
                    if (neighborhood != '' and price != '' and price != 0 and squareFoot != '' and float(squareFoot) > 5):
                        if (any(n == neighborhood for n in neighborhoodsForPricing) != 1 and float(price.split('$')[1])/float(squareFoot) < 3):
                            neighborhoodsForPricing.append(neighborhood)


                    #use data for the neighborhoods vs Review
                    if (neighborhood != '' and len(neighborhood) < 30 and reviewScore != ''):
                        if (any(n == neighborhood for n in neighborhoodsForReview) != 1): #some people might have incorrect entries
                            neighborhoodsForReview.append(neighborhood)

                    if (any(n.id == listingID for n in listings) != 1):
                        listings.append(Listing(zipCode, listingID, price, reviewScore, squareFoot, neighborhood, latitude, longitude, listingCount))

    #Loops and storage for the cost per sqarefoot for a neighborhood calculations
    neighborhoodsPricing = [0] * len(neighborhoodsForPricing)
    neighborhoodsCounterPricing = [0] * len(neighborhoodsForPricing)

    for listing in listings:

        #some are probably entered wrong because more than 2 per foot is absurd, outliers or incorrect information
        if (listing.price != '' and listing.price != 0 and listing.squareFoot != '' and listing.squareFoot > 30 and listing.zipCode.startswith('9')
            and listing.neighborhood != ''   and listing.price/listing.squareFoot < 3):
            try:
                #long calculation due to long names, it is just calculatin average
                neighborhoodsPricing[neighborhoodsForPricing.index(listing.neighborhood)] = round(((neighborhoodsPricing[neighborhoodsForPricing.index(listing.neighborhood)] *
                                                            neighborhoodsCounterPricing[neighborhoodsForPricing.index(listing.neighborhood)]
                                                            + listing.price / listing.squareFoot)
                                                            /(neighborhoodsCounterPricing[neighborhoodsForPricing.index(listing.neighborhood)] + 1)),2)
                neighborhoodsCounterPricing[neighborhoodsForPricing.index(listing.neighborhood)] = neighborhoodsCounterPricing[neighborhoodsForPricing.index(listing.neighborhood)] + 1
            except:
                pass

    #Loops and storage for the average Reviews for a neighborhood calculations

    neighborhoodsReviews = [0] * len(neighborhoodsForReview)
    neighborhoodsCounterReviews = [0] * len(neighborhoodsForReview) #different than neighborhoodsCounterPricing because not all that have prices and squarefeet have reviews

    for listing in listings:
        if (listing.reviewScore != '' and listing.zipCode != '' and listing.neighborhood != '' and len(listing.neighborhood) < 30):
            try:
                #long calculation due to long names, it is just calculatin average
                neighborhoodsReviews[neighborhoodsForReview.index(listing.neighborhood)] = round(((neighborhoodsReviews[neighborhoodsForReview.index(listing.neighborhood)] *
                                                            neighborhoodsCounterReviews[neighborhoodsForReview.index(listing.neighborhood)]
                                                            + listing.reviewScore)
                                                            /(neighborhoodsCounterReviews[neighborhoodsForReview.index(listing.neighborhood)] + 1)),2)
                neighborhoodsCounterReviews[neighborhoodsForReview.index(listing.neighborhood)] = neighborhoodsCounterReviews[neighborhoodsForReview.index(listing.neighborhood)] + 1
            except:
                pass

    # create others for the type of listings because it is very cluttered due to some random listing types
    # care a final list of types which will include 'other' instead of less frequent types
    otherSum = 0
    propertyTypesFinal = []
    propertyTypesCounterFinal = []
    for index in range(0,len(propertyTypes) - 1):
        count = propertyTypesCounter[index]
        if (propertyTypesCounter[index] < 25):
            otherSum += count
        else:
            if (propertyTypes[index] == 'Other'):
                otherSum += count
            else:
                propertyTypesFinal.append(propertyTypes[index])
                propertyTypesCounterFinal.append(count)
    # add the other to the dataset
    propertyTypesCounterFinal.append(otherSum)
    propertyTypesFinal.append('Other')


    #create the data in JSON format
    pieChartData = json.dumps([{'Type': typeListing, 'Count': count} for typeListing, count in zip(propertyTypesFinal,propertyTypesCounterFinal)])
    barGraphNeighborhoodPriceData = json.dumps([{'Neighborhood': zipcode, 'Cost Per Square Foot': cost} for zipcode, cost in zip(neighborhoodsForPricing,neighborhoodsPricing)])
    barGraphNeighborhoodReviewData = json.dumps([{'Neighborhood': zipcode, 'Average Review': review} for zipcode, review in zip(neighborhoodsForReview,neighborhoodsReviews)])
    finishData = 1
    print('done')

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        print(finishData)
        if finishData == 1:
                return render_template('index.html',
                            pieChartListingType = pieChartData,
                            barGraphNeighborhoodPrice = barGraphNeighborhoodPriceData,
                            barGraphNeighborhoodReview = barGraphNeighborhoodReviewData)
        else:
            data = threading.Thread(target=makeWebApp)
            data.start()
            return render_template('loading.html')
        #when the site is first loaded, no forms submited

    else:
        #form input
        #the revuenue for week is using a 1 mi circle around the given point and the average price and the given number of listings per week
        #
        # the optimal price is using the price of the listing with the most listings in 1 mi radius
        # if there are multiple with same number of listings their prices are averaged

        givenLocation = (request.form['latitudeIn'], request.form['longitudeIn'])
        numHostWeek = request.form['numHostWeek']
        givenLocationCost = 0
        countForWeekly = 0

        count = 0
        optimalCost = 0
        currentMax = 0
        countForOptimal = 0
        for listing in listings:
            if (vincenty(givenLocation,(listing.latitude,listing.longitude)).miles < 1): #1 mile apart
                if (listing.price != '' and listing.price != 0):
                    givenLocationCost = (count * givenLocationCost + listing.price)/(count + 1)
                    count += 1

                    if (listing.listingCount > currentMax):
                        countForOptimal = 0
                        currentMax = listing.listingCount
                        optimalCost = listing.price
                        countForOptimal += 1
                    elif (listing.listingCount == currentMax):
                        optimalCost = (countForOptimal * optimalCost + listing.price)/(countForOptimal + 1)
                        countForOptimal += 1


        #if the input is bad (wrong location), there are if statement to check
        if (givenLocationCost == 0 or request.form['latitudeIn'] == ''):
            givenLocationCost = 'BAD INPUT'
        else:
            #convert the price to the price per week
            givenLocationCost = '$' + str(round(givenLocationCost * int(numHostWeek)))

        if (optimalCost == 0):
            optimalCost = 'BAD INPUT'
        else:
            optimalCost = '$' + str(round(optimalCost,2))

        #return the site with the form data results
        return render_template('index.html',
                            pieChartListingType = pieChartData,
                            barGraphNeighborhoodPrice = barGraphNeighborhoodPriceData,
                            barGraphNeighborhoodReview = barGraphNeighborhoodReviewData,
                            givenLocationCost = givenLocationCost,
                            optimalLocationCost = optimalCost)

if __name__ == '__main__':
    app.debug = True
    app.run()
