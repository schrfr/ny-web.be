/* menu-sort.js */

jQuery(function($) {
    // $('div.inline-group').sortable({
    //     /*containment: 'parent',
    //     zindex: 10, */
    //     items: 'div.inline-related',
    //     handle: 'h3:first',
    //     update: function() {
    //         $(this).find('div.inline-related').each(function(i) {
    //             if ($(this).find('input[id$=name]').val()) {
    //                 $(this).find('input[id$=order]').val(i+1);
    //             }
    //         });
    //     }
    // });
    // $('div.inline-related h3').css('cursor', 'move');
    // $('div.inline-related').find('input[id$=order]').parent('div').hide();
        
    // CASE Hard Copy Print Issue OR Library Text
    if ($('body').hasClass('hardcopies-printissue') || $('body').hasClass('library-text') ) {
        $('div.inline-group').sortable({
            items: 'div.inline-related',
            handle: 'h3:first',
            update: function() {
                $(this).find('div.inline-related').each(function(i) {
                    if ($(this).find('select option:selected').attr('value') != '') {
                        $(this).find('input[id$=order]').val(i+1);
                    }
                });
            }
        });
        $('div.inline-related h3').css('cursor', 'move');
        $('div.inline-related').find('input[id$=order]').parent('div').hide();        
    };
    
});
