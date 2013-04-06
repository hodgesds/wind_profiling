  #!/usr/bin/env Rscript
# Andrew Borgman
# 3/14/2013
# Helper functions for wind analysis

# Takes in data frame with our standard aggregated format 
# and returns a data with all 0 values from the anenometer 
# imputed. If only one sensor is missing, impute with the data from
# the other sensor. If both are missing, could use average of values on either
# side (e.g. sensor 1 prev, sensor 2 prev, sensor 1 post, sensor 2 post).
# But sometimes you get long runs of missing data... Need to figure
# out what to do here
impute_anenometer_data <- function(data_frame){
  
  # Get indicies for all missing data
  an1_sel = which(data_frame$AN1 == 0) 
  an2_sel = which(data_frame$AN2 == 0) 
  both_missing = intersect(an1_sel, an2_sel) 
  
  # Impute values where only one sensor is missing
  data_frame$AN1[an1_sel[-which(an1_sel %in% both_missing)]] = data_frame$AN2[an1_sel[-which(an1_sel %in% both_missing)]]
  data_frame$AN2[an2_sel[-which(an2_sel %in% both_missing)]] = data_frame$AN1[an2_sel[-which(an2_sel %in% both_missing)]]
  
  # Impute values where both are missing
  # STILL NEED TO DO THIS...
  
  # Give it back, yo
  return(data_frame)  
  
}

