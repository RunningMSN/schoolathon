var rowCounter = 0;

function addRow() {
	rowCounter++;

	var form = document.getElementById("advisorForm");
	form.innerHTML += `
	<div class="row" style="margin-bottom: 10px">
		<div class="col">
			<input type="text" class="form-control" placeholder="Advisor/Office Name" id="name-${rowCounter}" />
		</div>
		<div class="col">
			<input type="text" class="form-control" placeholder="Email" id="email-${rowCounter}" />
		</div>
		<div class="col">
			<select class="form-control" id="advisorType-${rowCounter}">
				<option value="" disabled selected hidden>Select a Category</option>
				<option>Pre-health Advisor</option>
				<option>Biology Teacher</option>
				<option>General Career Advisor</option>
				<option>Other (Please Specify)</option>
			</select>
		</div>
		<div class="col-1 d-flex align-items-center justify-content-center">
		
		</div>
	</div>
	`
}	