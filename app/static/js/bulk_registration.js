/**
 * Created by Lars Veldscholte on 02/03/2017.
 */

$(document).ready(function () {
	$('#chairedCommittees').on('change', function () {
		var committeeName = $('#chairedCommittees').val();
		if (committeeName != "") {
			$('.members').hide();
			$('.members#' + committeeName).show();
			$('#CommitteeInput').attr('value', committeeName);
			$('#myModal').modal();
		}

		$('#chairedCommittees').prop('selectedIndex', 0);
	});
});
