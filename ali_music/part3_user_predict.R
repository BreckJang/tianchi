input_file <- 'd://tianchi//p2_music//part2_user_frequency.csv'
output_file <- 'd://tianchi//p2_music//user_predict_tmp.csv'
given_day_num <- 183
predict_day_num <- 61

library(forecast)
origin_data <- read.csv(input_file, header=FALSE)

for(i in 1:nrow(origin_data)){
  tmp <- as.numeric(origin_data[i,3: given_day_num+2])
  tmp_2 <- ts(tmp, start=1)
  fit <- auto.arima(tmp_2)
  result <- forecast(fit, h=predict_day_num)
  # plot(result)
  name <- as.vector(origin_data[i, 2])
  tmp_1 <- data.frame(result)$Point.Forecast
  cat(name, tmp_1, file=output_file, append=TRUE, sep=',')
  cat('\n', file=output_file, append=TRUE, sep='')
}