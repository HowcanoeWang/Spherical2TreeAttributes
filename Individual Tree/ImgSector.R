

library(OpenImageR)
sector.sample<-function(img=".\\COR R1 S00 0 16.jpg",sample.intensity=2,num.sectors=1,img.out="red COR R1 S00 0 16.jpg")
{
  require("OpenImageR")
  IMG<-readImage(img)
  imageShow(IMG)
  Iwd<-dim(IMG)[2]
  Swd<-round(sample.intensity*Iwd/100/num.sectors,0)
  sector.mids<-sample(1:Iwd,size=num.sectors)
  print(sector.mids)
  for(i in sector.mids){
    Sbeg<-round(i-Swd/2,0)
    if(Sbeg<0){Sbeg<-Iwd+Sbeg}
    Send<-round(i+Swd/2,0)
    if(Send>Iwd){Send<-Send-Iwd}
    if(Sbeg<=2){ss<-seq(-Sbeg,0)}else{ss<-seq(-2,0)}
    IMG[,Sbeg+ss,1]<-1
    IMG[,Sbeg+ss,2]<-0
    IMG[,Sbeg+ss,3]<-0
    if(Iwd-Send<=2){ee<-seq(0,Iwd-Send)}else{ee<-seq(0,2)}
    IMG[,Send+ee,1]<-1
    IMG[,Send+ee,2]<-0
    IMG[,Send+ee,3]<-0
  }
  imageShow(IMG)
  writeImage(IMG,file=img.out)
}


library(imager)
I<-load.image("C:\\Users\\dx542\\OneDrive\\Desktop\\Photo_NL16\\16only\\Cormack\\COR R1 S00 0 16.jpg")
plot(I)


#---------------------------------COR R1--------------------------------#

sector.sample(img=".\\COR R1 S00 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S00 0 16.jpg")
sector.sample(img=".\\COR R1 S00 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S00 1 16.jpg")
sector.sample(img=".\\COR R1 S00 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S00 2 16.jpg")


sector.sample(img=".\\COR R1 S12 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S12 0 16.jpg")
sector.sample(img=".\\COR R1 S12 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S12 1 16.jpg")
sector.sample(img=".\\COR R1 S12 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S12 2 16.jpg")

sector.sample(img=".\\COR R1 S18 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S18 0 16.jpg")
sector.sample(img=".\\COR R1 S18 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S18 1 16.jpg")
sector.sample(img=".\\COR R1 S18 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S18 2 16.jpg")

sector.sample(img=".\\COR R1 S24 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S24 0 16.jpg")
sector.sample(img=".\\COR R1 S24 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S24 1 16.jpg")
sector.sample(img=".\\COR R1 S24 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S24 2 16.jpg")

sector.sample(img=".\\COR R1 S30 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S30 0 16.jpg")
sector.sample(img=".\\COR R1 S30 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S30 1 16.jpg")
sector.sample(img=".\\COR R1 S30 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R1 S30 2 16.jpg")



#-----------------------------COR R2------------------------------------------#


sector.sample(img=".\\COR R2 S00 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S00 0 16.jpg")
sector.sample(img=".\\COR R2 S00 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S00 1 16.jpg")
sector.sample(img=".\\COR R2 S00 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S00 2 16.jpg")


sector.sample(img=".\\COR R2 S12 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S12 0 16.jpg")
sector.sample(img=".\\COR R2 S12 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S12 1 16.jpg")
sector.sample(img=".\\COR R2 S12 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S12 2 16.jpg")

sector.sample(img=".\\COR R2 S18 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S18 0 16.jpg")
sector.sample(img=".\\COR R2 S18 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S18 1 16.jpg")
sector.sample(img=".\\COR R2 S18 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S18 2 16.jpg")

sector.sample(img=".\\COR R2 S24 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S24 0 16.jpg")
sector.sample(img=".\\COR R2 S24 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S24 1 16.jpg")
sector.sample(img=".\\COR R2 S24 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S24 2 16.jpg")

sector.sample(img=".\\COR R2 S30 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S30 0 16.jpg")
sector.sample(img=".\\COR R2 S30 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S30 1 16.jpg")
sector.sample(img=".\\COR R2 S30 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R2 S30 2 16.jpg")




#-----------------------------COR R3------------------------------------------#

sector.sample(img=".\\COR R3 S00 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S00 0 16.jpg")
sector.sample(img=".\\COR R3 S00 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S00 1 16.jpg")
sector.sample(img=".\\COR R3 S00 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S00 2 16.jpg")


sector.sample(img=".\\COR R3 S12 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S12 0 16.jpg")
sector.sample(img=".\\COR R3 S12 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S12 1 16.jpg")
sector.sample(img=".\\COR R3 S12 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S12 2 16.jpg")

sector.sample(img=".\\COR R3 S18 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S18 0 16.jpg")
sector.sample(img=".\\COR R3 S18 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S18 1 16.jpg")
sector.sample(img=".\\COR R3 S18 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S18 2 16.jpg")

sector.sample(img=".\\COR R3 S24 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S24 0 16.jpg")
sector.sample(img=".\\COR R3 S24 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S24 1 16.jpg")
sector.sample(img=".\\COR R3 S24 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S24 2 16.jpg")

sector.sample(img=".\\COR R3 S30 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S30 0 16.jpg")
sector.sample(img=".\\COR R3 S30 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S30 1 16.jpg")
sector.sample(img=".\\COR R3 S30 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red COR R3 S30 2 16.jpg")









#---------------------------------PAS R1--------------------------------#

sector.sample(img=".\\PAS R1 S00 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S00 0 16.jpg")
sector.sample(img=".\\PAS R1 S00 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S00 1 16.jpg")
sector.sample(img=".\\PAS R1 S00 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S00 2 16.jpg")


sector.sample(img=".\\PAS R1 S12 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S12 0 16.jpg")
sector.sample(img=".\\PAS R1 S12 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S12 1 16.jpg")
sector.sample(img=".\\PAS R1 S12 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S12 2 16.jpg")

sector.sample(img=".\\PAS R1 S18 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S18 0 16.jpg")
sector.sample(img=".\\PAS R1 S18 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S18 1 16.jpg")
sector.sample(img=".\\PAS R1 S18 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S18 2 16.jpg")

sector.sample(img=".\\PAS R1 S24 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S24 0 16.jpg")
sector.sample(img=".\\PAS R1 S24 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S24 1 16.jpg")
sector.sample(img=".\\PAS R1 S24 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S24 2 16.jpg")

sector.sample(img=".\\PAS R1 S30 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S30 0 16.jpg")
sector.sample(img=".\\PAS R1 S30 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S30 1 16.jpg")
sector.sample(img=".\\PAS R1 S30 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R1 S30 2 16.jpg")



#-----------------------------PAS R2------------------------------------------#


sector.sample(img=".\\PAS R2 S00 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S00 0 16.jpg")
sector.sample(img=".\\PAS R2 S00 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S00 1 16.jpg")
sector.sample(img=".\\PAS R2 S00 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S00 2 16.jpg")


sector.sample(img=".\\PAS R2 S12 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S12 0 16.jpg")
sector.sample(img=".\\PAS R2 S12 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S12 1 16.jpg")
sector.sample(img=".\\PAS R2 S12 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S12 2 16.jpg")

sector.sample(img=".\\PAS R2 S18 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S18 0 16.jpg")
sector.sample(img=".\\PAS R2 S18 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S18 1 16.jpg")
sector.sample(img=".\\PAS R2 S18 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S18 2 16.jpg")

sector.sample(img=".\\PAS R2 S24 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S24 0 16.jpg")
sector.sample(img=".\\PAS R2 S24 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S24 1 16.jpg")
sector.sample(img=".\\PAS R2 S24 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S24 2 16.jpg")

sector.sample(img=".\\PAS R2 S30 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S30 0 16.jpg")
sector.sample(img=".\\PAS R2 S30 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S30 1 16.jpg")
sector.sample(img=".\\PAS R2 S30 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R2 S30 2 16.jpg")




#-----------------------------PAS R3------------------------------------------#

sector.sample(img=".\\PAS R3 S00 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S00 0 16.jpg")
sector.sample(img=".\\PAS R3 S00 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S00 1 16.jpg")
sector.sample(img=".\\PAS R3 S00 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S00 2 16.jpg")


sector.sample(img=".\\PAS R3 S12 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S12 0 16.jpg")
sector.sample(img=".\\PAS R3 S12 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S12 1 16.jpg")
sector.sample(img=".\\PAS R3 S12 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S12 2 16.jpg")

sector.sample(img=".\\PAS R3 S18 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S18 0 16.jpg")
sector.sample(img=".\\PAS R3 S18 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S18 1 16.jpg")
sector.sample(img=".\\PAS R3 S18 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S18 2 16.jpg")

sector.sample(img=".\\PAS R3 S24 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S24 0 16.jpg")
sector.sample(img=".\\PAS R3 S24 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S24 1 16.jpg")
sector.sample(img=".\\PAS R3 S24 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S24 2 16.jpg")

sector.sample(img=".\\PAS R3 S30 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S30 0 16.jpg")
sector.sample(img=".\\PAS R3 S30 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S30 1 16.jpg")
sector.sample(img=".\\PAS R3 S30 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red PAS R3 S30 2 16.jpg")















#---------------------------------ROD R1--------------------------------#

sector.sample(img=".\\ROD R1 S00 0 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S00 0 16.jpg")
sector.sample(img=".\\ROD R1 S00 1 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S00 1 16.jpg")
sector.sample(img=".\\ROD R1 S00 2 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S00 2 16.jpg")


sector.sample(img=".\\ROD R1 S12 0 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S12 0 16.jpg")
sector.sample(img=".\\ROD R1 S12 1 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S12 1 16.jpg")
sector.sample(img=".\\ROD R1 S12 2 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S12 2 16.jpg")

sector.sample(img=".\\ROD R1 S18 0 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S18 0 16.jpg")
sector.sample(img=".\\ROD R1 S18 1 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S18 1 16.jpg")
sector.sample(img=".\\ROD R1 S18 2 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S18 2 16.jpg")

sector.sample(img=".\\ROD R1 S24 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S24 0 16.jpg")
sector.sample(img=".\\ROD R1 S24 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S24 1 16.jpg")
sector.sample(img=".\\ROD R1 S24 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S24 2 16.jpg")

sector.sample(img=".\\ROD R1 S30 0 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S30 0 16.jpg")
sector.sample(img=".\\ROD R1 S30 1 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S30 1 16.jpg")
sector.sample(img=".\\ROD R1 S30 2 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R1 S30 2 16.jpg")



#-----------------------------ROD R2------------------------------------------#


sector.sample(img=".\\ROD R2 S00 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S00 0 16.jpg")
sector.sample(img=".\\ROD R2 S00 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S00 1 16.jpg")
sector.sample(img=".\\ROD R2 S00 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S00 2 16.jpg")


sector.sample(img=".\\ROD R2 S12 0 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S12 0 16.jpg")
sector.sample(img=".\\ROD R2 S12 1 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S12 1 16.jpg")
sector.sample(img=".\\ROD R2 S12 2 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S12 2 16.jpg")

sector.sample(img=".\\ROD R2 S18 0 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S18 0 16.jpg")
sector.sample(img=".\\ROD R2 S18 1 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S18 1 16.jpg")
sector.sample(img=".\\ROD R2 S18 2 16 A20.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S18 2 16.jpg")

sector.sample(img=".\\ROD R2 S24 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S24 0 16.jpg")
sector.sample(img=".\\ROD R2 S24 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S24 1 16.jpg")
sector.sample(img=".\\ROD R2 S24 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S24 2 16.jpg")

sector.sample(img=".\\ROD R2 S30 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S30 0 16.jpg")
sector.sample(img=".\\ROD R2 S30 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S30 1 16.jpg")
sector.sample(img=".\\ROD R2 S30 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R2 S30 2 16.jpg")




#-----------------------------ROD R3------------------------------------------#

sector.sample(img=".\\ROD R3 S00 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S00 0 16.jpg")
sector.sample(img=".\\ROD R3 S00 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S00 1 16.jpg")
sector.sample(img=".\\ROD R3 S00 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S00 2 16.jpg")


sector.sample(img=".\\ROD R3 S12 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S12 0 16.jpg")
sector.sample(img=".\\ROD R3 S12 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S12 1 16.jpg")
sector.sample(img=".\\ROD R3 S12 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S12 2 16.jpg")

sector.sample(img=".\\ROD R3 S18 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S18 0 16.jpg")
sector.sample(img=".\\ROD R3 S18 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S18 1 16.jpg")
sector.sample(img=".\\ROD R3 S18 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S18 2 16.jpg")

sector.sample(img=".\\ROD R3 S24 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S24 0 16.jpg")
sector.sample(img=".\\ROD R3 S24 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S24 1 16.jpg")
sector.sample(img=".\\ROD R3 S24 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S24 2 16.jpg")

sector.sample(img=".\\ROD R3 S30 0 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S30 0 16.jpg")
sector.sample(img=".\\ROD R3 S30 1 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S30 1 16.jpg")
sector.sample(img=".\\ROD R3 S30 2 16.jpg",sample.intensity=5,num.sectors=1,img.out="red ROD R3 S30 2 16.jpg")









