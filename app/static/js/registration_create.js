/**
 * Created by Lars Veldscholte on 01/03/2017.
 */

$(document).ready(function() {
	$('#addRow').click(function () {
		// Clone the first row
		var row = $('tbody tr')
			.first()
			.clone();

		// Reset all inputs
		row.find('input:text').val('');

		row
			.hide()
			.fadeIn('normal')
			.appendTo('tbody');

		$('.date').datetimepicker({
			format: 'YYYY-MM-DD'
		});
	});

	// Remove rows
	$('form').on('click', '.close', function () {
		// Don't remove last row
		if($('tbody tr').length > 1) {
			$(this)
				.closest('tr')
				.fadeOut("normal", function () {
					$(this).remove();
				})
		}
	});
});
