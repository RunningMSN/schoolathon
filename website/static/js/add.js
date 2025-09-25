var rowCounter = 0;

function addRow() {
	rowCounter++;

	// Create wrapper div
	let row = document.createElement("div");
	row.className = "row mb-2";

	row.innerHTML = `
		<input type="hidden" id="advisorRow-${rowCounter}" name="advisorRow-${rowCounter}"/>
		<div class="col">
			<input type="text" class="form-control" placeholder="Advisor/Office Name" id="name-${rowCounter}" name="name-${rowCounter}" />
		</div>
		<div class="col">
			<input type="text" class="form-control" placeholder="Email" id="email-${rowCounter}" name="email-${rowCounter}" />
		</div>
		<div class="col">
			<select class="form-control" id="advisorType-${rowCounter}" name="advisorType-${rowCounter}">
				<option value="" disabled selected hidden>Select a Category</option>
				<option>Pre-health Advisor</option>
				<option>Biology Teacher</option>
				<option>General Career Advisor</option>
				<option>Other</option>
			</select>
		</div>
		<div class="col-1 d-flex align-items-center justify-content-center">
			<!-- Optional: Add a delete button here -->
		</div>
	`;

	document.getElementById("advisorForm").appendChild(row);
}
