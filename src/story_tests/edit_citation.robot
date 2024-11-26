*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
After editing a citation, changes are visible
    Go To Home Page
    Create Test Citation  1
    Click Citation Row  1
    Citation Page Should Be Open
    Click Edit
    Wait Until Element Is Visible    year
    Wait Until Element Is Enabled    year
    Input Text  year  2023
    Click Update
    Sleep  1
    Citation Page Should Be Open
    Page Should Contain  2023
    Go To Home Page
    Page Should Contain  2023



*** Keywords ***
Click Create
    Scroll Element Into View  ${CREATE}
    Wait Until Element is visible  ${CREATE}  timeout=5s
    Set Focus To Element  ${CREATE}    
    Click Element  ${CREATE}

Create Test Citation
    [Arguments]  ${append}
    Click Element  xpath=//button[contains(text(), 'Create new citation')]
    Wait Until Element Is Visible    year
    Wait Until Element Is Enabled    year
    Input Text  title  Title${append}
    Input Text  author  Author${append}
    Input Text  journal  Journal${append}
    Input Text  year  Year${append}
    Click Create

Click Citation Row
    [Arguments]  ${row}
    Double Click Element  //td[contains(text(), "${row}")]

Click Edit
    Scroll Element Into View  ${EDIT}
    Wait Until Element is visible  ${EDIT}  timeout=5s
    Set Focus To Element  ${EDIT}    
    Click Element  ${EDIT}

Click Update
    Scroll Element Into View  ${UPDATE}
    Wait Until Element is visible  ${UPDATE}  timeout=5s
    Set Focus To Element  ${UPDATE}    
    Click Element  ${UPDATE}

Page Should Contain Visible Text
    [Arguments]  ${text}
    Element Should Be Visible  xpath=//*[contains(text(), '${text}')]