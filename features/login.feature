Feature: Demoblaze login

   Background:
     Given user is on the Demoblaze application
   
   @TC-001
   Scenario: Login with valid credentials
     When users open the login dialog
     And user enters the valid username and password
     And user clicks the login button
     Then user should be logged in successfully

   @TC-002
   Scenario: Login with invalid credentials
     When users open the login dialog
     And user enters the invalid username and password
     And user clicks the login button with invalid credentials
     Then login should fails with an error message
"""
   Scenario: Login with blank username
     When user opens the login dialog
     And user enters blank username and valid password
     And user clicks the login button
     Then login should fail with an error message

   Scenario: Login with blank password
     When user opens the login dialog
     And user enters valid username and blank password
     And user clicks the login button
     Then login should fail with an error message
"""