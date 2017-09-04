$(document).ready(load)

var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

function load(){
    $( "[href='/admin/modificar_brigadista/']" ).parent().addClass('active').parent().addClass('open');
    $( "[href='/admin/modificar_brigadista/']" ).parent().parent().parent().addClass('active open hsub');
    $("#simple_table").each(function(){
        var currentPage = 0;
        var numPerPage = 10;
        var $table = $(this);
        $table.bind('repaginate', function() {
            $table.find('tbody tr.main-row').hide().slice(currentPage * numPerPage, (currentPage + 1) * numPerPage).show();
        });
        $table.trigger('repaginate');
        var numRows = $table.find('tbody tr').length / 2;
        var numPages = Math.ceil(numRows / numPerPage);
        var $pager = $('<div class="pager"></div>');
        for (var page = 0; page < numPages; page++) {
            $('<span class="page-number"></span>').text(page + 1).bind('click', {
                newPage: page
            }, function(event) {
                currentPage = event.data['newPage'];
                $table.trigger('repaginate');
                $(this).addClass('active').siblings().removeClass('active');
            }).appendTo($pager).addClass('clickable');
        }
        $pager.insertBefore($table).find('span.page-number:first').addClass('active');
    });

    var cities = ["Alaska", "Canada", "Nicaragua"];
    $('.show-details-btn').on('click', function(e) {
        e.preventDefault();
        $(this).closest('tr').next().toggleClass('open');
        $(this).find(ace.vars['.icon']).toggleClass('fa-angle-double-down').toggleClass('fa-angle-double-up');
    });

    $('.nombres').editable({
        
        type: 'text',
        name: 'nombres',	
        success: function(res, new_value){
            actualizar_brigadista("nombre", new_value, $(this).attr("b_id"))
        }
    });

    $('.apellidos').editable({
        type: 'text',
        name: 'nombres',
        success: function(res, new_value){
            actualizar_brigadista("apellido", new_value, $(this).attr("b_id"))
        }
    });

    $('.cedula').editable({
        type: 'text',
        name: 'nombres',
        success: function(res, new_value){
            actualizar_brigadista("cedula", new_value, $(this).attr("b_id"))
        }
    });

    $('.ocupaciones').editable({
        type: 'text',
        name: 'nombres',
        success: function(res, new_value){
            actualizar_brigadista("ocupacion", new_value, $(this).attr("b_id"))
        }
    });

    $('.funcion_sistema').editable({
        type: 'text',
        name: 'nombres',
        success: function(res, new_value){
            actualizar_brigadista("funcion_sistema", new_value, $(this).attr("b_id"))
        }
    });

    $('.anios_sistema').editable({
        type: 'text',
        name: 'nombres',
        success: function(res, new_value){
            actualizar_brigadista("anios_sistema", new_value, $(this).attr("b_id"))
        }
    });

    $('.celular_asignado').editable({
        type: 'text',
        name: 'nombres',
        success: function(res, new_value){
            actualizar_brigadista("celular_asignado", new_value, $(this).attr("b_id"))
        }
    });

    $('.celular_personal').editable({
        type: 'text',
        name: 'nombres',
        success: function(res, new_value){
            actualizar_brigadista("celular_personal", new_value, $(this).attr("b_id"))
        }
    });

    $('.etnia').editable({
        type: 'select2',
        value : '',
        source: ["creole", "misquito", "garifona", "rama", "ulwa", "mestizo"],
        select2: {
            'width': 140
        },
        success: function(res, new_value){
            actualizar_brigadista("etnia", new_value, $(this).attr("b_id"))
        }
    });
    
    $('.sexo').editable({
        type: 'select2',
        value : '',
        source: ["femenino", "masculino"],
        select2: {
            'width': 140
        },
        success: function(res, new_value){
            actualizar_brigadista("sexo", new_value, $(this).attr("b_id"))
        }
    });


    $('.comunidad').editable({
        type: 'select2',
        value : '',
        //onblur:'ignore',
        source: comunidades,
        select2: {
            'width': 140
        },
        success: function(res, new_value){
            actualizar_brigadista("comunidad", new_value, $(this).attr("b_id"))
        }
    });
    $('.primaria').editable({
        type: 'select2',
        value : 'vacio',
        source: [
            {
                id:"1", 
                text: "Primer Grado"
            },
            {
                id:"2", 
                text: "Segundo Grado"
            },
            {
                id:"3", 
                text: "Tercer Grado"
            },
            {
                id:"4", 
                text: "Cuarto Grado"
            },
            {
                id:"5", 
                text: "Quinto Grado"
            },
            {
                id:"6", 
                text: "Sexto Grado"
            },
        ],
        select2: {
            'width': 140
        },
        success: function(res, new_value){
            actualizar_brigadista("primaria", new_value, $(this).attr("b_id"))
        }
    });
    $('.secundaria').editable({
        type: 'select2',
        value : 'opcion',
        source: [
            {
                id:"7", 
                text: "Primer Año"
            },
            {
                id:"8", 
                text: "Segundo Año"
            },
            {
                id:"9", 
                text: "Tercer Año"
            },
            {
                id:"10", 
                text: "Cuarto Año"
            },
            {
                id:"11", 
                text: "Quinto Año"
            }
        ],
        select2: {
            'width': 140
        },
        success: function(res, new_value){
            actualizar_brigadista("secundaria", new_value, $(this).attr("b_id"))
        }
    });
    $('.tecnico').editable({
        type: 'text',
        name: 'valor_tecnico',
        success: function(res, new_value){
            actualizar_brigadista("tecnico", new_value, $(this).attr("b_id"))
        }
    });
    $('.universidad').editable({
        type: 'text',
        name: 'valor_universidad',
        success: function(res, new_value){
            actualizar_brigadista("universidad", new_value, $(this).attr("b_id"))
        }
    });
    $('.otro').editable({
        type: 'text',
        name: 'valor_otro',
        success: function(res, new_value){
            actualizar_brigadista("valor_otro", new_value, $(this).attr("b_id"))
        }
    });
    
    $('.escolaridad').editable({
        type: 'select2',
        value : '',
        source: ["primaria", "secundaria", "tecnico", "universidad", "otro"],
        select2: {
            'width': 140
        },
        success: function(res, new_value){
            actualizar_brigadista("escolaridad", new_value, $(this).attr("b_id"))
        }
    });
    $('.escolaridad').on('shown', function(e, editable) {
        $(document).on('change', editable, function() {
                    
            var new_value = editable.input.$input[0].value;
    
            if (new_value == 'primaria') {
                $(".div-primaria").removeClass("hide")
                $(".div-secundaria").addClass("hide")
                $(".div-tecnico").addClass("hide")
                $(".div-universidad").addClass("hide")
                $(".div-otros-estudios").addClass("hide")
            }
            if (new_value == 'secundaria') {
                $(".div-primaria").addClass("hide")
                $(".div-secundaria").removeClass("hide")
                $(".div-tecnico").addClass("hide")
                $(".div-universidad").addClass("hide")
                $(".div-otros-estudios").addClass("hide")
            }
            if (new_value == 'tecnico') {
                $(".div-primaria").addClass("hide")
                $(".div-secundaria").addClass("hide")
                $(".div-tecnico").removeClass("hide")
                $(".div-universidad").addClass("hide")
                $(".div-otros-estudios").addClass("hide")
            }
            if (new_value == 'universidad') {
                $(".div-primaria").addClass("hide")
                $(".div-secundaria").addClass("hide")
                $(".div-tecnico").addClass("hide")
                $(".div-universidad").removeClass("hide")
                $(".div-otros-estudios").addClass("hide")
            }
            if (new_value == 'otro') {
                $(".div-primaria").addClass("hide")
                $(".div-secundaria").addClass("hide")
                $(".div-tecnico").addClass("hide")
                $(".div-universidad").addClass("hide")
                $(".div-otros-estudios").removeClass("hide")
            }
        });
    });

    
}


function actualizar_brigadista(llave, valor, b_id){
    var formData = new FormData()
    formData.append("b_id", b_id)
    formData.append(llave, valor)
    formData.append("csrfmiddlewaretoken", csrftoken)
    
    $.ajax({
        url : '/admin/actualizar_brigadista/',
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
}