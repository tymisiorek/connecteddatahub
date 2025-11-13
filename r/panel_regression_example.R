rm(list=ls())

path='/Users/psp2nq/Dropbox/Tutorials/Advanced-DID-main/Exercises/Exercise-1'
setwd(path)


rm(list=ls())

library(fixest)
library(dplyr)
library(marginaleffects)
library(ggplot2)

##################################
# Load data
##################################


dfself <- read.csv("bootstrap_noselfauthoraff_R_07172025.csv")


dfself$income_group <- factor(dfself$income_group, 
                              levels = c("LM-L", "UM", 'H')) # if you have category variable, to set the baseline category

levels(dfself$income_group)

dfself$NResearchers = log10(dfself$NResearchers)


dfself$Country <- as.factor(dfself$Country) # important
dfself$Year <- as.factor(dfself$Year) # important


df_normalized <- dfself %>%
  mutate(across(c(logNumPub, GDP,GDP_PCAP, RND_per, FracInternationalAuthors,
                  logzscore, NResearchers,FracInternationalAuthors,logzscore ), scale))  # Normalize only columns x, y, z

#######################################
# Table 2: Regression estimates of international collaboration on citation self-preference by stages of economic development.
#######################################

m1 <- feols(FracInternationalAuthors ~ logzscore, data = df_normalized)
m2 <- feols(FracInternationalAuthors ~ logzscore | Year, data = df_normalized)
m3 <- feols(FracInternationalAuthors ~ logzscore | Country+Year, data = df_normalized, cluster = ~Country)


m5 <- feols(FracInternationalAuthors ~ logzscore * GDP_PCAP | Country+Year, data = df_normalized, cluster = ~Country)

clean_data <- subset(df_normalized, income_group != "")
clean_data$income_group <- factor(clean_data$income_group)
clean_data$income_group <- relevel(clean_data$income_group, ref = "LM-L")

m6 <- feols(FracInternationalAuthors ~ logzscore*income_group | Country+Year, data = clean_data, cluster = ~Country)


fitstat_register("n_countries", function(x){
  if(!is.null(x$fixef_sizes) && "Country" %in% names(x$fixef_sizes)){
    x$fixef_sizes["Country"]   # number of unique countries in FE
  } else if("Country" %in% names(x$model_frame)){
    length(unique(x$model_frame$Country))  # fallback
  } else {
    NA
  }
})


etable(m1,m2,m3,m4,m5,m6)

etable(m1,m2,m3,m5,m6, tex = TRUE, digits = 3,  
       file = paste0("collabVSself_", filename_suffix, "_09222025.tex"), 
       fitstat = ~ n + n_countries + f + r2 + ar2, 
       replace = TRUE,
       title = "Regression estimates of international collaboration on citation self-preference by stages of
economic development.",
       order = c("logzscore", "GDP_PCAP", "income_groupUM", 
                 "income_groupH", "logzscore:income_groupUM", 
                 "logzscore:income_groupH", 
                 "!Constant"),
       dict = c("FracInternationalAuthors" = "International collaboration",
                "logzscore" = "Citation self-preference",
                "GDP_PCAP" = "GDP per capita",
                "income_groupH" = "High income",
                "income_groupUM" = "Upper-middle income",
                "logzscore:income_groupH" = "Citation self-preference × High income",
                "logzscore:income_groupUM" = "Citation self-preference × Upper-middle income",
                "n_countries" = "Countries"),
       placement = "H",arraystretch = 0.7     
)

