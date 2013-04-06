#!/usr/bin/env Rscript
# Andrew Borgman
# 3/7/2013
# Analysis and figures for grant report
library(lattice)
library(ggplot2)
library(forecast)
library(timeSeries)
library(stringr)
library(lubridate)
library(RColorBrewer)
library(reshape)
library(KernSmooth)
source("~/multiplot.R")

# Grab monthly files
data_dir = "~/wind_data/raw_data/"
files = str_c(data_dir, dir(data_dir))
files = files[-grep("all", files)] # get rid of big one

for (f in files){
  
  # Read in, label, and convert
  dat = read.table(f, sep="\t")
  names(dat) = c("Time", "RG1", "RG2", "RG3", "RG4","RG5", "RG6","AN1", "AN2")
  
  for (k in 1:20){
    
    # Grab random start
    start = sample(length(dat[,1]),1)
    end = start + 2100
    
    # Melt it!
    dat_long = melt(dat[start:end, ])
    dat_long[,1] <- as.POSIXct(strptime(dat_long[,1], format="%Y/%m/%d %H:%M:%S"))
    names(dat_long) = c("Time", "Sensor", "Speed")
    
    # Make some sex rectangles
    start_time = dat_long[1,1]
    rect_left = start_time + dminutes(seq(0,30,10)) 
    rectangles <- data.frame(
      xmin = rect_left,
      xmax = rect_left + dminutes(5),
      ymin = 0 ,
      ymax = max(dat_long$Speed) + 0.25
    )
    
    # Sex colors
    cols = c("#FF7F00", "#F781BF", "#377EB8", "#E41A1C", "#FFFF33", "#4DAF4A", "#A65628", "#984EA3")

    image_file_name = str_c("~/projects/grant_work/images/",str_split(str_split(f, "/")[[1]][3], ".tsv")[[1]][1], k,".svg" )
    p = ggplot() + geom_rect(data=rectangles, aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax), fill='gray80', alpha=0.3) + 
          geom_line(data=dat_long,aes(x=Time, y=Speed, colour=Sensor), size=1, alpha=.8) + 
          scale_colour_manual(values=cols) + theme_bw(22) + ylab("Speed (m/s)") + ggtitle("Wind Speeds for All Sensors") +
          ylim(0,max(dat_long$Speed) + 0.25) + theme(panel.border = element_rect(colour = "black", size=2), axis.ticks = element_line(size=1.25),
          panel.grid.major = element_blank(), panel.grid.minor = element_blank())
    ggsave(filename=image_file_name,  plot=p, width=8, height=5)
    
  }  
}


# Grab random start
start = sample(length(dat[,1]),1)
end = start + 2100

# Melt it!
dat_long = melt(dat[start:end, ])
dat_long[,1] <- as.POSIXct(strptime(dat_long[,1], format="%Y/%m/%d %H:%M:%S"))
names(dat_long) = c("Time", "Sensor", "Speed")
dat_long$lagger = c(0, diff(dat_long$Speed))

test = dat[start:end, ]
test[,1] <- as.POSIXct(strptime(test[,1], format="%Y/%m/%d %H:%M:%S"))
h = dpill(dat[,1], dat[,2], gridsize = 600)
fit = locpoly(test[,1],test[,2], bandwidth=h)

# Make some sex rectangles
start_time = dat_long[1,1]
rect_left = start_time + dminutes(seq(0,30,10)) 
rectangles <- data.frame(
  xmin = rect_left,
  xmax = rect_left + dminutes(5),
  ymin = 0 ,
  ymax = max(dat_long$Speed) + 0.25
)

# Sex colors
cols = c("#FF7F00", "#F781BF", "#377EB8", "#E41A1C", "#FFFF33", "#4DAF4A", "#A65628", "#984EA3")


p1 = ggplot() + geom_rect(data=rectangles, aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax), fill='gray80', alpha=0.3) + 
  geom_line(data=dat_long,aes(x=Time, y=Speed, colour=Sensor), size=1, alpha=.8) + 
  scale_colour_manual(values=cols) + theme_bw(22) + ylab("Speed (m/s)") + ggtitle("Wind Speeds for All Sensors") +
  ylim(0,max(dat_long$Speed) + 0.25) + theme(panel.border = element_rect(colour = "black", size=2), axis.ticks = element_line(size=1.25),
                                             panel.grid.major = element_blank(), panel.grid.minor = element_blank())

rectangles_lag <- data.frame(
  xmin = rect_left,
  xmax = rect_left + dminutes(5),
  ymin =  min(dat_long$lagger) - 0.02,
  ymax = max(dat_long$lagger) + 0.02
)


p2 = ggplot() + geom_rect(data=rectangles_lag, aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax), fill='gray80', alpha=0.3) + 
      geom_line(data=dat_long,aes(x=Time, y=lagger, colour=Sensor), size=1, alpha=.8) + 
      scale_colour_manual(values=cols) + theme_bw(22) + ylab("Speed (m/s)") + ggtitle("Wind Speeds for All Sensors") +
      ylim(min(dat_long$lagger) - 0.02,max(dat_long$lagger) + 0.05) + theme(panel.border = element_rect(colour = "black", size=2), axis.ticks = element_line(size=1.25),
                                             panel.grid.major = element_blank(), panel.grid.minor = element_blank())

multiplot(p1,p2)


