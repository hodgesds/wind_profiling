#!/usr/bin/env Rscript
# Andrew Borgman
# 3/14/2013
# Attempt @ programatically locating regions with poor data
# Also need to check on the imputation of anenometer values of 0
library(lattice)
library(ggplot2)
library(data.table)
library(forecast)
library(timeSeries)
library(stringr)
library(lubridate)
library(RColorBrewer)
library(reshape)
source("~/multiplot.R")
source("~/Dropbox/NRG/grant_work/r_src/wind_functions.R")

# Grab monthly files
data_dir = "~/wind_data/raw_data/"
files = str_c(data_dir, dir(data_dir))
files = files[-grep("all", files)] # get rid of big one

dat = read.table(files[1], sep="\t")
names(dat) = c("Time", "RG1", "RG2", "RG3", "RG4","RG5", "RG6","AN1", "AN2")
dat[,1] <- as.POSIXct(strptime(dat[,1], format="%Y/%m/%d %H:%M:%S"))
#dat = data.table(dat)

head(dat)

# Impute anenometer data -- FINISH THIS FUNCTION
dat = impute_anenometer_data(dat)

# Testing different methods for 


  
# Look for regions where there is too much change or not enough change in wind speed
# These are the areas with poor data

tmp = dat$RG1
lagger = diff(x=tmp)
mean(lagger)
sd(lagger)

