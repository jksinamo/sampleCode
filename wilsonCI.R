#Wilson confidence interval
wilson_interval <- function(n, phat, type){
  #setting up an empty vector
  LB <- rep(NA, length(n)); UB <- rep(NA, length(n))
  
  # if we use wilson
  if (type == 'wilson'){
    for(i in 1:length(n)){
      
      mid = (phat[i] * n[i] + (1.96^2)/2) / ( n[i]+ 1.96^2)
      plusMinus = (1.96*( n[i]^(1/2) )/( n[i]+1.96^2)) * 
        ((phat[i] * (1-phat[i]) ) + (1.96^2)/(4 * n[i]))^(1/2)
      
      LB[i] <- mid - plusMinus; UB[i] <- mid + plusMinus
    }
  }
  
  # if we use wilson with continuity correction
  #   from: Newcombe(1998) Two-sided confidence interval for the single proportion:
  #           comparison of seven methods
  else if(type == 'wilson continuity correction'){
    for(i in 1:length(n)){
      LB[i] <- (2*n[i] * phat[i] + 3.8416 - 
                  (1.96*sqrt(3.8416 - 1/n[i] +  4*n[i] * phat[i] * (1 - phat[i]) + (4*phat[i] - 2) ) + 1))/
        (2*(n + 3.8416))
      UB[i] <- (2*n[i] * phat[i] + 3.8416 + 
                  (1.96*sqrt(3.8416 - 1/n[i] +  4*n[i] * phat[i] * (1 - phat[i]) - (4*phat[i] - 2) ) + 1))/
        (2*(n + 3.8416))
    }
  }
  
  # if we use wilson with lower bound modification
  # from BCD (2001); alternative -> BinomCI
  # function has been tested against BinomCI and binomCI, outputs were the same
  else if(type == 'modified wilson'){
    for(i in 1:length(n)){
      x = phat[i] * n[i]
      mid = (phat[i] * n[i] + (1.96^2)/2) / ( n[i]+ 1.96^2)
      plusMinus = (1.96*( n[i]^(1/2) )/( n[i]+1.96^2)) * 
        ((phat[i] * (1-phat[i]) ) + (1.96^2)/(4 * n[i]))^(1/2)
      
      # my implementation of BCD p.112, section 4.1.1 after equation 10
      #   when n <= 50, then use x* = 2, when n > 50, use x* = 3
      if((n[i] <= 50 & x > 0 & x < 3) | n[i] > 50 & x >= 3){
        #x* = 2 is recommended by BCD for sample size below 50
        LB[i] <- (1/2)*qchisq(0.05, 2*x)/n[i]
      }
      else{
        LB[i] <- mid - plusMinus
      }
      # no changes in upper bound
      UB[i] <- mid + plusMinus
    }
  }
  
  # Making sure bounds stay between 0 and 1 [inclusive]
  for(i in 1:length(n)){
    if(LB[i] < 0){
      LB[i] <- 0
    }
    if(UB[i] > 1){
      UB[i] <- 1
    }
  }
  # return dataframe for easier access and data modification
  return(data.frame('lower_bound' = LB, 'upper_bound' = UB))
}