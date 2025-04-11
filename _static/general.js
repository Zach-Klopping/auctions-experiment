// Disable Copying
document.addEventListener('copy', function(event) {
    event.preventDefault();
    alert("Copying is disabled on this page.");
});

// Create payoff table based on the selected value
function createPayoffTable(value) {
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
                payoff = value - bid2;  // Winner's payoff
            } else if (bid1 === bid2) {
                payoff = Math.floor((value - bid2) / 2);  // Average payoff if bids are equal
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
    // Get the selected value from the input field (or default to 0 if invalid)
    const value = parseInt(document.querySelector('.dropdown-btn').innerText.split(": ")[1]) || 0;

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
    document.querySelector('.dropdown-btn').innerText = `Selected: ${value}`;
    toggleDropdown();  // Hide the dropdown after selecting a value
    updatePayoffTable();  // Automatically update the payoff table after selection
}

// Close dropdown if clicked outside of it
document.addEventListener('click', function(event) {
    const dropdown = document.querySelector('.dropdown');
    if (!dropdown.contains(event.target)) {
        document.getElementById("dropdown-content").style.display = "none";
    }
});

// Add event listener for the "Update Table" button
document.addEventListener('DOMContentLoaded', function () {
    // Call updatePayoffTable on page load
    updatePayoffTable();
});

function showInstructions() {
    document.getElementById('instructions-bttn').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
    document.body.style.overflow = 'hidden'; // Disable background scroll
}

// Function that closes the Explainer popup
function closeInstructions() {
    // Close the popup and hide the overlay
    document.getElementById('instructions-bttn').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
    document.body.style.overflow = 'auto'; // Re-enable background scroll
}