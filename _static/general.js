function createPayoffTable(value) {
    // Function to create the payoff table based on the selected value
    // Define the valid values (multiples of 40 from 0 to 400)
    const validValues = Array.from({length: 11}, (_, i) => i * 40);  // [0, 40, 80, ..., 400]
    
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
    const value = parseInt(document.getElementById('value-input').value) || 0;
    
    // Define the valid values (multiples of 40 from 0 to 400)
    const validValues = Array.from({length: 11}, (_, i) => i * 40);
    
    // Check if the entered value is valid
    if (!validValues.includes(value)) {
        alert("Please enter a valid value (0, 40, 80, ..., 400)");
        return;
    }
    
    // Generate the payoff table based on the selected value
    const payoffTable = createPayoffTable(value);
    let tableHTML = '<table>';
    
    // Create the header row with the valid bid values
    tableHTML += '<tr><th></th>';
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

document.addEventListener('DOMContentLoaded', function () {
    // Add event listener for the "Update Table" button
    document.getElementById('update-button').addEventListener('click', function() {
        updatePayoffTable();  // Call the function when the button is clicked
    });

    // Call updatePayoffTable on page load (if needed)
    updatePayoffTable();
});

// Disable Copying
document.addEventListener('copy', function(event) {
    event.preventDefault();
    alert("Copying is disabled on this page.");
});

