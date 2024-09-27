# Email App

An app to automatically pull information from Mie Trak, identify materials from that item, pull the relevant email-ids from Mie Trak supplier list and finally, sending all of them an email.
The app does this using by using the local outlook client on the host machine.

## Pulling data from Mie Trak
Since Mie Trak is an SQL server, we treat it like a simple relational database and use the REST API to make requests.
The API's code and how to implement it can be found in the`auto-server` repo. 

## Usage
clone the repo:
`git clone ...`

