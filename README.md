# CapitalOneAirbnb : https://capitalbnb.herokuapp.com/
This is a website that was created for the Capital One Software Engineering Summit (Jan 2018). It will take a while to load the first time because the server is most likely not running due to inactivity which triggers the free Heroku hosting to shut it down. This slowdown is not due to the app, it is due to the free hosting service. 

It was created with all of the following:

* Flask
  * This was used for the backend of the project
  * I used multiple things within python such as 
    * threading
    * geopy
      * Used for finding distances using longitudes and latitudes 
* amCharts
  * This was used for graphing the data
  
## Base Objectives 

* There are three graphs near the bottom of my webpage
  * A bar graph of price vs Neighborhood
  * A bar graph of ratings vs Neighborhood
  * A pie graph of the types of listings
* Given a location I am able to calculate the potential earnings
  * A number of days that the location will be listed is asked to improve accuracy
  * The price per day is used by taking an average of other listings in a radius around the given location
* Given a location I am able to calculate the potential earnings
  * it is calculated by using the price of the listing in a radius around the location with the most listings

## Optional Objectives

* There are animations in the charts from amCharts
* The chart with rating vs neighborhood shows the most popular neighborhoods


