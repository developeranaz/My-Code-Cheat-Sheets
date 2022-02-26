#!/usr/bin/expect

spawn heroku login -i
expect "Email"
send "dash@email.com";
send "\r"
expect "Password"
send "rawpassword"
expect "Logged"
interact
