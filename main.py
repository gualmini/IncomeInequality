
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

gini_df = pd.read_csv("gini.csv")
gdp_df = pd.read_csv("gdp.csv")

gdp_df = gdp_df.dropna(subset=["Code"])
gdp_df = gdp_df[gdp_df["Entity"] != "World"]
gini_df = gini_df.dropna(subset=["Code"])



gdp_gini_df = gdp_df.iloc[:,[0, 2, 3]].copy()
merged_df = gdp_gini_df.merge(gini_df[["Entity", "Year", "Gini coefficient"]], on=["Entity", "Year"], how="left")
gdp_gini_df["Gini coefficient"] = merged_df["Gini coefficient"]
gdp_gini_df = gdp_gini_df.dropna(subset=["Gini coefficient"])

columns_to_be_checked_for_correlation = ["Gini coefficient", "GDP per capita"]

#calculate the Pearson and Spearman correlation coefficients at Global level
pearson_correlation, pearson_pvalue = pearsonr(gdp_gini_df[columns_to_be_checked_for_correlation][columns_to_be_checked_for_correlation[0]], gdp_gini_df[columns_to_be_checked_for_correlation][columns_to_be_checked_for_correlation[1]])
spearman_correlation, spearman_pvalue = spearmanr(gdp_gini_df[columns_to_be_checked_for_correlation][columns_to_be_checked_for_correlation[0]], gdp_gini_df[columns_to_be_checked_for_correlation][columns_to_be_checked_for_correlation[1]])

print(f"WORLD LEVEL - Pearson correlation coefficient between {columns_to_be_checked_for_correlation[0]} and {columns_to_be_checked_for_correlation[1]}: {pearson_correlation} (p-value: {pearson_pvalue})")
print(f"WORLD LEVEL - Spearman correlation coefficient between {columns_to_be_checked_for_correlation[0]} and {columns_to_be_checked_for_correlation[1]}: {spearman_correlation} (p-value: {spearman_pvalue})")


# calculate the Pearson and Spearman correlation coefficients and p-values per country

corr_table = pd.DataFrame(columns=["Country", "Pearson Correlation", "Pearson p-value", "Spearman Correlation", "Spearman p-value"])
for country in gdp_gini_df['Entity'].unique():
    country_df = gdp_gini_df[gdp_gini_df["Entity"] == country]
    if len(country_df) < 2:
        corr_table.loc[len(corr_table)] = [country, np.nan, np.nan, np.nan, np.nan]
    else:
        pearson_correlation, pearson_pvalue = pearsonr(country_df["Gini coefficient"], country_df["GDP per capita"])
        spearman_correlation, spearman_pvalue = spearmanr(country_df["Gini coefficient"], country_df["GDP per capita"])
        corr_table.loc[len(corr_table)] = [country, round(pearson_correlation, 2), pearson_pvalue, round(spearman_correlation, 2), spearman_pvalue]

corr_table = corr_table.sort_values(by="Pearson p-value", ascending=True, na_position="last")
pd.set_option('display.max_columns', None)
print("There is a significant negative correlation for several countries. These are the 10 countries with the lowest p-value")
print(corr_table.head(10))


