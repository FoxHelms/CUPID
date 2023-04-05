# CUPID
Automated flight price tracking daemon

I run this 24/7 off my raspberry pi. It records the prices of flights from the source airport (in my case, Des Moines) to an arbitrary number of target airports. 
A running average price is kept. 
Any single flight that is significantly cheaper than the average, or is cheaper than a defined threshold price, gets saved.
An email containing the details of this flight is sent to my inbox.
