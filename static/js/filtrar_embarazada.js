$(document).ready(load)

function load(){
    $("#btn_exportar_embarazadas").on("click", function(e) {
        e.preventDefault();
        let form = $("#form-filtrar-embarazada")
        form.attr("target", "_blank")
        form.attr("action", "/admin/exportar_embarazadas/").submit()
        form.attr("action", "/admin/filtrar_embarazada/")
        form.attr("target", "_self")
    });
    
    $('.show-details-btn').on('click', function(e) {
        e.preventDefault();
        $(this).closest('tr').next().toggleClass('open');
        $(this).find(ace.vars['.icon']).toggleClass('fa-angle-double-down').toggleClass('fa-angle-double-up');
    });
}