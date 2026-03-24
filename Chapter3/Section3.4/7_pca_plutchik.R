library(factoextra)
library(FactoMineR)

dataset <- read.csv("6_dataset_pca_caus.csv", sep = ";", header = T)
df1 <- data.frame(dataset[,-1], row.names = dataset[,1])

# create dataset with ratings
pl_rat  <- df1[1:8]

pl_rat$joy <- as.numeric(gsub(",", ".", pl_rat$joy))
pl_rat$sadness <- as.numeric(gsub(",", ".", pl_rat$sadness))
pl_rat$anger <- as.numeric(gsub(",", ".", pl_rat$anger))
pl_rat$disgust <- as.numeric(gsub(",", ".", pl_rat$disgust))
pl_rat$fear <- as.numeric(gsub(",", ".", pl_rat$fear))
pl_rat$trust <- as.numeric(gsub(",", ".", pl_rat$trust))
pl_rat$surprise <- as.numeric(gsub(",", ".", pl_rat$surprise))
pl_rat$anticipation <- as.numeric(gsub(",", ".", pl_rat$anticipation))


View(dataset)

# apply pca
pl_pca <- PCA(na.omit(pl_rat), graph = TRUE)

# create dataset with cxn labels
pl_dat <- dataset[-c(9:23)]

pl_dat$joy <- as.numeric(gsub(",", ".", pl_dat$joy))
pl_dat$sadness <- as.numeric(gsub(",", ".", pl_dat$sadness))
pl_dat$anger <- as.numeric(gsub(",", ".", pl_dat$anger))
pl_dat$disgust <- as.numeric(gsub(",", ".", pl_dat$disgust))
pl_dat$fear <- as.numeric(gsub(",", ".", pl_dat$fear))
pl_dat$trust <- as.numeric(gsub(",", ".", pl_dat$trust))
pl_dat$surprise <- as.numeric(gsub(",", ".", pl_dat$surprise))
pl_dat$anticipation <- as.numeric(gsub(",", ".", pl_dat$anticipation))

pl_dat <- na.omit(pl_dat)
pl_rat <- na.omit(pl_rat)
pl_rat <- pl_rat[, colSums(pl_rat == "") == 0]
pl_dat <- pl_dat[, colSums(pl_dat == "") == 0]

View(pl_rat)
# plot causative cxns, one by one one

# plot cxn fillers pca on biplot
plotfare <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$fare_LVC), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
#extract data points for cxns fillers from cxn fillers biplot
d <- as.data.frame(plotfare$data)
# calculate mean point for cxn fillers
fare_LVC <- c(mean(d$x[d$Groups == "fare_LVC"]), mean(d$y[d$Groups == "fare_LVC"]))

plotdare <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$dare_LVC), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotdare$data)
dare_LVC <- c(mean(d$x[d$Groups == "dare_LVC"]), mean(d$y[d$Groups == "dare_LVC"]))

plotconv <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$conversion_caus), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotconv$data)
conversion_caus <- c(mean(d$x[d$Groups == "conversion_caus"]), mean(d$y[d$Groups == "conversion_caus"]))

plotpara <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$parasynthesis_caus), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotpara$data)
parasynthesis <- c(mean(d$x[d$Groups == "parasynthesis_caus"]), mean(d$y[d$Groups == "parasynthesis_caus"]))

plotmettere <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$mettere_LVC), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotmettere$data)
mettere_LVC <- c(mean(d$x[d$Groups == "mettere_LVC"]), mean(d$y[d$Groups == "mettere_LVC"]))

# create dataframe with mean points
x <- c(conversion_caus[1], dare_LVC[1], fare_LVC[1], mettere_LVC[1], parasynthesis[1])
y <- c(conversion_caus[2], dare_LVC[2], fare_LVC[2], mettere_LVC[2], parasynthesis[2])
causatives <- data.frame(x,y, row.names = c("conversion", "dare_LVC", "fare_LVC", "mettere_LVC", "parasynthesis"))

# plot mean points of cxn fillers on pca's biplot (noun labels were hidden)
plot_white <- fviz_pca_biplot(pl_pca, col.ind = "white", repel = T, mean.point.size = 4, geom = "point")
plot_white
fviz_add(plot_white, causatives, geom = "point", addlabel = TRUE, repel = TRUE, color = "black")

plot_white
fviz_add(plot_white, causatives, geom = "point", addlabel = TRUE, repel = TRUE, color = "black")
# same process for inchoatives
plotandare_in <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$andare_in_LVC), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotandare_in$data)
andare_in_LVC <- c(mean(d$x[d$Groups == "andare_in_LVC"]), mean(d$y[d$Groups == "andare_in_LVC"]))

plotprendere <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$prendere_LVC), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotprendere$data)
prendere_LVC <- c(mean(d$x[d$Groups == "prendere_LVC"]), mean(d$y[d$Groups == "prendere_LVC"]))

plotconversion_si <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$conversion_si), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotconversion_si$data)
conversion_si <- c(mean(d$x[d$Groups == "conversion_si"]), mean(d$y[d$Groups == "conversion_si"]))

plotparasynthesis_si <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$parasynthesis_si), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotparasynthesis_si$data)
parasynthesis_si <- c(mean(d$x[d$Groups == "parasynthesis_si"]), mean(d$y[d$Groups == "parasynthesis_si"]))

x <- c(andare_in_LVC[1], conversion_si[1], parasynthesis_si[1], prendere_LVC[1])
y <- c(andare_in_LVC[2], conversion_si[2], parasynthesis_si[2], prendere_LVC[2])
inchoatives <- data.frame(x,y, row.names = c("andare_in_LVC", "conversion_si", "parasynthesis_si", "prendere_LVC"))

plot_white <- fviz_pca_biplot(pl_pca, col.ind = "white", repel = T, geom = "point")
fviz_add(plot_white, inchoatives, geom = "point", addlabel = TRUE, repel = TRUE, color = "black")



# same process for statives
plotconversion_si_stat <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$conversion_si_stat), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotconversion_si_stat$data)
conversion_si_stat <- c(mean(d$x[d$Groups == "conversion_si_stat"]), mean(d$y[d$Groups == "conversion_si_stat"]))

plotconversion_stat <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$conversion_stat), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotconversion_stat$data)
conversion_stat <- c(mean(d$x[d$Groups == "conversion_stat"]), mean(d$y[d$Groups == "conversion_stat"]))

plotessere_in_LVC <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$essere_in_LVC), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotessere_in_LVC$data)
essere_in_LVC <- c(mean(d$x[d$Groups == "essere_in_LVC"]), mean(d$y[d$Groups == "essere_in_LVC"]))

plotsentire_LVC <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$sentire_LVC), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotsentire_LVC$data)
sentire_LVC <- c(mean(d$x[d$Groups == "sentire_LVC"]), mean(d$y[d$Groups == "sentire_LVC"]))

plotprovare_LVC <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$provare_LVC), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotprovare_LVC$data)
provare_LVC <- c(mean(d$x[d$Groups == "provare_LVC"]), mean(d$y[d$Groups == "provare_LVC"]))

plotavere_LVC <- fviz_pca_biplot(pl_pca, habillage = as.factor(pl_dat$avere_LVC), addEllipses = TRUE, ellipse.type = "none", repel = T, mean.point.size = 4, pointsize = 0, geom = "point")
d <- as.data.frame(plotavere_LVC$data)
avere_LVC <- c(mean(d$x[d$Groups == "avere_LVC"]), mean(d$y[d$Groups == "avere_LVC"]))

x <- c(avere_LVC[1], conversion_stat[1], conversion_si_stat[1], essere_in_LVC[1], provare_LVC[1], sentire_LVC[1])
y <- c(avere_LVC[2], conversion_stat[2], conversion_si_stat[2], essere_in_LVC[2], provare_LVC[2], sentire_LVC[2])

statives <- data.frame(x,y, row.names = c("avere_LVC", "conversion_stat", "conversion_si_stat", "essere_in_LVC", "provare_LVC", "sentire_LVC"))
plot_white <- fviz_pca_biplot(pl_pca, col.ind = "white", repel = T, geom = "point")
fviz_add(plot_white, statives, geom = "point", addlabel = TRUE, repel = TRUE, color = "black")

