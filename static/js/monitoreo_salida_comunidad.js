$(document).ready(load)

function load(){
    $(document).on('submit', "form[name='form-nuevo-monitoreo']", function(){
        
        if(validar_campos() == 0){
            var res_radio_1 = $(".radio_1:checked").val();
            console.log(res_radio_1)
            
            var formData = new FormData( $( "form[name='form-nuevo-monitoreo']" )[0] );
            console.log(formData)
            formData.append("res_radio_1", res_radio_1)
            $.ajax({
                url : '/admin/embarazada_comunidad/',
                type : 'post',
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
    return 0
}