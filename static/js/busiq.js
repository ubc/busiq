/**
 * Created by compass on 15-04-17.
 */
$(function() {
    // prevent user to type in random email
    //$("#id_email").attr('readonly', true);
    //$("#id_verify_email").attr('readonly', true);
    // hook up autocomplete for first and last name field
    $("#id_first_name, #id_last_name, #id_email").autocomplete({
        source: function(request, response) {
            var self = this;
            var first_name = $('#id_first_name').val();
            var last_name = $('#id_last_name').val();
            var email = $('#id_email').val();
            var data = {
                first_name: first_name,
                last_name: last_name,
                email: email
            };
            //data[field_name] = request.term;
            $.ajax({
                url: window.location.protocol + "//busiq.ctlt.ubc.ca/staff",
                dataType: "jsonp",
                data: data,
                success: function(data) {
                    console.log(data);
                    response($.map(data.staff, function(val) {
                        return {
                            'label': val.first_name + " " + val.last_name + " (" + val.email + ")",
                            'value': val
                        };
                    }));
                }
            });
        },
        minLength: 2,
        select: function(event, ui) {
            // populate fields when selected
            for (var id in ui.item.value) {
                $('#id_' + id).val(ui.item.value[id]);
            }
            // this is for department head sign off invite form
            if ($('#id_verify_email').length) {
                $('#id_verify_email').val(ui.item.value['email']);
            }
            return false;
        },
        open: function() {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function() {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });
});
