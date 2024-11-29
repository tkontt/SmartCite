*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
When Get BibTeX Is Clicked The Generated BibTeX Is Shown
    Create Test Citation  Author1  Title1  2024  Journal1
    Go To Home Page
    Click Get Bibtex
    Wait Until Element Is Visible  copy_bibtex_button
    Page Should Contain  author = \{Author1\},\n\ttitle = \{Title1\},\n\tyear = \{2024\},\n\tjournal = \{Journal1\}

*** Keywords ***
Click Get Bibtex
    Scroll Element Into View  ${GET_BIBTEX}
    Wait Until Element is visible  ${GET_BIBTEX}  timeout=5s
    Set Focus To Element  ${GET_BIBTEX}    
    Click Element  ${GET_BIBTEX}