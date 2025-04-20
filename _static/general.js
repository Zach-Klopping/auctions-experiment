// ==================================================
// Disable Copying on the Page
// ==================================================
document.addEventListener('copy', function(event) {
    event.preventDefault();
    document.getElementById('copy-popup').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
});

function closeCopyPopup() {
    document.getElementById('copy-popup').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
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
    const questions = [
        { id: 'fllw_up_Q1', errorId: 'errorQ1' },
        { id: 'fllw_up_Q2', errorId: 'errorQ2' },
        { id: 'fllw_up_Q3', errorId: 'errorQ3' }
    ];

    let isValid = true;

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
        Q1: document.querySelector('input[name="Q1"]').value.trim(),
        Q2: document.querySelector('input[name="Q2"]').value.trim(),
        Q3: document.querySelector('select[name="Q3"]').value.trim(),
    };

    var correct_answers_quiz1 = js_vars.correct_answers_quiz1;
    var correct = true;

    // Clear previous error messages
    var errorSpans = document.querySelectorAll('[id^="errorQ"]');
    errorSpans.forEach(function (errorSpan) {
        errorSpan.textContent = '';
        errorSpan.style.display = 'none';
    });

    // Check answers
    for (var key in answers_quiz1) {
        if (answers_quiz1[key] !== correct_answers_quiz1[key]) {
            Quiz1showErrorMessage(key);
            correct = false;
        }
    }

    liveSend({'action': 'submit_quiz', 'answers_quiz1': answers_quiz1});

    if (correct) {
        document.forms[0].submit();
    }
}

// ==================================================
// Payoff Table Logic
// ==================================================
function createPayoffTable(value) {
    var constant = js_vars.constant;
    const validValues = Array.from({length: 11}, (_, i) => i * 50);

    if (!validValues.includes(value)) {
        throw new Error(`Value must be one of the following: ${validValues.join(", ")}`);
    }

    const payoffTable = {};

    validValues.forEach(bid1 => {
        validValues.forEach(bid2 => {
            let payoff;
            if (bid1 > bid2) {
                payoff = constant + (value - bid2);
            } else if (bid1 === bid2) {
                payoff = constant + Math.floor((value - bid2) / 2);
            } else {
                payoff = 0;
            }
            payoffTable[`${bid1},${bid2}`] = payoff;
        });
    });
    return payoffTable;
}

function updatePayoffTable() {
    const tableContainer = document.getElementById('payoff-table-container');
    if (!tableContainer) return;

    let value;
    const dropdown = document.querySelector('.dropdown-btn');
    if (dropdown) {
        const selectedText = dropdown.innerText;
        const parsed = parseInt(selectedText.split(": ")[1]);
        value = isNaN(parsed) ? js_vars.auction_value : parsed;
    } else {
        value = js_vars.auction_value;
    }

    const validValues = Array.from({length: 11}, (_, i) => i * 50);
    if (!validValues.includes(value)) {
        alert("Please enter a valid value (0, 50, 100, ..., 500)");
        return;
    }

    const payoffTable = createPayoffTable(value);
    let tableHTML = '<table>';
    tableHTML += `<tr><th></th><th colspan="${validValues.length + 1}">Other Participant's Bid</th></tr>`;
    tableHTML += `<tr><th rowspan="${validValues.length + 1}" style="writing-mode: vertical-rl; transform: rotate(180deg); text-align: center;">My Bid</th><th></th>`;
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
function toggleDropdown() {
    const content = document.getElementById("dropdown-content");
    content.style.display = content.style.display === "none" ? "block" : "none";
}

function selectValue(value) {
    document.querySelector('.dropdown-btn').innerText = `Payoff Table: ${value}`;
    toggleDropdown();
    updatePayoffTable();
}

function toggleBidDropdown() {
    const content = document.getElementById("bid-dropdown-content");
    content.style.display = content.style.display === "none" ? "block" : "none";
}

function selectBid(value) {
    document.querySelector('.bid-dropdown-btn').innerText = `Selected Bid: ${value}`;
    document.getElementById('selected-bid-input').value = value;
    document.getElementById('selected-bid-display').innerText = value;
    document.getElementById('continue-button').classList.add('green');
    toggleBidDropdown();
}

function validateBidSelection() {
    const bidInput = document.getElementById('selected-bid-input');
    const errorSpan = document.getElementById('bid-error-message');

    if (!bidInput || !bidInput.value) {
        if (errorSpan) {
            errorSpan.textContent = 'Please Select a Bid';
            errorSpan.style.display = 'block';
            errorSpan.style.fontWeight = 'bold';
        }
        return false;
    }
    return true;
}

// ==================================================
// Close Dropdowns When Clicking Outside
// ==================================================
document.addEventListener('click', function(event) {
    const dropdown = document.querySelector('.dropdown');
    const bidDropdown = document.querySelector('.bid-dropdown');

    if (dropdown && !dropdown.contains(event.target)) {
        document.getElementById("dropdown-content").style.display = "none";
    }

    if (bidDropdown && !bidDropdown.contains(event.target)) {
        document.getElementById("bid-dropdown-content").style.display = "none";
    }
});

// ==================================================
// Instructions Button
// ==================================================
function showInstructions() {
    document.getElementById('instructions-bttn').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeInstructions() {
    document.getElementById('instructions-bttn').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// ==================================================
// Advances Page if 3 Incorrect Quiz Answers
// ==================================================
function liveRecv(data) {
    if (data.advance_page) {
        document.forms[0].submit();
    }
}