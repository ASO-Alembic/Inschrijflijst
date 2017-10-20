/**
 * Created by Lars Veldscholte on 13/07/2017.
 */

$(document).ready(function () {
	$('#note_field_check').click(setNoteFieldsetState);

	// Initial check at load for fieldset
	setNoteFieldsetState();

	// Set readonly state of tagsinput according to wether its empty or not (for filled form)
	if($('#id_note_field_options').val() == '')
		$('.bootstrap-tagsinput input').prop('readonly', true);

	// Disable and clear tagsinput on radio change
	$('input:radio').change(function() {
		$("#id_note_field_options").tagsinput('removeAll');
		$('.bootstrap-tagsinput input').prop('readonly', true);

		if ($(this).is(":checked"))
			$(this).parent().parent().parent().next().find("input:text").prop('readonly', false);
	});
});

// Set readonly state of fieldset according to checked state of checkbox
function setNoteFieldsetState() {
	var checked = $('#note_field_check').is(':checked');

	$('#note_fieldset input').prop('readonly', !checked);
	$('#note_fieldset input:checkbox, #note_fieldset input:radio').prop('disabled', !checked);

	if(!checked)
		$('#id_note_field').val('')
}
