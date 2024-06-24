# Geocoding-Addresses
An example of geocoding addresses with tidygeocoder in R and by web scraping Google Maps using Selenium in Python

In this repository, I added a R script (Geocoding with Tidygeocoder.R), a Python script (Geocoding with Google Maps.py), an input dataset (Zipcodes_with_address.xlsx), and two output datasets (Zipcodes_with_address_with_coord_tidygeocoder.xlsx and Zipcodes_with_address_with_coord_Google_Maps.xlsx). This example may help people to understand how the tidygeocoder library works and how it is also possible to use Google Maps for geolocalizing. This example uses Brazilian addresses. In general, tidygeocoder is definity the better option, but it doesn't have access to all places that Google maps has. So for example, you you need to geolocate the townhall of a county, maybe tidygeocoder will not return a good match, but Google Maps will be able to localize it. 

The syntax of tidygeocoder is quite simple. In it, you can use various 'geocoding services' such as Google or Bing, but these require a key. I use arcGIS because it is free and provides very satisfactory results, as you can see in the output dataset. Library documentation: https://jessecambon.github.io/tidygeocoder/?search-input=geocode

For web scraping Google Maps, I use Selenium and take advantage of the geographic coordinnates that Google Maps displays in its URL. Yhe code is a little bit more complicated, but hopefully it is commented enough.

Hope this can help someone
