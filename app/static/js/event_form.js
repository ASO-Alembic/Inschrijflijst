/**
 * Created by Lars Veldscholte on 13/07/2017.
 */

$(document).ready(function () {
	$('#note_field_check').click(setNoteFieldsetState);
	if($('.bootstrap-tagsinput input').val() == '')
		$('.bootstrap-tagsinput input').prop('disabled', true);

	$('input:radio').change(function() {
		$(this).closest('.form-group').find("#id_note_field_options").tagsinput('removeAll');
		$(this).closest('.form-group').find("input:text").prop('disabled', true);

		if ($(this).is(":checked"))
			$(this).parent().parent().parent().next().find("input:text").prop('disabled', false);
	});
});

function setNoteFieldsetState() {
	$('#note_fieldset').prop('disabled', !$('#note_field_check').is(':checked'));
}
