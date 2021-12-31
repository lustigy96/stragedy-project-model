
#directories
d_loc = "C:\\YAEL\\TAU\\projects\\stragedy-project\\"
d_income_path_postfix = "income_statement\\"
d_ratios_path_postfix = "ratios\\"
d_compustat_path_postfix="compustat\\"
d_proccessed_path_postfix = "processed\\"

#files_locations
sp500_info_file=d_loc+"S&P500-Info.csv";
compustat_file_name= "snp-500-compustat-2.csv"
compustat_original_data=    d_loc+d_compustat_path_postfix  +compustat_file_name
compustat_normalized_file = d_loc+d_proccessed_path_postfix +compustat_file_name.replace('.csv',"")+"-normalized.csv"
compustat_normalized_calssified_file =compustat_normalized_file.replace('.csv',"")+"-classified.csv"
compustat_mki = d_loc+d_proccessed_path_postfix+"marketing_intensity_relevants.csv"
compustat_rdi = d_loc+d_proccessed_path_postfix+"rd_intensity_relevants.csv"

Lregs_all_simple_file = d_loc+d_proccessed_path_postfix+"Lreg_all_simple.csv"
Lreg_all_simple_by_sector_file = d_loc+d_proccessed_path_postfix+"Lreg_all_simple_by_sector.csv"
Lregs_rdi_compustat_file = d_loc+d_proccessed_path_postfix+"rdi_Lregs.csv"
# fields
field_income_statement= ["date",
                      "revenue",
                      "research_and_development_expenses",
                      "eps_-_earnings_per_share"]
field_ratios =["date",
            "gross_margin",
            "roe_-_return_on_equity",
            "book_value_per_share",
            ]
#regression
linear_regression_y=["book_value","roe","market_to_book_ratio","firm_size","earning_per_share"]
p_distinction_val=0.05