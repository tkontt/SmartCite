*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
When Header Is Clicked The Citations Are Sorted
    Create Test Citations
    Go To Home Page
    Click Table Header    Author
    # 2 on yläotsikon "Author" indeksi alkaen luvusta 1. Jos otsikoiden järjestys muuttuu niin pitää muuttaa. Sama alemmassa testissä.
    Verify Table Row  2  1  Author1
    Verify Table Row  2  2  Author2
    Verify Table Row  2  3  Author3

When Header Is Clicked Twice The Sorting Is Reversed
    Create Test Citations
    Go To Home Page
    Click Table Header  Year
    Click Table Header  Year
    Verify Table Row  4  1  2019
    Verify Table Row  4  2  2018
    Verify Table Row  4  3  2017

When Citations Are Sorted The Previous Relative Order Is Kept
    Create Test Citation  Author1  Title1  2015  Journal1
    Create Test Citation  Author2  Title1  2014  Journal1
    Create Test Citation  Author1  Title1  2016  Journal1
    Create Test Citation  Author2  Title1  2018  Journal1
    Create Test Citation  Author1  Title1  2014  Journal1
    Create Test Citation  Author1  Title1  2017  Journal1
    Go To Home Page
    Click Table Header  Year
    Click Table Header  Author
    Verify Table Row  4  1  2014
    Verify Table Row  4  2  2015
    Verify Table Row  4  3  2016
    Verify Table Row  4  4  2017

*** Keywords ***
Click Table Header
    [Arguments]  ${header}
    Click Element  //th[contains(text(), "${header}")]

Verify Table Row
    [Arguments]  ${column_index}  ${row_index}  ${expected_value}
    ${first_element}=  Get Text  //table[@id="citations-table"]/tbody/tr[${row_index}]/td[${column_index}]
    Should Be Equal  ${first_element.strip()}  ${expected_value}

Click Create
    Scroll Element Into View  ${CREATE}
    Wait Until Element is visible  ${CREATE}  timeout=5s
    Set Focus To Element  ${CREATE}    
    Click Element  ${CREATE}