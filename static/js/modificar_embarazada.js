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
            actualizar_embarazada("nombre", new_value, $(this).attr("e_id"))
        }
    });

    $('.apellidos').editable({
        type: 'text',
        name: 'nombres',
        success: function(res, new_value){
            actualizar_embarazada("apellido", new_value, $(this).attr("e_id"))
        }
    });

    $('.cedula').editable({
        type: 'text',
        name: 'nombres',
        success: function(res, new_value){
            actualizar_embarazada("cedula", new_value, $(this).attr("e_id"))
        }
    });

    $('.etnia').editable({
        type: 'text',
        name: 'nombres',
        success: function(res, new_value){
            actualizar_embarazada("etnia", new_value, $(this).attr("e_id"))
        }
    });

    $('.comunidad').editable({
        type: 'select2',
        value : '',
        //onblur:'ignore',
        source: cities,
        select2: {
            'width': 140
        }
    });
    $('.municipio').editable({
        type: 'select2',
        value : '',
        //onblur:'ignore',
        source: cities,
        select2: {
            'width': 140
        }
    });

    $('.centro_salud').editable({
        type: 'select2',
        value : '',
        //onblur:'ignore',
        source: cities,
        select2: {
            'width': 140
        }
    });

    $('.region').editable({
        type: 'select2',
        value : '',
        //onblur:'ignore',
        source: cities,
        select2: {
            'width': 140
        }
    });

    $('.edad').editable({
        type: 'spinner',
        name : 'age',
        spinner : {
            min : 16,
            max : 99,
            step: 1,
            on_sides: true
            //,nativeUI: true//if true and browser support input[type=number], native browser control will be used
        },
        success: function(res, new_value){
            actualizar_embarazada("edad", new_value, $(this).attr("e_id"))
        }
    });

    $('.semana_embarazo').editable({
        type: 'spinner',
        name : 'age',
        spinner : {
            min : 16,
            max : 99,
            step: 1,
            on_sides: true
            //,nativeUI: true//if true and browser support input[type=number], native browser control will be used
        },
        success: function(res, new_value){
            actualizar_embarazada("semana_embarazo", new_value, $(this).attr("e_id"))
        }
    });
}


function actualizar_embarazada(llave, valor, e_id){
    var formData = new FormData()
    formData.append("e_id", e_id)
    formData.append(llave, valor)
    formData.append("csrfmiddlewaretoken", csrftoken)
    
    $.ajax({
        url : '/admin/actualizar_embarazada/',
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