# Simple Bike Rental Shop

EL código es un simple ejercicio que representa una tienda de renta de bicicletas.
AL rentar una bici se debe pasar como parametro un id de usuario y un id de bicileta. Las clases de Usuario y Bicicleta no estan modeladas.


###Ejemplo de código cliente:
```python
from bike_rental import BikesRental

bike_shop_rental = BikesRental(stock_bikes = 20)

bike_shop_rental.rent_bike_per_hour('USER001', 'BIKE001')

bike_shop_rental.rent_bike_per_day('USER001', 'BIKE002')
```

El Usuario debe devolver todas las bicicletas para generar la factura y calcular el precio final.
```python
bike_shop_rental.return_bike('BIKE001')

bike_shop_rental.return_bike('BIKE002')

final_price = bike_shop_rental.generate_bill('USER001')
```


###Requerimientos:

Python 3
pip install -U pytest



###Ejecutar Pruebas:
pytest