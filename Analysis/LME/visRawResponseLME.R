rm(list = ls())
setwd("C:/Users/wenlou/Documents/R scripts")
library(lme4)
library(openxlsx)
library(lmerTest)  # lme4 wrapper that appends p-values
library(dplyr)
#library(BayesFactor)
#########################################################################################

## read in data
data_path <- "P:/3026008.01/Data" 
out_path <- "./output"

df_V = read.csv(file.path(data_path, "exp1_V_all_exc.csv"), header = TRUE)

df_V$sub_id <- factor(df_V$sub_id)
df_V$ComSourFlag <- factor(df_V$ComSourFlag, order=FALSE) # 1 - common, 0 - separate
df_V$delta_VA <- factor(df_V$delta_VA, order=FALSE)
str(df_V)
#########################################################################################

# create 8 dummy variables - each for one spatial disparity
dummy8 <- model.matrix(~ interaction(df_V$delta_VA) - 1)
colnames(dummy8) <- paste0("av.", c('n24', 'n16', 'n8', '0', 'p8', 'p16', 'p24'))
df_V <- cbind(df_V, dummy8)

# LME model
lmer_resultsV1<-lmer(respPos~ av.n24 + av.n16 + av.n8 + av.p8 + av.p16 + av.p24 + 
      truePos + (1+truePos|sub_id), data=df_V ,control = lmerControl(optimizer = "Nelder_Mead"))
summary(lmer_resultsV1)

#  extracting the coef from 8 dummy variable models
fix.coefs <- as.data.frame(coef(summary(lmer_resultsV1))) %>%
rename("coef.value" = "Estimate",
        "std.err" = "Std. Error",
        "t.value" = "t value",
        "p.value" =  "Pr(>|t|)")

fix.coefs[, 'effects'] <- fix.coefs[, 'coef.value'] + c(0, rep(fix.coefs[1, 'coef.value'], nrow(fix.coefs) - 2), 0)
rownames(fix.coefs)[1] <- "av.0"
fix.coefs$delta_VA <- c(0,-24,-16,-8,8,16,24, -99)

# random effects
rand.coefs <- ranef(lmer_resultsV1)$sub_id%>%rename(c("randInt" = "(Intercept)", "randtruePos" = "truePos"))

#write table
write.csv(fix.coefs, file.path(out_path, "vis_raw_resp_fix_effect.csv") , row.names = TRUE)
write.csv(rand.coefs, file.path(out_path, "vis_raw_resp_rand_effect.csv") , row.names = FALSE)

#########################################################################################
# another LME with no deltaVA
df_V$delta_VA <- as.numeric(df_V$delta_VA)
full_lmer <-  lmer(respPos~ delta_VA + truePos + (1+truePos|sub_id), data=df_V , REML = FALSE)
null_lmer <-  lmer(respPos~ truePos + (1+truePos|sub_id), data=df_V , REML=FALSE)  
BF_BIC <-  exp((BIC(null_lmer) - BIC(full_lmer))/2)  # BICs to Bayes factor
BF_BIC
1/BF_BIC
