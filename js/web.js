jQuery(document).ready(function() {

	$(".openedit").fancybox({
		'width'			: '30%',
		'height'		: '47%',
	        'autoScale'     	: false,
        	'transitionIn'		: 'none',
		'transitionOut'		: 'none',
		'type'			: 'iframe',
		onClosed	:	function() {
			            		window.location.reload();
	    				}

	});

	$(".opendel").fancybox({
		'width'			: '30%',
		'height'		: '19%',
	        'autoScale'     	: false,
        	'transitionIn'		: 'none',
		'transitionOut'		: 'none',
		'type'			: 'iframe',
		onClosed	:	function() {
			            		window.location.reload();
	    				}

	});

	$(".openlink").fancybox({
		'width'			: '80%',
		'height'		: '80%',
	        'autoScale'     	: false,
        	'transitionIn'		: 'none',
		'transitionOut'		: 'none',
		'type'			: 'iframe'
	});

});
