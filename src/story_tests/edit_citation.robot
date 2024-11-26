*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
After editing a citation, changes are visible
    Create Test Citations
    Go To Home Page
    Click Citation Row  1
    Citation Page Should Be Open
    Click Edit
    Wait Until Element Is Visible    year
    Sleep  0.25
    Input Text  year  2023
    Sleep  0.25
    Click Update
    Sleep  0.25
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