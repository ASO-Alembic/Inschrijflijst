/**
 * Created by Lars Veldscholte on 02/03/2017.
 */

// Snippet for disabling submit button if form is unchanged
$('form')
	.each(function () {
		$(this).data('serialized', $(this).serialize())
	})
	.on('change input', function () {
		$(this)
			.find('button:submit')
			.attr('disabled', $(this).serialize() == $(this).data('serialized'));
	})
	.find('button:submit')
	.attr('disabled', true);
