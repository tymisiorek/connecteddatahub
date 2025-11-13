library(fixest)
library(dplyr)

# Load and prep data
df <- read.csv("C:/Projects/connecteddatahub/data/interlocks/interlocks_grants.csv")
df$Year <- as.factor(df$Year)

# Ensure your residual variables are numeric and scaled if desired
df_norm <- df %>%
  mutate(across(c(grants_resid, funding_resid, weakness_entropy), scale))

############################################
# Regression using residual (size-controlled) outcomes
############################################

m1 <- feols(grants_resid ~ weakness_entropy + betweenness_centrality + clustering | Year, data = df_norm)
m2 <- feols(funding_resid ~ weakness_entropy + betweenness_centrality + clustering | Year, data = df_norm)

etable(m1, m2,
       digits = 3,
       fitstat = ~ n + f + r2 + ar2,
       title = "Dependence of size-controlled grants and funding on institutional network structure and weakness entropy (Year FE)",
       dict = c("grants_resid" = "Grants (Size-Controlled)",
                "funding_resid" = "Funding (Size-Controlled)",
                "weakness_entropy" = "Weakness Entropy",
                "betweenness_centrality" = "Betweenness Centrality",
                "clustering" = "Clustering Coefficient"),
       order = c("weakness_entropy", "betweenness_centrality", "clustering", "!Constant"))
