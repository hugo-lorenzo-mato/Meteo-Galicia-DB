from django import forms
from django.forms import widgets

CHOICES= (
    ('24', '24 horas'),
    ('48', '48 horas'),
    ('72', '72 horas'),
)


opciones_meteosix = (
    ('temperature', 'Temperatura'),
    ('sky_state', 'Estado del cielo'),
    ('precipitation_amount', 'Precipitaciones'),
    ('wind', 'Viento'),
    ('relative_humidity', 'Humedad Relativa'),
    ('cloud_area_fraction', 'Cobertura de nubes'),
    ('snow_level', 'Cota de nieve'),

)

anhos_selector = (
    ('1950', '1950'),
    ('1951', '1951'),
    ('1952', '1952'),
    ('1953', '1953'),
    ('1954', '1954'),
    ('1955', '1955'),
    ('1956', '1956'),
    ('1957', '1957'),
    ('1958', '1958'),
    ('1959', '1959'),
    ('1960', '1960'),
    ('1961', '1961'),
    ('1962', '1962'),
    ('1963', '1963'),
    ('1964', '1964'),
    ('1965', '1965'),
    ('1966', '1966'),
    ('1967', '1967'),
    ('1968', '1968'),
    ('1969', '1969'),
    ('1970', '1970'),
    ('1971', '1971'),
    ('1972', '1972'),
    ('1973', '1973'),
    ('1974', '1974'),
    ('1975', '1975'),
    ('1976', '1976'),
    ('1977', '1977'),
    ('1978', '1978'),
    ('1979', '1979'),
    ('1980', '1980'),
    ('1981', '1981'),
    ('1982', '1982'),
    ('1983', '1983'),
    ('1984', '1984'),
    ('1985', '1985'),
    ('1986', '1986'),
    ('1987', '1987'),
    ('1988', '1988'),
    ('1989', '1989'),
    ('1990', '1990'),
    ('1991', '1991'),
    ('1992', '1992'),
    ('1993', '1993'),
    ('1994', '1994'),
    ('1995', '1995'),
    ('1996', '1996'),
    ('1997', '1997'),
    ('1998', '1998'),
    ('1999', '1999'),
    ('2000', '2000'),
    ('2001', '2001'),
    ('2002', '2002'),
    ('2003', '2003'),
    ('2004', '2004'),
    ('2005', '2005'),
    ('2006', '2006'),
    ('2007', '2007'),
    ('2008', '2008'),
    ('2009', '2009'),
    ('2010', '2010'),
    ('2011', '2011'),
    ('2012', '2012'),
    ('2013', '2013'),
    ('2014', '2014'),
    ('2015', '2015'),
    ('2016', '2016'),
    ('2017', '2017'),
)

estacion = (
    ("1387","A Coruña A Coruña (Estación completa) 1387"),
    ("1387E","A Coruña A Coruña (Aeroporto) 1387E"),
    ("1428","A Coruña Santiago de Compostela (Labacolla) 1428"),
    ("1393","A Coruña Cabo Vilán 1393"),
    ("1505","Lugo Rozas (Aeródromo) 1505"),
    ("1690A","Ourense Ourense (Granxa Deputación) 1690A"),
    ("1484C","Pontevedra Pontevedra (Mourente) 1484C"),
    ("1495","Pontevedra Vigo (Peinador) 1495"),
)

tiposGraficas = (
    ('histogramaTemperaturas', 'Histograma temperaturas'),
    ('rosaVientos', 'Rosa de los vientos'),
    ('tablaPrecipitaciones', 'Tabla Precipitaciones'),
    ('histogramaHumedad', 'Histograma Humedad Relativa')
)

class FormRequest(forms.Form):

    Lugar = forms.CharField(required=False)
    Longitud = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'long'}))
    Latitud = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'lat'}))
    Prediccion = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    Variables = forms.MultipleChoiceField(choices=opciones_meteosix,
                                          widget=widgets.CheckboxSelectMultiple(),
                                          )
    Grafica = forms.TypedChoiceField(widget=forms.Select, choices=tiposGraficas)
    Año = forms.TypedChoiceField(widget=forms.Select, choices=anhos_selector)
    Estacion_meteorológica = forms.TypedChoiceField(widget=forms.Select, choices=estacion)
