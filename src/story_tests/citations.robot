*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
At start there are no citations
    Go To Home Page
    Home Page Should Be Open
    Page Should Contain  You haven't added any citations

After adding a citation, there is one
    Go To Home Page
    Click Link  Create new citation
    New Citation Page Should Be Open
    Input Text  key  Key123
    Input Text  title  Title
    Input Text  author  Author
    Input Text  year  2024
    Input Text  publisher  Publisher
    Execute Javascript   window.scrollTo(0, document.body.scrollHeight)
    Sleep  1
    Click Button  create
    Page Should Not Contain  You haven't added any citations
    Page Should Contain  Key123

*** Test Cases ***
When Header Is Clicked The Citations Are Sorted
    Go To Home Page
    Create Test Citation    2
    Create Test Citation    1
    Create Test Citation    3
    Click Table Header      Author
    # 4 on yläotsikon "Author" indeksi alkaen luvusta 1. Jos otsikoiden järjestys muuttuu niin pitää muuttaa. Sama alemmassa testissä.
    Verify First Element    4    Author1

When Header Is Clicked Twice The Sorting Is Reversed
    Go To Home Page
    Create Test Citation    2
    Create Test Citation    1
    Create Test Citation    3
    Click Table Header      Year
    Click Table Header      Year
    Verify First Element    6    Year3

*** Keywords ***
Create Test Citation
    [Arguments]  ${append}
    Click Link  Create new citation
    Input Text  key  Key${append}
    Input Text  title  Title${append}
    Input Text  author  Author${append}
    Input Text  year  Year${append}
    Input Text  publisher  Publisher${append}
    Execute Javascript   window.scrollTo(0, document.body.scrollHeight)
    Sleep  1
    Click Button  create

Click Table Header
    [Arguments]  ${header}
    Click Element    //th[contains(text(), "${header}")]

Verify First Element
    [Arguments]  ${column_index}  ${expected_value}
    ${first_element}=    Get Text    //table[@id="citationsTable"]/tbody/tr[1]/td[${column_index}]
    Should Be Equal    ${first_element.strip()}    ${expected_value}