/**
 * Created by Lars Veldscholte on 13/07/2017.
 */

$(document).ready(function () {
	$('.bootstrap-tagsinput input').prop('disabled', true);

	$('#note_field_check').click(function() {
		$('#note_field').prop('disabled', !this.checked);
	});

	$('input:radio').change(function() {
		$(this).closest('.form-group').find("#id_note_field_options").tagsinput('removeAll');
		$(this).closest('.form-group').find("input:text").prop('disabled', true);

		if ($(this).is(":checked"))
			$(this).parent().parent().parent().next().find("input:text").prop('disabled', false);
	});
});
