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
    Input Text  author  TestAuthor1
    Input Text  year  2024
    Input Text  publisher  Publisher
    Scroll Down Page
    Click Button  create
    Page Should Not Contain  You haven't added any citations
    Page Should Contain  TestAuthor1

*** Test Cases ***
When Header Is Clicked The Citations Are Sorted
    Go To Home Page
    Create Test Citation  2
    Create Test Citation  1
    Create Test Citation  3
    Click Table Header    Author
    # 2 on yläotsikon "Author" indeksi alkaen luvusta 1. Jos otsikoiden järjestys muuttuu niin pitää muuttaa. Sama alemmassa testissä.
    Verify Table Row  2  1  Author1
    Verify Table Row  2  2  Author2
    Verify Table Row  2  3  Author3

When Header Is Clicked Twice The Sorting Is Reversed
    Go To Home Page
    Create Test Citation  2
    Create Test Citation  1
    Create Test Citation  3
    Click Table Header  Year
    Click Table Header  Year
    Verify Table Row  4  1  Year3
    Verify Table Row  4  2  Year2
    Verify Table Row  4  3  Year1

*** Keywords ***
Create Test Citation
    [Arguments]  ${append}
    Click Link  Create new citation
    Input Text  key  Key${append}
    Input Text  title  Title${append}
    Input Text  author  Author${append}
    Input Text  year  Year${append}
    Input Text  publisher  Publisher${append}
    Scroll Down Page
    Click Button  create

Click Table Header
    [Arguments]  ${header}
    Click Element  //th[contains(text(), "${header}")]

Verify Table Row
    [Arguments]  ${column_index}  ${row_index}  ${expected_value}
    ${first_element}=  Get Text  //table[@id="citations-table"]/tbody/tr[${row_index}]/td[${column_index}]
    Should Be Equal  ${first_element.strip()}  ${expected_value}

Scroll Down Page
    Execute Javascript  window.scrollTo(0, document.body.scrollHeight)
    Wait Until Keyword Succeeds  10s  0.2s  Scroll Finished

Scroll Finished
    ${scroll_height}  Execute Javascript  return document.body.scrollHeight
    ${scroll_top}  Execute Javascript  return window.scrollY + window.innerHeight
    Should Be Equal  ${scroll_height}  ${scroll_top}