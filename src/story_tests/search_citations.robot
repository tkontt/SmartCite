*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
When Text Is Searched The Correct Citations Are Shown
    Create Test Citations
    Go To Home Page
    Input Text  search-input  Author6
    Page Should Not Contain Visible Text  Author5
    Page Should Not Contain Visible Text  Author7
    Page Should Contain Visible Text  Author6

When A Hidden Field Is Searched The Correct Citations Are Shown
    Create Test Citations
    Go To Home Page
    Input Text  search-input  CustomField6
    Page Should Not Contain Visible Text  Author5
    Page Should Not Contain Visible Text  CustomField6
    Page Should Contain Visible Text  Author6

*** Keywords ***
Page Should Contain Visible Text
    [Arguments]  ${text}
    Element Should Be Visible  xpath=//*[contains(text(), '${text}')]

Page Should Not Contain Visible Text
    [Arguments]  ${text}
    Element Should Not Be Visible  xpath=//*[contains(text(), '${text}')]