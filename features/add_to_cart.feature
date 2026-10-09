Feature: Add to cart
  
  @TC-003
  Scenario: Add product to cart successfully
    Given I am logged in to the application
    When I click on a product
    And I click on the Add to cart button
    And I click on the Cart button
    Then I should see the added product in the cart