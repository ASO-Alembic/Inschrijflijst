/**
 * Created by Lars Veldscholte on 13/07/2017.
 */

$(document).ready(function () {
	// Initial check at load for fieldset
	$('#note_field_check').click(setNoteFieldsetState);

	// Set disabled state of tagsinput according to wether its empty or not
	if($('#id_note_field_options').val() == '')
		$('.bootstrap-tagsinput input').prop('disabled', true);

	// Disable and clear tagsinput on radio change
	$('input:radio').change(function() {
		$(this).closest('.form-group').find("#id_note_field_options").tagsinput('removeAll');
		$(this).closest('.form-group').find("input:text").prop('disabled', true);

		if ($(this).is(":checked"))
			$(this).parent().parent().parent().next().find("input:text").prop('disabled', false);
	});
});

// Set disabled state of fieldset according to checked state of checkbox
function setNoteFieldsetState() {
	$('#note_fieldset').prop('disabled', !$('#note_field_check').is(':checked'));

	if(!$('#note_field_check').is(':checked'))
		$('#id_note_field').val('')
}
