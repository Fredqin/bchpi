library(data.table)
library(plyr)

# import csv
data.raw = read.csv("csv/hpi_data.csv")

# format benchmark to number
data.raw$benchmark = as.numeric(data.raw$benchmark)

# 10 years, increase mostly area and house type

# aggregate the data by area and type
formatted_data = data.table(data.raw)
# rouped_data = formatted_data[, lapply(.SD[benchmark== head(benchmark)], head), by=list(type, area)]
# grouped_data = formatted_data[, .SD[nrow(.SD),], by=list(type, area)]

grouped_data = formatted_data[, 
                              list(benchmark_increase_rate = (.SD[1,]$benchmark - .SD[nrow(.SD),]$benchmark)/ (.SD[nrow(.SD),]$benchmark),
                                   house_price_index_change = (.SD[1,]$price_index - .SD[nrow(.SD),]$price_index)/ (.SD[nrow(.SD),]$price_index)), 
                              by=list(type, area)]
grouped_data
write.csv(grouped_data, file = "./csv/hpi_data_analysis_results.csv", row.names=FALSE)
