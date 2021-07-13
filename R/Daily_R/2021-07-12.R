install.packages("rjson")
install.packages("mailR")
install.packages("rJava")
install.packages("sendmailR")


library(jsonlite)
library(mailR)
library(sendmailR)
library(rJava)

send.mail(from = sender,
          to = recipients,
          subject = 'Teest email from RStudio',
          body = 'Test email body',
          smtp = list(host.name = "smtp.gmail.com", 
                      port = 465, 
                      user.name = "swallow9212@gmail.com",            
                      passwd="Wogns62412!",
                      ssl = TRUE),
          authenticate  = TRUE,
          send = TRUE)

from <- sprintf("<sendmailR@\\%s>", Sys.info()[4])
to <- "<swallow9212@gmail.com>"
subject <- "Hello from R"
body <- list("It works!", mime_part(iris))
send.mail(from, to, subject, body,
         control=list(smtpServer="ASPMX.L.GOOGLE.COM"))

Server<-list(smtpServer= "smtp.example.io")

library(sendmailR)
from <- sprintf("<user@sender.com>","The Sender") # the sender’s name is an optional value
to <- sprintf("<user@recipient.com>")
subject <- "Test email subject"
body <- "Test email body"

sendmailR::sendmail(from,to,subject,body,control=list(smtpServer= "smtp.example.io"))

 
