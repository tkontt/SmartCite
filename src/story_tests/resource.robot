*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      0.5 seconds
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${CREATE_TEST_CITATIONS_URL}  http://${SERVER}/create_test_citations
${CREATE_TEST_CITATION_URL}  http://${SERVER}/create_test_citation
${NEW_CITATION_URL}   http://${SERVER}
${BROWSER}    chrome
${HEADLESS}   false
${CREATE}     //button[@name='create']
${EDIT}       //input[@name='edit']
${UPDATE}     //button[@name='update']

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

Home Page Should Be Open
    Title Should Be  Citation App

Go To Home Page
    Go To  ${HOME_URL}

Go To New Citation Page
    Go To  ${NEW_CITATION_URL}

Citation Page Should Be Open
    Title Should Be  Citation Details