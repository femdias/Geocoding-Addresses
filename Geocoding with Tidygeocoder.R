#Libraries 
library(readxl)
#install.packages('tidygeocoder')
library(tidygeocoder)
library(dplyr)
library(stringr)
library(sf)
library(stringi)
library(writexl)

# Defining work directory  
setwd('C:\\Users\\femdi\\Documents\\GitHub\\Geocoding')

# Reading Excel with CEP + street names (logradouros) from hospitalization
df <- read_excel('Zipcodes_with_address.xlsx')


###############################################################################
# Creating "Search string" variable
###############################################################################

# Function to create the search string
create_search_string <- function(street, neighborhood, city) {
  # Split the street by ' - '
  list_str <- strsplit(street, ' - ')[[1]]
  
  # Initialize the string variable
  string <- ""
  
  if (length(list_str) > 1) {
    # Try to select only numbers
    tryCatch({
      # Replace common substrings to isolate only a number of the address
      nums <- as.numeric(unlist(strsplit(gsub('de |/|até ', ',', list_str[2]), ',')))
      nums <- nums[!is.na(nums)]
      
      # Final String
      if (length(nums) > 0) {
        string <- paste0(list_str[1], ", ", nums[1] + 1, ' - ', neighborhood, ", ", city)
      } else {
        string <- paste0(list_str[1], ' - ', neighborhood, ", ", city)
      }
    }, error = function(e) {
      string <- paste0(list_str[1], ' - ', neighborhood, ", ", city)
    })
  } else {
    string <- paste0(list_str[1], ' - ', neighborhood, ", ", city)
  }
  return(string)
}

# Apply the function to each row in the data frame
df <- df %>%
  rowwise() %>%
  mutate(Search_string = create_search_string(Street, Neighborhood, City)) %>%
  ungroup()


###############################################################################
#Using the 'tidygeocoder' with method 'arcGIS' to geocode every address
# Documentation: https://jessecambon.github.io/tidygeocoder/?search-input=geocode
###############################################################################


df_result <- df %>% tidygeocoder::geocode(Search_string,
                    method = "arcgis", full_results = TRUE)

# Saving
write_xlsx(df_result, 'Zipcodes_with_address_with_coord_tidygeocoder.xlsx')
