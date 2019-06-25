from datetime import datetime
# from fake_db import get_rentals_db

HOUR_PRICE = 5
DAY_PRICE = 20
WEEK_PRICE = 60


class BikesRental(object):

    def __init__(self, stock_bikes=50):
        self.stock_bikes = stock_bikes
        self.current_rentals = []  # get_rentals_db()

    def rent_bike_per_hour(self, customer_id, bike_id, start_time=None):
        '''
            Rentar una bici en base hora.
        '''
        rental = RentalByHour(customer_id, bike_id, start_time)
        self.current_rentals.append(rental)
        self.stock_bikes -= 1

    def rent_bike_per_day(self, customer_id, bike_id, start_time=None):
        '''
            Rentar una bici en base dia.
        '''
        rental = RentalByDay(customer_id, bike_id, start_time)
        self.current_rentals.append(rental)
        self.stock_bikes -= 1

    def rent_bike_per_week(self, customer_id, bike_id, start_time=None):
        '''
            Rentar una bici en base semana.
        '''
        rental = RentalByWeek(customer_id, bike_id, start_time)
        self.current_rentals.append(rental)
        self.stock_bikes -= 1

    def return_bike(self, bike_id):
        '''
            Devolver una bici por bike_id.
        '''
        rental = self._get_rental_by_bike_id(bike_id=bike_id)
        if not rental:
            print("No hay renta activa para la bici %s ." % bike_id)
            return None
        rental.finish_rent_time()
        return bike_id

    def generate_bill(self, customer_id):
        '''
            Facturar todas las rentas para un usuario, una vez devueltas todas las bicis.
        '''
        rentals_by_customer = self._get_rentals_by_customer_id(customer_id)
        if not self._bikes_have_been_returned(rentals_by_customer):
            print("Deben devolverse todas las bicis antes de Calcular la factura. ¬¬")
            return -1
        final_price = self._calculate_final_price(rentals_by_customer)
        print("El precio final facturado es de $", final_price)
        self._delete_rentals(customer_id)
        return final_price

    def _calculate_final_price(self, rentals_by_customer):
        final_price = sum([r.calculate_price() for r in rentals_by_customer])
        if len(rentals_by_customer) > 2:
            final_price = final_price * 0.7
        return final_price

    def _bikes_have_been_returned(self, rentals_by_customer):
        all_bikes_returned = True
        for r in rentals_by_customer:
            if not r.bike_returned:
                print("La Bici \'%s\' todavia no fue devuelta." % (r.bike_id))
                all_bikes_returned = False
        return all_bikes_returned

    def _get_rentals_by_customer_id(self, customer_id):
        rentals_result = list()
        rentals_result = [r for r in self.current_rentals if r.customer_id == customer_id]
        return rentals_result

    def _get_rental_by_bike_id(self, bike_id):
        for r in self.current_rentals:
            if r.bike_id == bike_id:
                return r

    def _delete_rentals(self, customer_id):
        for r in self.current_rentals:
            if r.customer_id == customer_id:
                self.current_rentals.remove(r)


class Rental(object):

    def __init__(self, customer_id, bike_id, start_time=None):
        self.customer_id = customer_id
        self.bike_id = bike_id
        self.start_time = start_time or datetime.utcnow()
        self.end_time = None
        self.bike_returned = False

    def finish_rent_time(self):
        self.end_time = datetime.utcnow()
        self.bike_returned = True

    def calculate_price(self):
        pass


class RentalByHour(Rental):

    def __init__(self, customer_id, bike_id, start_time=None):
        super().__init__(customer_id, bike_id, start_time)

    def calculate_price(self):
        '''
            Calcular precio en base hora.
        '''
        if not self.bike_returned:
            print("La bici todavia no fue devuelta.")
            return
        billed_hours = (self.end_time - self.start_time).seconds // 3600
        price = billed_hours * HOUR_PRICE
        if price < HOUR_PRICE:
            price = HOUR_PRICE
        return price


class RentalByDay(Rental):

    def __init__(self, customer_id, bike_id, start_time=None):
        super().__init__(customer_id, bike_id, start_time)

    def calculate_price(self):
        '''
            Calcular precio en base dia.
        '''
        if not self.bike_returned:
            print("La bici todavia no fue devuelta.")
            return
        billed_days = (self.end_time - self.start_time).days
        price = billed_days * DAY_PRICE
        if price < DAY_PRICE:
            price = DAY_PRICE
        return price


class RentalByWeek(Rental):

    def __init__(self, customer_id, bike_id, start_time=None):
        super().__init__(customer_id, bike_id, start_time)

    def calculate_price(self):
        '''
            Calcular precio en base mes.
        '''
        if not self.bike_returned:
            print("La bici todavia no fue devuelta.")
            return
        billed_weeks = int((self.end_time - self.start_time).days / 7) + 1
        return billed_weeks * WEEK_PRICE
