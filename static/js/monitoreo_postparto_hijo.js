$(document).ready(load)

function load(){
    $(document).on('submit', "form[name='form-nuevo-monitoreo']", function(event){
        if(validar_campos() == 0){
            var res_radio_1 = $(".radio_1:checked").val();
            var res_radio_2 = $(".radio_2:checked").val();
            var res_radio_3 = $(".radio_3:checked").val();
            var res_radio_4 = $(".radio_4:checked").val();
            var res_radio_5 = $(".radio_5:checked").val();
            var res_radio_6 = $(".radio_6:checked").val();
            var res_radio_7 = $(".radio_7:checked").val();
            var res_radio_8 = $(".radio_8:checked").val();
            var res_radio_9 = $(".radio_9:checked").val();
           
            
            var formData = new FormData( $( "form[name='form-nuevo-monitoreo']" )[0] );
            formData.append("res_radio_1", res_radio_1)
            formData.append("res_radio_2", res_radio_2)
            formData.append("res_radio_3", res_radio_3)
            formData.append("res_radio_4", res_radio_4)
            formData.append("res_radio_5", res_radio_5)
            formData.append("res_radio_6", res_radio_6)
            formData.append("res_radio_7", res_radio_7)
            formData.append("res_radio_8", res_radio_8)
            formData.append("res_radio_9", res_radio_9)
            
            $.ajax({
                url : '/admin/embarazada_postparto_hijo/',
                type : 'POST',
                data : formData,
                async : true,
                contentType: false,
                processData: false,
                success: function(data) {                    
                    console.log(data)
                    if(data.status){
                        $.gritter.add({
                            // (string | mandatory) the heading of the notification
                            title: 'Excelente!',
                            // (string | mandatory) the text inside the notification
                            text: data.mensaje,
                            class_name: 'gritter-success' 
                        });
                        $( "form[name='form-nuevo-monitoreo']" )[0].reset()
                    }else{
                        $.gritter.add({
                            // (string | mandatory) the heading of the notification
                            title: 'Urgente!',
                            // (string | mandatory) the text inside the notification
                            text: data.mensaje,
                            class_name: 'gritter-error' 
                        });
                        $( "form[name='form-nuevo-monitoreo']" )[0].reset()
                    }
                    
                },
                error: function (XMLHttpRequest, estado, errorS) {
                var error = eval("(" + XMLHttpRequest.responseText + ")");
                console.log(error.Message);
                console.log(estado);
                console.log(errorS);
                },
                complete: function (jqXHR, estado) {
                }
            });
        }else{
            $.gritter.add({
                // (string | mandatory) the heading of the notification
                title: 'Error!',
                // (string | mandatory) the text inside the notification
                text: "Campos Incompletos",
                class_name: 'gritter-error' 
            });
        }
        
        return false;
    })
}

function validar_campos(){
    var radio_length = ($('input[type=radio]:checked').size());
    
    if(radio_length == 9)
    {
        return 0
    }
    else{
        return 1
    }
}