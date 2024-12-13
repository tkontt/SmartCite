*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
After editing a citation, changes are visible
    Create Test Citation  TestAuthor  Title  2006  Journell
    Go To Home Page
    Click Citation Row  1
    Click Edit
    Wait Until Element Is Visible  year
    Input Text  year  2023
    Input Text  journal  Journal
    Click Update
    Sleep  0.25
    View First Citation Details
    Page Should Contain  2023
    Page Should Contain  Journal
    
After adding an optional fields in edit, the fields exist
    Create Test Citation  TestAuthor  Title  2020  Journal11
    Go To Home Page
    Click Citation Row  1
    Click Edit
    Wait Until Element Is Visible  add-field-edit
    Input Text  add-field-edit  volume
    Click Element  add-field-edit-btn
    Wait Until Element Is Visible  volume
    Input Text  volume  5050
    Input Text  add-field-edit  month
    Click Element  add-field-edit-btn
    Wait Until Element Is Visible  month
    Input Text  month  April
    Click Update
    Sleep  0.25
    View First Citation Details
    Page Should Contain  volume
    Page Should Contain  5050
    Page Should Contain  month
    Page Should Contain  April

After removing an optional field and pressing update, the field no longer exists
    Create Test Citation With Optional Field
    Sleep  0.25
    Go To Home Page
    Click Citation Row  1
    Click Edit
    Wait Until Element is visible  //button[@value='remove']  timeout=0.5s
    Click Element  //button[@value='remove']
    Sleep  0.25
    Click Update
    Sleep  0.25
    View First Citation Details
    Page Should Not Contain  volume
    Page Should Not Contain  5050

After removing an optional field and closing the edit without updating, the field still exists
    Create Test Citation With Optional Field
    Sleep  0.25
    Go To Home Page
    Click Citation Row  1
    Click Edit
    Wait Until Element is visible  //button[@value='remove']  timeout=0.5s
    Click Element  //button[@value='remove']
    Sleep  0.25
    Wait Until Element is visible  //button[@name='exit-edit']  timeout=0.25s
    Click Element  //button[@name='exit-edit']
    Reload Page
    View First Citation Details
    Page Should Contain  volume
    Page Should Contain  5050

Error message is shown if user tries to add an existing field
    Create Test Citation With Optional Field
    Go To Home Page
    Click Citation Row  1
    Click Edit
    Wait Until Element Is Visible  add-field-edit
    Input Text  add-field-edit  author
    Click Element  add-field-edit-btn
    Page Should Contain  A field with the given name already exists.

Error message is shown if user tries to add a field with no name
    Create Test Citation With Optional Field
    Go To Home Page
    Click Citation Row  1
    Click Edit
    Wait Until Element Is Visible  add-field-edit
    Click Element  add-field-edit-btn
    Page Should Contain  Pease name the field.


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
