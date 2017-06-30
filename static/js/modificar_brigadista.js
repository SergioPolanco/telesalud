$(document).ready(load)

var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

function load(){
    
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

    $('.escolaridades').editable({
        type: 'text',
        name: 'nombres',
        success: function(res, new_value){
            actualizar_brigadista("escolaridad", new_value, $(this).attr("b_id"))
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
        type: 'text',
        name: 'nombres',
        success: function(res, new_value){
            actualizar_brigadista("etnia", new_value, $(this).attr("b_id"))
        }
    });

    $('.comunidad').editable({
        type: 'select2',
        value : '',
        //onblur:'ignore',
        source: cities,
        select2: {
            'width': 140
        },
        success: function(res, new_value){
            
        }
    });
    $('.municipio').editable({
        type: 'select2',
        value : '',
        //onblur:'ignore',
        source: cities,
        select2: {
            'width': 140
        },
        success: function(res, new_value){
            
        }
    });

    $('.centro_salud').editable({
        type: 'select2',
        value : '',
        //onblur:'ignore',
        source: cities,
        select2: {
            'width': 140
        },
        success: function(res, new_value){
            
        }
    });

    $('.region').editable({
        type: 'select2',
        value : '',
        //onblur:'ignore',
        source: cities,
        select2: {
            'width': 140
        },
        success: function(res, new_value){
            
        }
    });

    $('.sector').editable({
        type: 'select2',
        value : '',
        //onblur:'ignore',
        source: cities,
        select2: {
            'width': 140
        },
        success: function(res, new_value){
            
        }
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