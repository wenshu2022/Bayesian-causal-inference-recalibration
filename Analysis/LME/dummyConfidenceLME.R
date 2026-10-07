rm(list = ls())
setwd("C:/Users/wenlou/Documents/R scripts")
library(lme4)
library(openxlsx)
library(lmerTest)  # lme4 wrapper that appends p-values
library(dplyr)
#########################################################################################

## read in data
data_path <- "P:/3026008.01/Data" 
out_path <- "./output"

df_A = read.csv(file.path(data_path, "exp1_A_all_w_VAE_norm_exc.csv"), header = TRUE)
str(df_A)

df_A$sub_id <- factor(df_A$sub_id)
df_A$ComSourFlag <- factor(df_A$ComSourFlag, order=FALSE) # 1 - common, 0 - separate
df_A$confLvl <- factor(df_A$confLvl, order=FALSE)
#########################################################################################

## create dummy variables
# 1. 24 dummy variables - interaction between spatial disparity and high/medium/low confidence, and common/distinct
inter24_ <- interaction(df_A$ComSourFlag, df_A$confLvl , df_A$abs_delta_VA,  sep = "_")
dummy24 <- model.matrix(~ inter24_-1)

# 2. 12 dummy variables - interaction between spatial disparity and high/medium/low confidence
inter12_ <- interaction(df_A$confLvl , df_A$abs_delta_VA,  sep = "_")
dummy12 <- model.matrix(~ inter12_-1)

# Combine the dummy variables with the original data frame
df_A <- cbind(df_A, dummy24, dummy12)

#########################################################################################

# LME - COMMON/SEPARATE vs. confidence vs. spatial disparity

model.Dummy.intr24 <- lmer(flipVAE ~  inter24_0_1_0 + inter24_1_1_0 + inter24_0_2_0 + inter24_1_2_0 + inter24_0_3_0 + inter24_0_1_8 + inter24_1_1_8 + inter24_0_2_8 + 
                                inter24_1_2_8 + inter24_0_3_8 + inter24_1_3_8 + inter24_0_1_16 + inter24_1_1_16 + inter24_0_2_16 + inter24_1_2_16 + inter24_0_3_16 + inter24_1_3_16+
                                inter24_0_1_24 + inter24_1_1_24 + inter24_0_2_24 + inter24_1_2_24 + inter24_0_3_24 + inter24_1_3_24 + (1|sub_id), data=df_A, 
                    control = lmerControl(optimizer = "Nelder_Mead"))
summary(model.Dummy.intr24)

fix.coefs <- as.data.frame(coef(summary(model.Dummy.intr24))) %>%
rename("coef.value" = "Estimate",
        "std.err" = "Std. Error",
        "t.value" = "t value",
        "p.value" =  "Pr(>|t|)")

fix.coefs[, 'effects'] <- fix.coefs[, 'coef.value'] + c(0, rep(fix.coefs[1, 'coef.value'], nrow(fix.coefs) - 1))

rownames(fix.coefs)[1] <- "inter24_1_3_0"

fix.coefs$confLvl <- c(3, 1, 1, 2, 2, 3, 1, 1, 2, 2, 3, 3, 1, 1, 2, 2, 3, 3, 1, 1, 2, 2, 3, 3)
fix.coefs$abs_delta_VA <- c(0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 16, 16, 16, 16, 16, 16, 24, 24, 24, 24, 24, 24)
fix.coefs$com_flag <- c(1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1)

fix.coefs[fix.coefs$com_flag==1, 'ComSourLbl']='Common'
fix.coefs[fix.coefs$com_flag==0, 'ComSourLbl']='Separate'

fix.coefs[fix.coefs$confLvl==1, 'ConfLbl']='Low'
fix.coefs[fix.coefs$confLvl==2, 'ConfLbl']='Medium'
fix.coefs[fix.coefs$confLvl==3, 'ConfLbl']='High'


#########################################################################################

# LME - confidence vs. spatial disparity
# ##### with raw flipVAE
model.Dummy.intr12 <- lmer(flipVAE ~  inter12_1_0 + inter12_2_0 + 
                                    inter12_1_8 + inter12_2_8 + inter12_3_8 +
                                    inter12_1_16 + inter12_2_16 + inter12_3_16 +
                                    inter12_1_24 + inter12_2_24 + inter12_3_24 + (1|sub_id), data=df_A, 
                    control = lmerControl(optimizer = "Nelder_Mead"))
summary(model.Dummy.intr12)

fix.coefs.t <- as.data.frame(coef(summary(model.Dummy.intr12))) %>%
rename("coef.value" = "Estimate",
        "std.err" = "Std. Error",
        "t.value" = "t value",
        "p.value" =  "Pr(>|t|)")

fix.coefs.t[, 'effects'] <- fix.coefs.t[, 'coef.value'] + c(0, rep(fix.coefs.t[1, 'coef.value'], nrow(fix.coefs.t) - 1))

rownames(fix.coefs.t)[1] <- "inter12_3_0"

fix.coefs.t$confLvl <- c(3,1,2,1,2,3,1,2,3,1,2,3)
fix.coefs.t$abs_delta_VA <- c(0, 0, 0, 8, 8, 8, 16, 16, 16, 24, 24, 24)
fix.coefs.t[fix.coefs.t$confLvl==1, 'ConfLbl']='Low'
fix.coefs.t[fix.coefs.t$confLvl==2, 'ConfLbl']='Medium'
fix.coefs.t[fix.coefs.t$confLvl==3, 'ConfLbl']='High'
fix.coefs.t[, 'ComSourLbl']='Total'


#########################################################################################

# combine the two datasets and write table

# fixed effects
fix.coefs <- rbind(fix.coefs[, -which(names(fix.coefs)=='com_flag')], fix.coefs.t)
write.csv(fix.coefs, file.path(out_path, "fix_effect_conf.csv") , row.names = FALSE)

# random effects
random_effects24 <- ranef(model.Dummy.intr24)$sub_id%>%rename("intr24" = "(Intercept)")
random_effects12 <- ranef(model.Dummy.intr12)$sub_id%>%rename("intr12_t" = "(Intercept)")

write.csv(cbind(random_effects24, random_effects12) , file.path(out_path, "rand_effect_conf.csv"), row.names = FALSE)





