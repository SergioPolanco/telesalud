$(document).ready(load)

function load(){
    $( "[href='/admin/agregar_brigadista/']" ).parent().addClass('active').parent().addClass('open');
    $( "[href='/admin/agregar_brigadista/']" ).parent().parent().parent().addClass('active open hsub');
    $(document).on('submit', "form[name='form-nuevo-brigadista']", function(){
        
        if(validar_campos() == 0){
            var formData = new FormData( $( "form[name='form-nuevo-brigadista']" )[0] );
            $.ajax({
                url : '/admin/insert_brigadist/',
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
                        $( "form[name='form-nuevo-brigadista']" )[0].reset()
                    }else{
                        $.gritter.add({
                            // (string | mandatory) the heading of the notification
                            title: 'Error!',
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
    let cont = 0;
    if($("#region").val() == "" ){
        cont++
    }

    if($("#sector").val() == "" ){
        cont++
    }

    if($("#escolaridad").val() == "" ){
        cont++
    }

    if($("#ocupacion").val() == "" ){
        cont++
    }

    if($("#funcion_sistema_salud").val() == "" ){
        cont++
    }

    if($("#anios_sistema_salud").val() == "" ){
        cont++
    }

    if($("#celular_asignado").val() == "" ){
        cont++
    }

    if($("#celular_personal").val() == "" ){
        cont++
    }

    if($("#municipio").val() == "" ){
        cont++
    }

    if($("#centro_salud").val() == "" ){
        cont++
    }
    if($("#comunidad").val() == "" ){
        cont++
    }
    if($("#nombres").val() == "" ){
        cont++
    }
    if($("#apellidos").val() == "" ){
        cont++
    }
    if($("#cedula").val() == "" ){
        cont++
    }
    if($("#sexo").val() == "" ){
        cont++
    }
    if($("#fecha_nacimiento").val() == "" ){
        cont++
    }
    if($("#etnia").val() == "" ){
        cont++
    }
    return cont
    
}