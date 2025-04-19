// Disable Copying
document.addEventListener('copy', function(event) {
    event.preventDefault();
    alert("Copying is disabled on this page.");
});

function validateAttentionCheck1() {
    const selectedOption = document.querySelector('input[name="attn_check_1"]:checked');  // Find the selected radio button
    const errorSpan = document.getElementById('attn-error-message');
    
    if (!selectedOption) {
        if (errorSpan) {
            errorSpan.textContent = 'Please select an option';
            errorSpan.style.display = 'block';
            errorSpan.style.fontWeight = 'bold';
        }
        return false;  // Stop further action
    }
    return true;  // Allow form submission
}

function validateAttentionCheck2() {
    const selectedOption = document.querySelector('input[name="attn_check_2"]:checked');  // Find the selected radio button
    const errorSpan = document.getElementById('attn-error-message');
    
    if (!selectedOption) {
        if (errorSpan) {
            errorSpan.textContent = 'Please select an option';
            errorSpan.style.display = 'block';
            errorSpan.style.fontWeight = 'bold';
        }
        return false;  // Stop further action
    }
    return true;  // Allow form submission
}

// Showing error message
function Quiz1showErrorMessage(question) {
    var errorSpan = document.getElementById('error' + question);
    errorSpan.textContent = 'Incorrect';
    errorSpan.style.fontWeight = 'bold';
    errorSpan.style.display = 'inline';
}

// Create payoff table based on the selected value
function createPayoffTable(value) {
    var constant = js_vars.constant;
    
    // Define the valid values (multiples of 50 from 0 to 500)
    const validValues = Array.from({length: 11}, (_, i) => i * 50);  // [0, 50, 100, ..., 500]
    
    // Ensure the provided value is valid
    if (!validValues.includes(value)) {
        throw new Error(`Value must be one of the following: ${validValues.join(", ")}`);
    }
    
    // Initialize the payoff table object
    const payoffTable = {};
    
    // Generate the payoff values for each combination of bids
    validValues.forEach(bid1 => {
        validValues.forEach(bid2 => {
            let payoff;
            if (bid1 > bid2) {
                payoff = constant + (value - bid2);  // Winner's payoff
            } else if (bid1 === bid2) {
                payoff = constant + Math.floor((value - bid2) / 2);  // Average payoff if bids are equal
            } else {
                payoff = 0;  // Loser's payoff
            }
            // Store the payoff in the table using a string key for easier lookup
            payoffTable[`${bid1},${bid2}`] = payoff;
        });
    });

    return payoffTable;
}

// Function to update the payoff table displayed on the webpage
function updatePayoffTable() {
    const tableContainer = document.getElementById('payoff-table-container');
    if (!tableContainer) return; // Exit if there's no container
    
    // Get the selected value from the input field (or default to 0 if invalid)
    let value;
    const dropdown = document.querySelector('.dropdown-btn');
    if (dropdown) {
        const selectedText = dropdown.innerText;
        const parsed = parseInt(selectedText.split(": ")[1]);
        value = isNaN(parsed) ? js_vars.auction_value : parsed;
    } else {
        value = js_vars.auction_value;
    }
    // Define the valid values (multiples of 50 from 0 to 500)
    const validValues = Array.from({length: 11}, (_, i) => i * 50);
    
    // Check if the entered value is valid
    if (!validValues.includes(value)) {
        alert("Please enter a valid value (0, 50, 100, ..., 500)");
        return;
    }
    
    // Generate the payoff table based on the selected value
    const payoffTable = createPayoffTable(value);
    let tableHTML = '<table>';
    tableHTML += `<tr><th></th><th colspan="${validValues.length+1}">Other Participant's Bid</th></tr>`;
    tableHTML += `<tr><th rowspan="${validValues.length + 1}" style="writing-mode: vertical-rl; transform: rotate(180deg); text-align: center;">My Bid</th>`;
    
    // Inline styles for the header
    tableHTML += `<th></th>`;
    validValues.forEach(bid => tableHTML += `<th>${bid}</th>`);
    tableHTML += '</tr>';
    
    // Create rows for each combination of bids and their corresponding payoffs
    validValues.forEach(bid1 => {
        tableHTML += `<tr><th>${bid1}</th>`;
        validValues.forEach(bid2 => {
            const payoff = payoffTable[`${bid1},${bid2}`];
            tableHTML += `<td>${payoff}</td>`;
        });
        tableHTML += '</tr>';
    });
    
    tableHTML += '</table>';
    // Insert the generated table into the webpage
    document.getElementById('payoff-table-container').innerHTML = tableHTML;
}

// Toggle the dropdown visibility
function toggleDropdown() {
    const content = document.getElementById("dropdown-content");
    content.style.display = content.style.display === "none" ? "block" : "none";
}

// Handle selection of a value from the dropdown
function selectValue(value) {
    document.querySelector('.dropdown-btn').innerText = `Payoff Table: ${value}`;
    toggleDropdown();  // Hide the dropdown after selecting a value
    updatePayoffTable();  // Automatically update the payoff table after selection
}
 
// Bid-specific dropdown functions
function toggleBidDropdown() {
    const content = document.getElementById("bid-dropdown-content");
    content.style.display = content.style.display === "none" ? "block" : "none";
}

// Handle selection of a bid from the dropdown
function selectBid(value) {
    document.querySelector('.bid-dropdown-btn').innerText = `Selected Bid: ${value}`;
    document.getElementById('selected-bid-input').value = value;  // <-- Add this line
    toggleBidDropdown();  // Hide the bid dropdown after selection
}

function ValidateQuiz2() {
    const questions = [
        { id: 'fllw_up_Q1', errorId: 'errorQ1' },
        { id: 'fllw_up_Q2', errorId: 'errorQ2' },
        { id: 'fllw_up_Q3', errorId: 'errorQ3' }
    ];

    let isValid = true;

    // Loop through each question and check if it has been answered
    questions.forEach(function(question) {
        const input = document.getElementById(question.id);
        const errorSpan = document.getElementById(question.errorId);

        if (!input.value) {
            errorSpan.textContent = 'Answer required.';
            errorSpan.style.display = 'inline';
            isValid = false;
        } else {
            errorSpan.style.display = 'none';
        }
    });

    return isValid;  // Return false if any question is unanswered
}

// Close dropdown if clicked outside of it
document.addEventListener('click', function(event) {
    const dropdown = document.querySelector('.dropdown');
    const bidDropdown = document.querySelector('.bid-dropdown');

    // Close the general dropdown if clicked outside
    if (dropdown && !dropdown.contains(event.target)) {
        document.getElementById("dropdown-content").style.display = "none";
    }

    // Close the bid dropdown if clicked outside
    if (bidDropdown && !bidDropdown.contains(event.target)) {
        document.getElementById("bid-dropdown-content").style.display = "none";
    }
});

// Add event listener for the "Update Table" button
document.addEventListener('DOMContentLoaded', function () {
    // Call updatePayoffTable on page load
    updatePayoffTable();
});

// Function that showes the Instructions popup
function showInstructions() {
    document.getElementById('instructions-bttn').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
    document.body.style.overflow = 'hidden'; // Disable background scroll
}

// Function that closes the Instructions popup
function closeInstructions() {
    // Close the popup and hide the overlay
    document.getElementById('instructions-bttn').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
    document.body.style.overflow = 'auto'; // Re-enable background scroll
}

// Define liveRecv to handle the server response
function liveRecv(data) {
    if (data.advance_page) {
        document.forms[0].submit();  // Submit the form to advance the page
    }
}

// Showing error message
function Quiz1showErrorMessage(question) {
    var errorSpan = document.getElementById('error' + question);
    errorSpan.textContent = 'Incorrect';
    errorSpan.style.fontWeight = 'bold';
    errorSpan.style.display = 'inline';
}

/// Stage 1 instructions quiz answer validation
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

    // Check if all answers are correct
    for (var key in answers_quiz1) {
      if (answers_quiz1[key] !== correct_answers_quiz1[key]) {
        Quiz1showErrorMessage(key);
        correct = false;
      }
    }

    liveSend({'action': 'submit_quiz', 'answers_quiz1': answers_quiz1});

    if (correct) {
      // Submit the form
      document.forms[0].submit();
    }
}