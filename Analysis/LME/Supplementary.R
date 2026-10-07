rm(list = ls())
setwd("C:/Users/wenlou/Documents/R scripts")
library(lme4)
library(openxlsx)
library(lmerTest)  # lme4 wrapper that appends p-values
library(dplyr)
#install.packages('bridgesampling')
# library(brms)
# library(bridgesampling)
setwd("C:/Users/wenlou/Documents/R scripts/RecaliProject")
data_path <- "P:/3026008.01/Data" 
out_path <- "./output"


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


################################################################
####section A1 - validate VAE for auditory and visual modality##
################################################################
test_VAE_valid <- function(modality, test_type){

    if (modality =='A'){
        filename = 'exp1_A_all_w_VAE_norm_exc.csv'
    }else{
        filename = 'exp1_V_all_exc.csv'
    }

    df = read.csv(file.path(data_path, filename), header = TRUE)
    df$sub_id <- factor(df$sub_id)
    df$ComSourFlag <- factor(df$ComSourFlag, order=FALSE) # 1 - common, 0 - separate
    #df$delta_VA <- factor(df$delta_VA, order=FALSE)

    if (test_type == 'ANOVA'){
      full_lmer <- lmer(
        respPos ~ delta_VA + truePos + (1 | sub_id),
        data = df,
        REML = FALSE
      )
      
      null_lmer <- lmer(
        respPos ~ truePos + (1 | sub_id),
        data = df,
        REML = FALSE
      )
      
      anova(null_lmer, full_lmer)
      
    } else if (test_type == 'BF_BIC') {
      full_lmer <- lmer(
        respPos ~ delta_VA + truePos + (1 | sub_id),
        data = df,
        REML = FALSE
      )
      
      null_lmer <- lmer(
        respPos ~ truePos + (1 | sub_id),
        data = df,
        REML = FALSE
      )
      
      BF01 <- exp((BIC(null_lmer) - BIC(full_lmer)) / 2)
      print(BF01)
      #summary(full_lmer)$coefficients["delta_VA", ]
      #fixef(full_lmer)["delta_VA"]
      confint(full_lmer, parm = "delta_VA")
      
    }

}

test_VAE_valid('A', 'ANOVA')
test_VAE_valid('V', 'ANOVA')

test_VAE_valid('V', 'BF_BIC')

##############################################
####section A2 - determinants for VAE#########
##############################################
df_A = read.csv(file.path(data_path, "exp1_A_all_w_VAE_norm_exc.csv"), header = TRUE)
str(df_A)

df_A$sub_id <- factor(df_A$sub_id)
df_A$ComSourFlag <- factor(df_A$ComSourFlag, order=FALSE)
df_A$confLvl <- factor(df_A$confLvl, order=FALSE)

model1 <- lmer(flipVAE~ (abs_delta_VA +I(abs_delta_VA^2)) * ComSourFlag  * confLvl  + (1|sub_id), data=df_A
                    ,control = lmerControl(optimizer = "Nelder_Mead"))
summary(model1)

model2 <- lmer(flipVAE~  abs_delta_VA  * ComSourFlag  * confLvl + ComSourFlag*I(abs_delta_VA^2) +  (1|sub_id), data=df_A
               ,control = lmerControl(optimizer = "Nelder_Mead"))
summary(model2)

model3 <- lmer(flipVAE~  abs_delta_VA  * ComSourFlag  * confLvl  +  (1|sub_id), data=df_A
               ,control = lmerControl(optimizer = "Nelder_Mead"))
summary(model3)# win

anova(model3, model2)

model4 <- lmer(flipVAE~  abs_delta_VA  * ComSourFlag  * confLvl +I(abs_delta_VA^2) +  (1|sub_id), data=df_A
               ,control = lmerControl(optimizer = "Nelder_Mead"))
summary(model4)

# organize into excel 
fix.coefs <- as.data.frame(coef(summary(model3))) %>%
  rename("coef.value" = "Estimate",
         "std.err" = "Std. Error",
         "t.value" = "t value",
         "p.value" = "Pr(>|t|)")

write.xlsx(fix.coefs,file.path(out_path, paste0("supplementary.xlsx")) , rowNames = TRUE)

anova_tab <- anova(model3, type = 3)
anova_df  <- round(as.data.frame(anova_tab), 4)
#write.xlsx(fix.coefs,file.path(out_path, paste0("supplementary.xlsx")) , rowNames = TRUE)
anova_df

###################################
####section 2 - non-linear effects

model.quar1 <- lmer(flipVAE~ (abs_delta_VA  + I(abs_delta_VA^2) ) * ComSourFlag  + (1|sub_id), data=df_A
                    ,control = lmerControl(optimizer = "Nelder_Mead"))
summary(model.quar1)


model.quar2 <- lmer(flipVAE~ abs_delta_VA  + I(abs_delta_VA^2) * ComSourFlag  + (1|sub_id), data=df_A
                    ,control = lmerControl(optimizer = "Nelder_Mead"))

#summary(model.quar5)
sink("C:\\Users\\wenlou\\Documents\\Python Scripts\\plot4paper\\sup\\supLMEsummary2.txt")  # Redirect output to a file
summary(model.quar2)
sink() 
anova(model.quar1, model.quar2) #winner - model.quar2

anova_tab <- anova(model.quar2, type = 3)
anova_df  <- round(as.data.frame(anova_tab), 4)
#write.xlsx(fix.coefs,file.path(out_path, paste0("supplementary.xlsx")) , rowNames = TRUE)
anova_df

