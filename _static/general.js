// ===================================================================
// Disable Back Button, Selecting Text and Right Click on the Page
// ====================================================================
document.addEventListener('DOMContentLoaded', function () {
    history.pushState(null, null, location.href);
    window.onpopstate = function() {
        history.go(1);
    };
    document.addEventListener('selectstart', function (e) {
    e.preventDefault();
    });

    document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    });
});
if (typeof js_vars.completion_link !== 'undefined') {
    window.onload = function() {
        window.location.href = js_vars.completion_link;
    }
}
    
// ==================================================
// Validations to Ensure Answers have been Given
// ==================================================
function validateEthicsStatement() {
    const ethicsCheckbox = document.getElementById('ethics-check');
    const errorSpan = document.getElementById('ethics-error-message');

    if (!ethicsCheckbox.checked) {
        if (errorSpan) {
            errorSpan.textContent = 'Please confirm that you have read the ethics statement';
            errorSpan.style.display = 'block';
            errorSpan.style.fontWeight = 'bold';
        }
        return false; 
    }
    return true;
}

function validateAttentionCheck1() {
    const selectedOption = document.querySelector('input[name="attn_check_1"]:checked');
    const errorSpan = document.getElementById('attn-error-message');

    if (!selectedOption) {
        if (errorSpan) {
            errorSpan.textContent = 'Please select an option';
            errorSpan.style.display = 'block';
            errorSpan.style.fontWeight = 'bold';
        }
        return false;
    }
    return true;
}

function validateAttentionCheck2() {
    const selectedOption = document.querySelector('input[name="attn_check_2"]:checked');
    const errorSpan = document.getElementById('attn-error-message');

    if (!selectedOption) {
        if (errorSpan) {
            errorSpan.textContent = 'Please select an option';
            errorSpan.style.display = 'block';
            errorSpan.style.fontWeight = 'bold';
        }
        return false;
    }
    return true;
}

function ValidateQuiz2() {
    let isValid = true;
    const questions = [
        { id: 'fllw_up_Q1', errorId: 'errorQ1' },
        { id: 'fllw_up_Q2', errorId: 'errorQ2' },
        { id: 'fllw_up_Q3', errorId: 'errorQ3' }
    ];

    questions.forEach(function(question) {
        const input = document.getElementById(question.id);
        const errorSpan = document.getElementById(question.errorId);

        if (!input.value) {
            errorSpan.textContent = 'Answer Required';
            errorSpan.style.display = 'inline';
            errorSpan.style.fontWeight = 'bold';
            isValid = false;
        } else {
            errorSpan.style.display = 'none';
        }
    });
    return isValid;
}
function validateDemographics() {
    let isValid = true;
    const selected1 = document.querySelector('input[name="demographic_1"]:checked');
    const errorSpan1 = document.getElementById('errorQ1');
    
    if (!selected1) {
        errorSpan1.textContent = 'Answer Required';
        errorSpan1.style.display = 'inline';
        errorSpan1.style.fontWeight = 'bold';
        isValid = false;
    } else {
        errorSpan1.style.display = 'none';
    }

    const selected2 = document.querySelector('input[name="demographic_2"]:checked');
    const errorSpan2 = document.getElementById('errorQ2');

    if (!selected2) {
        errorSpan2.textContent = 'Answer Required';
        errorSpan2.style.display = 'inline';
        errorSpan2.style.fontWeight = 'bold';
        isValid = false;
    } else {
        errorSpan2.style.display = 'none';
    }
    return isValid;
}
// ==================================================
// Checks if Quiz Answers are Correct
// ==================================================
function Quiz1showErrorMessage(question) {
    var errorSpan = document.getElementById('error' + question);
    errorSpan.textContent = 'Incorrect';
    errorSpan.style.fontWeight = 'bold';
    errorSpan.style.display = 'inline';
}
function CheckQuiz1Answers() {
    var answers_quiz1 = {
        Q1: parseInt(document.querySelector('input[name="Q1"]').value.trim(), 10),
        Q2: parseInt(document.querySelector('input[name="Q2"]').value.trim(), 10),
        Q3: document.querySelector('select[name="Q3"]').value.trim() === "1",
    };

    var correct_answers_quiz1 = js_vars.correct_answers_quiz1;
    var correct = true;

    var errorSpans = document.querySelectorAll('[id^="errorQ"]');
    errorSpans.forEach(function (errorSpan) {
        errorSpan.textContent = '';
        errorSpan.style.display = 'none';
    });

    for (var key in answers_quiz1) {
        if (answers_quiz1[key] !== correct_answers_quiz1[key]) {
            Quiz1showErrorMessage(key);
            correct = false;
        }
    }

    liveSend({'submit_quiz': 'submit_quiz', 'answers_quiz1': answers_quiz1});

    if (correct) {
        document.forms[0].submit();
    }
}

// ==================================================
// Payoff Table Logic
// ==================================================
function createPayoffTable(value) {
    var constant = js_vars.constant;
    var auction_instructions = js_vars.auction_instructions
    var computer_instructions = js_vars.computer_instructions
    const validValues = (auction_instructions || computer_instructions)

    ? Array.from({ length: 11 }, (_, i) => i * 50)
    : Array.from({ length: 11 }, (_, i) => i);
    const payoffTable = {};

    validValues.forEach(bid1 => {
        validValues.forEach(bid2 => {
            let payoff;
            if (auction_instructions || computer_instructions) {
                if (bid1 > bid2) {
                    payoff = constant + (value - bid2);
                } else if (bid1 === bid2) {
                    payoff = constant + Math.floor((value - bid2) / 2);
                } else {
                    payoff = constant;
                }
            } else {
                if (bid1 > bid2) {
                    payoff = constant + (value - bid2) * 50;
                } else if (bid1 === bid2) {
                    payoff = constant + (value - bid2) * 25;
                } else {
                    payoff = constant;
                }
            }
            payoffTable[`${bid1},${bid2}`] = payoff;
        });
    });
    return payoffTable;
}
function updatePayoffTable() {
    const popupContainer = document.getElementById('instructions-bttn');
    const isPopup = popupContainer !== null && popupContainer.style.display === 'block';

    const tableContainer = isPopup
        ? document.getElementById('payoff-table-popup')
        : document.getElementById('payoff-table-container');   
    if (!tableContainer) return;

    let value;
    const valueDropdown = document.querySelector('.value-dropdown-btn');

    if (valueDropdown) {
        const selectedText = valueDropdown.innerText;
        const parts = selectedText.split(": ");
        const parsed = parts.length > 1 ? parseInt(parts[1], 10) : NaN;

        value = !isNaN(parsed)
            ? parsed
            : fallbackValue();
    } else {
        value = fallbackValue();
    }

    function fallbackValue() {
        if (isPopup) return js_vars.instruction_value;
        if (js_vars.auction_value == null && js_vars.quiz_value == null) {
            return js_vars.instruction_value;
        }
        return js_vars.auction_value ?? js_vars.quiz_value ?? js_vars.instruction_value;
    }

    var auction_instructions = js_vars.auction_instructions;
    var computer_instructions = js_vars.computer_instructions
    const validValues = (auction_instructions || computer_instructions)
    ? Array.from({ length: 11 }, (_, i) => i * 50)
    : Array.from({ length: 11 }, (_, i) => i);

    const payoffTable = createPayoffTable(value);
    let tableHTML = '<table>';

    let columnHeader, rowHeader;

    if (computer_instructions) {
        columnHeader = "Computer's Bid";
        rowHeader = "My Bid";
    } else if (auction_instructions) {
        columnHeader = "Other Participant's Bid";
        rowHeader = "My Bid";
    } else {
        columnHeader = "Other Participant's Number";
        rowHeader = "My Number";
    }

    tableHTML += `<tr><th></th><th colspan="${validValues.length + 1}">${columnHeader}</th></tr>`;
    tableHTML += `<tr><th rowspan="${validValues.length + 1}" class="vertical-header">${rowHeader}</th><th></th>`;
    validValues.forEach(bid => tableHTML += `<th>${bid}</th>`);
    tableHTML += '</tr>';

    validValues.forEach(bid1 => {
        tableHTML += `<tr><th>${bid1}</th>`;
        validValues.forEach(bid2 => {
            const payoff = payoffTable[`${bid1},${bid2}`];
            tableHTML += `<td>${payoff}</td>`;
        });
        tableHTML += '</tr>';
    });
    tableHTML += '</table>';
    tableContainer.innerHTML = tableHTML;
}
document.addEventListener('DOMContentLoaded', function () {
    updatePayoffTable();
});

// ==================================================
// Dropdown Logic For Bid & Payoff Table Value
// ==================================================
function toggleDropdown(button) {
    const content = button.nextElementSibling;
    if (content) {
        content.style.display = content.style.display === "none" ? "block" : "none";
        content.style.width = `${button.offsetWidth}px`;
    }
}
function selectValue(value, option) {
    var auction_instructions = js_vars.auction_instructions;
    const dropdown = option.closest('.value-dropdown');
    if (!dropdown) return;

    const button = dropdown.querySelector('button');
    if (!button) return;

    const label = button.classList.contains('PC-value-dropdown-btn')
        ? `Value for Payoff: ${value}`
        : (auction_instructions ? `Value for Payoff Table: ${value}` : `Type for Payoff Table: ${value}`);

    button.innerText = label;

    liveSend({'dropdown_value': value });

    toggleDropdown(button);
    updatePayoffTable();
    tryCalculatePayoff();
}
function selectYourBid(bid) {
    const button = document.querySelector('.your-bid-dropdown-btn');
    document.querySelector('.your-bid-dropdown-btn').innerText = `Your Bid: ${bid}`;
    toggleDropdown(button);
    tryCalculatePayoff();
}
function selectOpponentBid(bid) {
    const button = document.querySelector('.opponent-bid-dropdown-btn');
    document.querySelector('.opponent-bid-dropdown-btn').innerText = `Other's Bid: ${bid}`;
    toggleDropdown(button);
    tryCalculatePayoff();
}
function confirmBid(bid) {
    var auction_instructions = js_vars.auction_instructions;
    var computer_instructions = js_vars.computer_instructions;
    const button = document.querySelector('.bid-dropdown-btn');
    const label = (auction_instructions || computer_instructions) ? 'Select Your Bid' : 'Select Your Number';
    const confirmLabel = (auction_instructions || computer_instructions) ? 'Confirm Your Bid' : 'Confirm Your Number';
    
    button.innerText = `${label}: ${bid}`;
    document.getElementById('selected-bid-input').value = bid;

    document.getElementById('confirm-button').innerHTML = `${confirmLabel}: <span id="selected-bid-display">${bid}</span>`;
    document.getElementById('confirm-button').classList.add('green');

    toggleDropdown(button);
}
function showErrorPopup() {
    document.getElementById('error-popup').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
}
function closeErrorPopup() {
    document.getElementById('error-popup').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}
function validateBidSelection() {
    const bidInput = document.getElementById('selected-bid-input');
    if (!bidInput || !bidInput.value) {
        showErrorPopup();
        return false;
    }
    return true;
}

// ==================================================
// Close Dropdowns When Clicking Outside
// ==================================================
document.addEventListener('click', function(event) {
    const dropdowns = [
        { wrapper: '.value-dropdown', content: 'value-dropdown-content' },
        { wrapper: '.bid-dropdown', content: 'bid-dropdown-content' },
        { wrapper: '.PC-value-dropdown', content: 'PC-value-dropdown-content' },
        { wrapper: '.your-bid-dropdown', content: 'your-bid-dropdown-content' },
        { wrapper: '.opponent-bid-dropdown', content: 'opponent-bid-dropdown-content' }
    ];

    dropdowns.forEach(({ wrapper, content }) => {
        const container = document.querySelector(wrapper);
        const contentEl = document.getElementById(content);

        if (container && contentEl && !container.contains(event.target)) {
            contentEl.style.display = "none";
        }
    });
});

// ==================================================
// Instructions Button
// ==================================================
function showInstructions() {
    document.getElementById('instructions-bttn').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
    document.body.style.overflow = 'hidden';
    updatePayoffTable();
}
function closeInstructions() {
    document.getElementById('instructions-bttn').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// ==================================================
// Advances Page if 2 Incorrect Quiz Answers
// ==================================================
function liveRecv(data) {
    if (data.advance_page) {
        document.forms[0].submit();
    }
}

// ==================================================
// Calculate Function
// ==================================================
function calculatePayoff() {
    const valueDropdown = parseInt(document.getElementById("PC-value-dropdown-btn").innerText.split(":")[1].trim(), 10);
    const yourBidValue = parseInt(document.getElementById("your-bid-dropdown-btn").innerText.split(":")[1].trim(), 10);
    const opponentBidValue = parseInt(document.getElementById("opponent-bid-dropdown-btn").innerText.split(":")[1].trim(), 10);
    var constant = js_vars.constant;

    let payoff;
    if (yourBidValue > opponentBidValue) {
        payoff = constant + (valueDropdown - opponentBidValue);
    } else if (yourBidValue === opponentBidValue) {
        payoff = constant + (Math.floor((valueDropdown - opponentBidValue) / 2));
    } else {
        payoff = constant;
    }

    liveSend({'value_dropdown': valueDropdown, 'your_bid_value': yourBidValue, 'opponent_bid_value': opponentBidValue});

    document.getElementById("payoff-display").innerHTML = `Your Payoff: <span style="color: green">${payoff}</span>`;

    return false;
}
function tryCalculatePayoff() {
    const val1 = document.getElementById("PC-value-dropdown-btn").innerText.split(":")[1]?.trim();
    const val2 = document.getElementById("your-bid-dropdown-btn").innerText.split(":")[1]?.trim();
    const val3 = document.getElementById("opponent-bid-dropdown-btn").innerText.split(":")[1]?.trim();

    if (val1 && val2 && val3) {
        calculatePayoff();
    }
}