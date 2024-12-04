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
    Sleep  0.2
    Page Should Contain  article
    Input Text  author  TestAuthor1
    Input Text  title  Title
    Input Text  journal  Journal
    Input Text  year  2024
    Sleep  0.25
    Click Create
    Page Should Not Contain  No citations found.
    Page Should Contain  TestAuthor1

When selecting a different citation type, the mandatory fields change
    Go To Home Page
    Click Button  create_citation_button
    Wait Until Element Is Visible  citation-type
    Select Citation Type  book
    Page Should Contain  editor
    Page Should Contain  publisher

After selecting and adding a different citation type, the fields are correct
    Go To Home Page
    Click Button  create_citation_button
    Wait Until Element Is Visible  citation-type
    Select Citation Type  booklet
    Input Text  title  Title123
    Sleep  0.25
    Click Create
    Page Should Contain  Title123
    Page Should Contain  booklet

After adding an optional field to a citation, the field exists
    Go To Home Page
    Click Button  create_citation_button
    Wait Until Element Is Visible  year
    Sleep  0.2
    Page Should Contain  article
    Input Text  author  TestAuthor1
    Input Text  title  Title
    Input Text  journal  Journal
    Input Text  year  2024
    Input Text  add-field-new  pages
    Click Element  add-field-new-btn
    Sleep  0.25
    Input Text  pages  2-5
    Sleep  0.25
    Click Create
    Double Click Element  //td[contains(text(), "1")]
    Citation Page Should Be Open
    Page Should Contain  pages
    Page Should Contain  2-5

*** Keywords ***
Click Create
    Scroll Element Into View  ${CREATE}
    Wait Until Element is visible  ${CREATE}  timeout=5s
    Set Focus To Element  ${CREATE}    
    Click Element  ${CREATE}