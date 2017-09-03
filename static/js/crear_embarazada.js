$(document).ready(load)

function load(){
    $( "[href='/admin/agregar_embarazada/']" ).parent().addClass('active').parent().addClass('open');
    $( "[href='/admin/agregar_embarazada/']" ).parent().parent().parent().addClass('active open hsub');
    
    $("#cmb_escolaridad").on("change", function(e){
        console.log($(this).val())
        if($(this).val() == "primaria"){
            $("#div-cmb-primaria").removeClass("hide")
            $("#div-cmb-secundaria").addClass("hide")
            $("#div-valor-tecnico").addClass("hide")
            $("#div-valor-universidad").addClass("hide")
            $("#div-valor-otro-escolaridad").addClass("hide")
            
        }
        if($(this).val() == "secundaria"){
            $("#div-cmb-primaria").addClass("hide")
            $("#div-cmb-secundaria").removeClass("hide")
            $("#div-valor-tecnico").addClass("hide")
            $("#div-valor-universidad").addClass("hide")
            $("#div-valor-otro-escolaridad").addClass("hide")
            
        }
        if($(this).val() == "tecnico"){
            $("#div-cmb-primaria").addClass("hide")
            $("#div-cmb-secundaria").addClass("hide")
            $("#div-valor-tecnico").removeClass("hide")
            $("#div-valor-universidad").addClass("hide")
            $("#div-valor-otro-escolaridad").addClass("hide")
            
        }
        
        if($(this).val() == "universidad"){
            $("#div-cmb-primaria").addClass("hide")
            $("#div-cmb-secundaria").addClass("hide")
            $("#div-valor-tecnico").addClass("hide")
            $("#div-valor-universidad").removeClass("hide")
            $("#div-valor-otro-escolaridad").addClass("hide")
            
        }
        if($(this).val() == "otro"){
            $("#div-cmb-primaria").addClass("hide")
            $("#div-cmb-secundaria").addClass("hide")
            $("#div-valor-tecnico").addClass("hide")
            $("#div-valor-universidad").addClass("hide")
            $("#div-valor-otro-escolaridad").removeClass("hide")
            
        }
    })
    
    $(document).on('submit', "form[name='form-nueva-embarazada']", function(){
        if(validar_campos()==0){
            var formData = new FormData( $( "form[name='form-nueva-embarazada']" )[0] );
            var escolaridad = $("#cmb_escolaridad").val();
            var valor_escolaridad = obtener_valor_escolaridad(escolaridad)
            formData.append("escolaridad", escolaridad);
            formData.append("valor_escolaridad", valor_escolaridad)
            
            $.ajax({
                url : '/admin/insert_pregnant/',
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
                        $( "form[name='form-nueva-embarazada']" )[0].reset()
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

function obtener_valor_escolaridad(escolaridad){
    if(escolaridad == "primaria"){
        return $("#cmb_primaria").val()
    }
    if(escolaridad == "secundaria"){
        return $("#cmb_secundaria").val()
        
    }
    if(escolaridad == "tecnico"){
        return $("#valor_tecnico").val()
        
    }
    
    if(escolaridad == "universidad"){
        return $("#valor_universidad").val()
        
    }
    if(escolaridad == "otro"){
        return $("#valor_otro_escolaridad").val()
    }
}

function validar_campos(){
    let cont = 0;
    if($("#region").val() == "" ){
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
    if($("#semana_embarazo").val() == "" ){
        cont++
    }
    if($("#edad").val() == "" ){
        cont++
    }
    if($("#etnia").val() == "" ){
        cont++
    }
    return cont
    
}