rm(list = ls())
setwd("C:/Users/wenlou/Documents/R scripts/RecaliProject")
library(lme4)
library(openxlsx)
library(lmerTest)  # lme4 wrapper that appends p-values
library(dplyr)
library(openxlsx)
#########################################################################################

## read in data
data_path <- "P:/3026008.01/Data" 
out_path <- "./output"

df_A = read.csv(file.path(data_path, "exp1_A_all_w_VAE_norm_exc.csv"), header = TRUE)
str(df_A)

df_A$sub_id <- factor(df_A$sub_id)
df_A$ComSourFlag <- factor(2-df_A$ComSourFlag, order=FALSE) # 1 - common, 0 - separate
#df_A$delta_VA <- factor(df_A$delta_VA, order=FALSE)
export_lme_to_excel <- function(
    model,
    file ,
    include_random = FALSE,
    digits = 4
) {
  
  # --- Type III ANOVA ---
  anova_tab <- anova(model, type = 3)
  anova_df  <- round(as.data.frame(anova_tab), digits)
  
  # --- Fixed effects ---
  fixef_tab <- summary(model)$coefficients
  fixef_df  <- round(as.data.frame(fixef_tab), digits)
  
  # --- Random effects (optional) ---
  if (include_random) {
    ranef_df <- round(as.data.frame(VarCorr(model)), digits)
  }
  
  # --- Create workbook ---
  wb <- createWorkbook()
  
  addWorksheet(wb, "Type_III_ANOVA")
  addWorksheet(wb, "Fixed_Effects")
  
  writeData(wb, "Type_III_ANOVA", anova_df, rowNames = TRUE)
  writeData(wb, "Fixed_Effects", fixef_df, rowNames = TRUE)
  
  if (include_random) {
    addWorksheet(wb, "Random_Effects")
    writeData(wb, "Random_Effects", ranef_df)
  }
  
  saveWorkbook(wb, file, overwrite = TRUE)
  
  message("✔ LME results written to: ", file)
}

options(contrasts = c("contr.sum", "contr.poly"))
#########################################################################################
# predicted causal confidence by a linear and a quadratic regressor of spatial disparity
lme_conf<-lmer(confLvl~ (abs_delta_VA * ComSourFlag)   +  (I(abs_delta_VA^2) * ComSourFlag) + (abs_delta_VA|sub_id), data=df_A ,control = lmerControl(optimizer = "Nelder_Mead"))

summary(lme_conf)

export_lme_to_excel(
  lme_conf,
  file = file.path(out_path, "raw_conf_lme.xlsx")
)


#########################################################################################
df_A$delta_VA <- factor(df_A$delta_VA, order=FALSE)
# create 8 dummy variables - each for one spatial disparity
dummy8 <- model.matrix(~ interaction(df_A$delta_VA) - 1)
colnames(dummy8) <- paste0("av.", c('n24', 'n16', 'n8', '0', 'p8', 'p16', 'p24'))
df_A <- cbind(df_A, dummy8)

# LME model
lmer_resultsA1<-lmer(respPos~ av.n24 + av.n16 + av.n8 + av.p8 + av.p16 + av.p24 + 
      truePos + (1+truePos|sub_id), data=df_A ,control = lmerControl(optimizer = "Nelder_Mead"))
summary(lmer_resultsA1)

#  extracting the coef from 8 dummy variable models
fix.coefs <- as.data.frame(coef(summary(lmer_resultsA1))) %>%
rename("coef.value" = "Estimate",
        "std.err" = "Std. Error",
        "t.value" = "t value",
        "p.value" =  "Pr(>|t|)")

fix.coefs[, 'effects'] <- fix.coefs[, 'coef.value'] + c(0, rep(fix.coefs[1, 'coef.value'], nrow(fix.coefs) - 2), 0)
rownames(fix.coefs)[1] <- "av.0"
fix.coefs$delta_VA <- c(0,-24,-16,-8,8,16,24, -99)

# random effects
rand.coefs <- ranef(lmer_resultsA1)$sub_id%>%rename(c("randInt" = "(Intercept)", "randtruePos" = "truePos"))

#write table
write.csv(fix.coefs, file.path(out_path, "raw_resp_fix_effect.csv") , row.names = TRUE)
write.csv(rand.coefs, file.path(out_path, "raw_resp_rand_effect.csv") , row.names = FALSE)

