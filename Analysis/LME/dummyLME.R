rm(list = ls())
setwd("C:/Users/wenlou/Documents/R scripts/RecaliProject")
library(lme4)
library(openxlsx)
library(lmerTest)
library(dplyr)

run_lme_analysis <- function(df_A, out_path, suffix = "") {
    
  # Create dummy variables
  inter8_ <- interaction(df_A$ComSourFlag, df_A$abs_delta_VA, sep = "_")
  dummy8 <- model.matrix(~ inter8_ - 1)
  df_A <- cbind(df_A, dummy8)
  
  inter4_ <- interaction(df_A$abs_delta_VA)
  dummy4 <- model.matrix(~ inter4_ - 1)
  df_A <- cbind(df_A, dummy4)
  
  # LME: COMMON VS. SEPARATE
  model.Dummy.intr8 <- lmer(flipVAE ~ inter8_0_0 + inter8_0_8 + inter8_1_8 + inter8_0_16 + 
                            inter8_1_16 + inter8_0_24 + inter8_1_24 + (1 | sub_id), 
                            data = df_A, 
                            control = lmerControl(optimizer = "Nelder_Mead"))
  
  # Extract coefficients from 8 dummy variable model
  fix.coefs <- as.data.frame(coef(summary(model.Dummy.intr8))) %>%
    rename("coef.value" = "Estimate",
           "std.err" = "Std. Error",
           "t.value" = "t value",
           "p.value" = "Pr(>|t|)")
  fix.coefs[, 'effects'] <- fix.coefs[, 'coef.value'] + c(0, rep(fix.coefs[1, 'coef.value'], nrow(fix.coefs) - 1))
  rownames(fix.coefs)[1] <- "inter8_1_0"
  fix.coefs$com_flag <- c(1, 0, 0, 1, 0, 1, 0, 1)
  fix.coefs$abs_delta_VA <- c(0, 0, 8, 8, 16, 16, 24, 24)
  fix.coefs$ComSourLbl[fix.coefs$com_flag == 1] <- 'Common'
  fix.coefs$ComSourLbl[fix.coefs$com_flag == 0] <- 'Separate'
  
  # LME: TOTAL
  model.Dummy.intr4 <- lmer(flipVAE ~ inter4_8 + inter4_16 + inter4_24 + (1 | sub_id), 
                            data = df_A, 
                            control = lmerControl(optimizer = "Nelder_Mead"))
  
  # Extract coefficients from 4 dummy variable model
  fix.coefs.t <- as.data.frame(coef(summary(model.Dummy.intr4))) %>%
    rename("coef.value" = "Estimate",
           "std.err" = "Std. Error",
           "t.value" = "t value",
           "p.value" = "Pr(>|t|)")
  fix.coefs.t[, 'effects'] <- fix.coefs.t[, 'coef.value'] + c(0, rep(fix.coefs.t[1, 'coef.value'], nrow(fix.coefs.t) - 1))
  rownames(fix.coefs.t)[1] <- "inter4_0"
  fix.coefs.t$abs_delta_VA <- c(0, 8, 16, 24)
  fix.coefs.t$ComSourLbl <- 'Total'
  
  # Combine and save fixed effects
  fix.coefs <- rbind(fix.coefs[, -which(names(fix.coefs) == 'com_flag')], fix.coefs.t)
  fix_effect_file <- file.path(out_path, paste0("fix_effect", suffix, ".csv"))
  write.csv(fix.coefs, fix_effect_file, row.names = FALSE)
  
  # Save random effects
  random_effects8 <- ranef(model.Dummy.intr8)$sub_id %>% rename("intr8_c_s" = "(Intercept)")
  random_effects4 <- ranef(model.Dummy.intr4)$sub_id %>% rename("intr4_t" = "(Intercept)")
  rand_effect_file <- file.path(out_path, paste0("rand_effect", suffix, ".csv"))
  write.csv(cbind(random_effects8, random_effects4), rand_effect_file, row.names = FALSE)
  
  anova_tab <- anova(model.Dummy.intr4, type = 3)
  print( round(as.data.frame(anova_tab), 4))
  
  anova_tab <- anova(model.Dummy.intr8, type = 3)
  print( round(as.data.frame(anova_tab), 4))
  
  message("Analysis completed. Outputs saved as:")
  message(fix_effect_file)
  message(rand_effect_file)
}

data_path <- "P:/3026008.01/Data" 
out_path <- "./output"

# Read in data
df_A = read.csv(file.path(data_path, "exp1_A_all_w_VAE_norm_exc_outlier_m.csv"), header = TRUE)

# delete outliers
#df_A  <-  df_A[df_A$outlier==0, ]
  
# Factorize variables
df_A$sub_id <- factor(df_A$sub_id)
df_A$ComSourFlag <- factor(df_A$ComSourFlag, order = FALSE)

df_A$rec_case <- ((df_A$VPosInAV - df_A$APosInAV <= 0) & (df_A$truePos <= df_A$VPosInAV)) | 
                ((df_A$VPosInAV - df_A$APosInAV >= 0) & (df_A$truePos >= df_A$VPosInAV))

df_A$opp_case <- ((df_A$VPosInAV - df_A$APosInAV <= 0) & (df_A$truePos >= df_A$VPosInAV)) | 
                ((df_A$VPosInAV - df_A$APosInAV >= 0) & (df_A$truePos <= df_A$VPosInAV))

run_lme_analysis(df_A, out_path, suffix = "")

## recalibration cases
run_lme_analysis(df_A[df_A$rec_case == 1, ], out_path, suffix = "_rec")
## opposite
run_lme_analysis(df_A[df_A$opp_case == 1, ], out_path, suffix = "_opp")


