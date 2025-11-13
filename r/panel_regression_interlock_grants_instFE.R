# Clear environment
rm(list=ls())

# Load required packages
library(fixest)
library(dplyr)
library(ggplot2)

# Load your dataset
df <- read.csv("C:/Projects/connecteddatahub/data/interlocks/interlocks_grants.csv")


# Ensure proper types
df$Year <- as.factor(df$Year)
df$AffiliationId <- as.factor(df$AffiliationId)

# Optional: scale numeric variables (normalization for comparability)
df_norm <- df %>%
  mutate(across(c(log_grants, log_funding, weakness_entropy), scale))

############################################
# Regression: Dependence on weakness_entropy
############################################

# Model 1: log(grants) ~ weakness_entropy + Year FE
m1 <- feols(log_grants ~ weakness_entropy | Year + AffiliationId, data = df_norm)

# Model 2: log(funding) ~ weakness_entropy + Year FE
m2 <- feols(log_funding ~ weakness_entropy | Year + AffiliationId, data = df_norm)

# (optional) If you want to see interaction:
# m3 <- feols(log_funding ~ weakness_entropy * log_grants | Year, data = df_norm)

############################################
# Display results
############################################

print("Weakness entropy and number of grants:")

etable(m1, m2,
       digits = 3,
       fitstat = ~ n + f + r2 + ar2,
       title = "Dependence of grants and funding on institutional weakness entropy (Year FE)",
       dict = c("log_grants" = "Log(Number of Grants)",
                "log_funding" = "Log(Total Funding)",
                "weakness_entropy" = "Weakness Entropy"),
       order = c("weakness_entropy", "!Constant"),
       placement = "H", arraystretch = 0.8)


summary(m1)
summary(m2)



cat()
print("average weakness instead of entropy")
cat()


m1_avg <- feols(log_grants ~ avg_weakness | Year + AffiliationId, data = df_norm)

# Model 2: log(funding) ~ avg_weakness + Year FE
m2_avg <- feols(log_funding ~ avg_weakness | Year + AffiliationId, data = df_norm)

############################################
# Display results
############################################

etable(m1_avg, m2_avg,
       digits = 3,
       fitstat = ~ n + f + r2 + ar2,
       title = "Dependence of grants and funding on average institutional weakness (Year FE)",
       dict = c("log_grants" = "Log(Number of Grants)",
                "log_funding" = "Log(Total Funding)",
                "avg_weakness" = "Average Weakness"),
       order = c("avg_weakness", "!Constant"),
       placement = "H", arraystretch = 0.8)
