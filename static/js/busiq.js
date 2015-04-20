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
            var field_name = this.element.attr('name');
            var data = {};
            data[field_name] = request.term;
            $.ajax({
                url: "http://localhost:5000/staff",
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
