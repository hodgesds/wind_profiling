require(TTR)
require(ttrTests)
require(quantmod)
require(fts)
require(forecast)
require(nlme)
require(fracdiff)
library(wavelets)
library(forecast)
library(its)
library(timeSeries)
library(pnmath)
work=read.table('all_2012.tsv',sep='\t',header=F)
nrow(work)
# number of obs 22740021
work$time <- as.POSIXct(strptime(work[,1],format="%Y/%m/%d %H:%M:%S"))
head(work)
work=xts(work[,2:9],work$time)
#trimmed <- work[,c("time", "rg1", "rg2", "rg3", "rg4", "rg5", "rg6","an1","an2")]
#work <- trimmed
summary(work)
mmean=apply.monthly(work,summary)

apply.daily(work,print(lm (work$V8~work$V2+work$V3+work$V4+work$V5+work$V6+work$V7)))
periodicity(work)
mdat=split.xts(work,f="months")
samp=work
plot.ts(as.ts(samp))
names(samp)=c('RG1','RG2','RG3','RG4','RG5','RG6','AN1','AN2')

fit=tbats(tsamp[1:3000,5],seasonal.periods=180,use.arma.errors=T,use.parallel=T,use.box.cox=F,use.trend=T)
ffit=forecast(fit,h=3000)

plot(fit)
summary(fit)
plot(forecast(fit,h=3000))

head(samp)
par(mfrow=c(1,1))
tn= nnetar(samp[1:300,5],P=100,p=20,size=5,repeats=2)
tnf=forecast(tn,h=30)
plot(ylim=c(0,20),tnf)
#points(ylim=c(0,20),samp[1:330,5])
lines(x=seq(1,330),y=tsamp[1:330,5],col='black')
tnf
accuracy(tnf)
mini = 0
minP = 0
minp = 0
minS = 0
minr = 0 
results=data.frame()
min_mase =1000000
for(i in seq(100,300,10))
{
    for(j in seq(1,28,3))
    {
        for(k in seq(1,100,10))
        {
            for(z in seq(1,28,3))
                {
                    for(y in seq(1,3))
                    {
                    tn= nnetar(samp[1:(100+i),5],P=k,p=j,size=z,repeats=y)
                    tnf=forecast(tn,h=i)
                    if(accuracy(tnf,samp[(101+i):(100+i+i),5])[6]<min_mase)
                    {
                        results=rbind(results,cbind(rbind(accuracy(tnf,samp[(101+i):(100+i+i),5])),i,j,k,z,y))
                        min_mase = accuracy(tnf,samp[(101+i):(100+i+i),5])[6]
                        mini = i
                        minp = j
                        minP = k
                        minS = z
                        minr = y
                        #print(accuracy(tnf,samp[101:200,5]))
                        print(cat("i=",as.character(i),"P=",as.character(k),"p=",as.character(j),"size=",as.character(z),"repeats=",as.character(y),"MASE=",as.character(accuracy(tnf,samp[(101+i):(100+i+i),5])[6]),"repeats=",as.character(y)))
                    }
                }
            }
        }
        #print(i)
        #print(j)
    }
}

summary(results)
which(results[,6]<0.42)
results
## best one
tn= nnetar(samp[1:200,5],P=41,p=22,size=13,repeats=3)
tnf=forecast(tn,h=100)
plot(ylim=c(0,20),tnf,main="Neural Network 100 Second Forcasts",ylab='Speed (m/s)',xlab='time (sec)')
lines(x=seq(200,300,1),ylim=c(0,20),y=samp[200:300,5],col='red')
legend(250,20,c('Forecast','Actual'),pch=45,col=c('blue','red'))
accuracy(tnf,samp[201:300,5])

par(mfrow=c(2,1))
tn= nnetar(samp[1:2000,5],P=1500,p=30,size=30,repeats=2)
tnf=forecast(tn,h=100)
plot(ylim=c(0,20),tnf)
lines(x=seq(2001,2100,1),ylim=c(0,20),y=samp[2001:2100,5],col='red')
accuracy(tnf,samp[2001:2100,5])

fit=tbats(samp[1:2000,5],seasonal.periods=500,use.arma.errors=T,use.parallel=T,use.box.cox=T,use.trend=T)
ffit=forecast(fit,h=100,fan=T)
plot(x=seq(1,2100),ylim=c(0,20),y=samp[0:2100,5],col='white')
lines(x=seq(2001,2100),ylim=c(0,20),y=samp[2001:2100,5],col=2)
lines(x=seq(1,2000),ylim=c(0,20),y=samp[1:2000,5],col=1)
lines(x=seq(2001,2100),ylim=c(0,20),y=ffit$mean,col='blue')


plot(forecast(arfima(samp[0:2000,5]),h=100))
plot(rwf(samp[0:2000,5],h=100,drift=T,fan=F,lambda=T))

#gls(samp[,8]~samp[,1]+samp[,2]+samp[,3]+samp[,4]+samp[,5]+samp[,6],samp)


