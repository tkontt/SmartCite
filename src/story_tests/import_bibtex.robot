*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
When Importing BibTeX Type Citations They Go Into App 
    Go To Home Page
    Sleep  0.25
    Click Import From Bibtex
    Wait Until Element Is Visible  input_bibtex
    Input Text  input_bibtex  @article{Jou20,\nauthor = {Joulupukki},\ntitle = {Toimitusketjujen optimointi},\nyear = {2020},\njournal = {JouluTiedeJournal},}
    Sleep  0.25
    Click Button Import
    Sleep  0.25
    Page Should Contain  Joulupukki

*** Keywords ***
Click Import From Bibtex
    Scroll Element Into View  ${IMPORT_BIBTEX}
    Wait Until Element is visible  ${IMPORT_BIBTEX}  timeout=5s
    Set Focus To Element  ${IMPORT_BIBTEX}    
    Click Element  ${IMPORT_BIBTEX}

Click Button Import 
    Scroll Element Into View  ${IMPORT}
    Wait Until Element is visible  ${IMPORT}  timeout=5s
    Set Focus To Element  ${IMPORT}    
    Click Element  ${IMPORT}