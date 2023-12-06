#Libraries 
library(readxl)
library(htmltools)
#install.packages('tidygeocoder')
library(tidygeocoder)
library(sf)
library(stringi)
library(stringr)
#library(giscoR)
library(ggplot2)
library(writexl)

# Defining work directory  
setwd('C:\\Users\\felipe.dias\\Documents\\Crimes e Doenças')

# Reading Excel with CEP + street names (logradouros) from hospitalization
cep_data <- read_excel('Outputs\\Hosp_CEPs_with_address.xlsx')

# Rename columns
names(cep_data) <- c('Street', "Neighborhood", 'City', 'CEP')

# Creating complete address columns
cep_data$complete_adress <- paste0(cep_data$Street,
                                   ", ",cep_data$Neighborhood,
                                   ", ",cep_data$City,
                                   ", ",cep_data$CEP)


#### Using the 'tidygeocoder' with method 'arcGIS' to geocode every address

# Breaking by 10000 addresses, because if an error occurs in the middle of the process, 
# the whole DataFrame is lost.

geo_code1 <- cep_data[1:10000,] %>%
  tidygeocoder::geocode(
    complete_adress,
    method = "arcgis",
    full_results = TRUE)

geo_code2 <- cep_data[10000:20000,] %>%
  tidygeocoder::geocode(
    complete_adress,
    method = "arcgis",
    full_results = TRUE)

geo_code3 <- cep_data[20000:30000,] %>%
  tidygeocoder::geocode(
    complete_adress,
    method = "arcgis",
    full_results = TRUE)

geo_code4 <- cep_data[30000:40000,] %>%
  tidygeocoder::geocode(
    complete_adress,
    method = "arcgis",
    full_results = TRUE)

geo_code5 <- cep_data[40000:50000,] %>%
  tidygeocoder::geocode(
    complete_adress,
    method = "arcgis",
    full_results = TRUE)

geo_code6 <- cep_data[50000:60000,] %>%
  tidygeocoder::geocode(
    complete_adress,
    method = "arcgis",
    full_results = TRUE)

geo_code7 <- cep_data[60000:70000,] %>%
  tidygeocoder::geocode(
    complete_adress,
    method = "arcgis",
    full_results = TRUE)


geo_code8 <- cep_data[70000:80000,] %>%
  tidygeocoder::geocode(
    complete_adress,
    method = "arcgis",
    full_results = TRUE)


geo_code9 <- cep_data[80000:nrow(cep_data),] %>%
  tidygeocoder::geocode(
    complete_adress,
    method = "arcgis",
    full_results = TRUE)

# Rbinding everything together
geo_code_total <- rbind(geo_code1,geo_code2, geo_code3, geo_code4,
                        geo_code5, geo_code6, geo_code7, geo_code8,
                        geo_code9)

# Removing duplicates
geo_code_total <- geo_code_total[!duplicated(geo_code_total), ]

# Saving
write_xlsx(geo_code_total, 'Outputs\\Hosp_CEPs_with_address_and_coord_tidygeocoder.xlsx')
