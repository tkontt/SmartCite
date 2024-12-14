*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      0.5 seconds
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${CREATE_TEST_CITATIONS_URL}  http://${SERVER}/create_test_citations
${CREATE_TEST_CITATION_URL}  http://${SERVER}/create_test_citation
${CREATE_TEST_CITATION_WITH_OPTIONAL_FIELD_URL}  http://${SERVER}/create_test_citation_with_optional_field
${NEW_CITATION_URL}   http://${SERVER}
${BROWSER}    chrome
${HEADLESS}   false
${CREATE}     //button[@name='create']
${GET_BIBTEX}     //button[@name='get_bibtex']
${IMPORT_BIBTEX}     //button[@name='import_bibtex']
${IMPORT}     //button[@name='import']
${EDIT}       //input[@name='edit']
${UPDATE}     //button[@name='update']
${DETAILS_FIRST_CITATION}    //button[@id='show_citation_button_0']
${SELECT-CITATION-TYPE}  //select[@name='citation-type']

*** Keywords ***
Open And Configure Browser
    IF  $BROWSER == 'chrome'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
    ELSE IF  $BROWSER == 'firefox'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0
        Call Method  ${options}  add_argument  --headless
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Reset Application
    Go To  ${RESET_URL}

Create Test Citations
    Go To  ${CREATE_TEST_CITATIONS_URL}

Create Test Citation
    [Arguments]  ${author}  ${title}  ${year}  ${journal}
    Go To  ${CREATE_TEST_CITATION_URL}/${author}/${title}/${year}/${journal}

Create Test Citation With Optional Field
    Go To  ${CREATE_TEST_CITATION_WITH_OPTIONAL_FIELD_URL}

Home Page Should Be Open
    Title Should Be  Citation App

Go To Home Page
    Go To  ${HOME_URL}

Go To New Citation Page
    Go To  ${NEW_CITATION_URL}

Citation Page Should Be Open
    Title Should Be  Citation Details

Select Citation Type
    [Arguments]  ${type}
    Click Element  ${SELECT-CITATION-TYPE}
    Wait Until Element Is Visible  ${type}
    Click Element  ${type}

View First Citation Details
    Wait Until Element is visible  ${DETAILS_FIRST_CITATION}  timeout=5s
    Set Focus To Element  ${DETAILS_FIRST_CITATION}    
    Click Element  ${DETAILS_FIRST_CITATION}