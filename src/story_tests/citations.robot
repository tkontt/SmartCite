*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
At start there are no citations
    Go To Home Page
    Home Page Should Be Open
    Page Should Contain  No citations found.

After adding a citation, there is one
    Go To Home Page
    Click Button  create_citation_button
    Wait Until Element Is Visible    year
    Sleep  0.25
    Page Should Contain  article
    Input Text  author  TestAuthor1
    Input Text  title  Title
    Input Text  journal  Journal
    Input Text  year  2024
    Sleep  0.25
    Click Create
    Page Should Not Contain  No citations found.
    Page Should Contain  TestAuthor1

When Text Is Searched The Correct Citations Are Shown
    Create Test Citations
    Go To Home Page
    Input Text  search-input  Author6
    Page Should Not Contain Visible Text  Author5
    Page Should Not Contain Visible Text  Author7
    Page Should Contain Visible Text  Author6

*** Keywords ***
Click Create
    Scroll Element Into View  ${CREATE}
    Wait Until Element is visible  ${CREATE}  timeout=5s
    Set Focus To Element  ${CREATE}    
    Click Element  ${CREATE}

Page Should Contain Visible Text
    [Arguments]  ${text}
    Element Should Be Visible  xpath=//*[contains(text(), '${text}')]

Page Should Not Contain Visible Text
    [Arguments]  ${text}
    Element Should Not Be Visible  xpath=//*[contains(text(), '${text}')]