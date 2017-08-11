from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboardView'),
    url(r'^agregar_embarazada/$', views.agregar_embarazada, name='agregarEmbarazadaView'),
    url(r'^agregar_brigadista/$', views.agregar_brigadista, name='agregarBrigadistaView'),
    url(r'^monitoreo_durante_embarazo/(?P<id>[-\w]+)/$', views.monitoreo_durante_embarazo, name='monitoreoDuranteEmbarazoView'),
    url(r'^monitoreo_salida_comunidad/(?P<id>[-\w]+)/$', views.monitoreo_salida_comunidad, name='monitoreoSalidaComunidadView'),
    url(r'^monitoreo_durante_parto/(?P<id>[-\w]+)/$', views.monitoreo_durante_parto, name='monitoreoDurantePartoView'),
    url(r'^monitoreo_postparto_madre/(?P<id>[-\w]+)/$', views.monitoreo_postparto_madre, name='monitoreoPostpartoMadreView'),
    url(r'^monitoreo_postparto_hijo/(?P<id>[-\w]+)/$', views.monitoreo_postparto_hijo, name='monitoreoPostpartoHijoView'),
    url(r'^modificar_embarazada/$', views.modificar_embarazada, name='modificarEmbarazadaView'),
    url(r'^filtrar_embarazada/$', views.vista_filtrar_embarazada, name='filtrarEmbarazadaView'),
    url(r'^filtrar_embarazada_post/$', views.filtrar_embarazada, name='filtrar_embarazada_post'),
    url(r'^modificar_brigadista/$', views.modificar_brigadista, name = 'modificarBrigadistaView'),
    url(r'^embarazada_durante_embarazo/$', views.monitoreo_durante_embarazo_post.as_view()),
    url(r'^embarazada_comunidad/$', views.monitoreo_salida_comunidad_post.as_view()),
    url(r'^insert_brigadist/$', views.ajax_agregar_brigadista.as_view()),
    url(r'^insert_pregnant/$', views.ajax_agregar_embarazada.as_view()),
    url(r'^actualizar_brigadista/$', views.ajax_actualizar_brigadista.as_view()),
    url(r'^actualizar_embarazada/$', views.ajax_actualizar_embarazadas.as_view()),
    url(r'^embarazada_durante_parto/$', views.monitoreo_durante_parto_post.as_view()),
    url(r'^embarazada_postparto_madre/$', views.monitoreo_postparto_madre_post.as_view()),
    url(r'^embarazada_postparto_hijo/$', views.monitoreo_postparto_hijo_post.as_view())
    
]