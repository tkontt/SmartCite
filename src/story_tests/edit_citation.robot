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
    Sleep  0.25
    Click Edit
    Wait Until Element Is Visible  year
    Sleep  0.25
    Input Text  year  2023
    Sleep  0.25
    Click Update
    Sleep  0.25
    Page Should Contain  2023
    Go To Home Page
    Page Should Contain  2023
    
After adding an optional field in edit, the field exists
    Create Test Citation With an Optional Field
    Page Should Contain  volume
    Page Should Contain  5050

After removing an optional field and pressing update, the field no longer exists
    Create Test Citation With an Optional Field
    Click Citation Row  1
    Sleep  0.25
    Click Edit
    Wait Until Element is visible  //button[@value='remove']  timeout=0.5s
    Click Element  //button[@value='remove']
    Sleep  0.25
    Click Update
    Click Citation Row  1
    Sleep  0.25
    Page Should Not Contain  volume
    Page Should Not Contain  5050

After removing an optional field and closing the edit without updating, the field still exists
    Create Test Citation With an Optional Field
    Click Citation Row  1
    Sleep  0.25
    Click Edit
    Wait Until Element is visible  //button[@value='remove']  timeout=0.5s
    Click Element  //button[@value='remove']
    Sleep  0.25
    Wait Until Element is visible  //button[@name='exit-edit']  timeout=0.25s
    Click Element  //button[@name='exit-edit']
    Reload Page
    Click Citation Row  1
    Sleep  0.25
    Page Should Contain  volume
    Page Should Contain  5050

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

Create Test Citation With an Optional Field
    Create Test Citation  TestAuthor  Title  2020  Journal
    Go To Home Page
    Click Citation Row  1
    Sleep  0.25
    Click Edit
    Wait Until Element Is Visible  add-field-edit
    Input Text  add-field-edit  volume
    Click Element  add-field-edit-btn
    Wait Until Element Is Visible  volume
    Input Text  volume  5050
    Click Update
    Sleep  0.25