*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
Clicking A Field In The Dropdown Should Toggle Field Visibility
    Create Test Citations
    Go To Home Page
    Home Page Should Be Open

    Page Should Contain Visible Text  Author1

    Page Should Not Contain Visible Text  CustomField1

    Click Button  dropdownMenuButton

    Click Element  xpath=//label[contains(text(), 'Custom_field')]/input
    Page Should Contain Visible Text  CustomField1

    Click Element  xpath=//label[contains(text(), 'Author')]/input
    Page Should Not Contain Visible Text  Author1

    Click Element  xpath=//label[contains(text(), 'Custom_field')]/input
    Page Should Not Contain Visible Text  CustomField1

*** Keywords ***
Page Should Contain Visible Text
    [Arguments]  ${text}
    Element Should Be Visible  xpath=//*[contains(text(), '${text}')]

Page Should Not Contain Visible Text
    [Arguments]  ${text}
    Element Should Not Be Visible  xpath=//*[contains(text(), '${text}')]