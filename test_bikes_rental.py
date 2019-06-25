from bikes_rental import *
from datetime import datetime, timedelta

now = datetime.utcnow()


def test_no_billing_while_all_bikes_not_returned():
    bikes_rental = BikesRental()
    bikes_rental.rent_bike_per_week('10505155', 'NNGG45', start_time=(now - timedelta(days=10)))

    assert bikes_rental.bill_booking('10505155') == -1


def test_discount_for_rent_more_than_three_bikes():
    bikes_rental = BikesRental()
    bikes_rental.rent_bike_per_day('10505155', 'NNGG45', start_time=(now - timedelta(days=2)))
    bikes_rental.rent_bike_per_day('10505155', 'NNGG46', start_time=(now - timedelta(days=2)))
    bikes_rental.rent_bike_per_week('10505155', 'NNGG47', start_time=(now - timedelta(days=2)))
    bikes_rental.return_bike('NNGG45')
    bikes_rental.return_bike('NNGG46')
    bikes_rental.return_bike('NNGG47')

    assert bikes_rental.bill_booking('10505155') == 98 


def test_billing_for_rent_bike_for_three_week():
    bikes_rental = BikesRental()
    bikes_rental.rent_bike_per_week('10505155', 'EETT89', start_time=(now - timedelta(days=15)))
    bikes_rental.return_bike('EETT89')

    assert bikes_rental.bill_booking('10505155') == 3 * WEEK_PRICE


def test_billing_for_rent_bike_for_less_than_week():
    bikes_rental = BikesRental()
    bikes_rental.rent_bike_per_week('10505155', 'EETT89', start_time=(now - timedelta(days=1)))
    bikes_rental.return_bike('EETT89')

    assert bikes_rental.bill_booking('10505155') == WEEK_PRICE


def test_billing_for_rent_bike_for_three_days():
    bikes_rental = BikesRental()
    bikes_rental.rent_bike_per_day('10505155', 'EETT89', start_time=(now - timedelta(days=3)))
    bikes_rental.return_bike('EETT89')

    assert bikes_rental.bill_booking('10505155') == 3 * DAY_PRICE

def test_billing_for_rent_bike_for_less_than_a_day():
    bikes_rental = BikesRental()
    bikes_rental.rent_bike_per_day('10505155', 'EETT89', start_time=(now - timedelta(hours=3)))
    bikes_rental.return_bike('EETT89')

    assert bikes_rental.bill_booking('10505155') == DAY_PRICE


def test_billing_for_rent_bike_for_five_hours():
    bikes_rental = BikesRental()
    bikes_rental.rent_bike_per_hour('10505155', 'EETT89', start_time=(now - timedelta(hours=5)))
    bikes_rental.return_bike('EETT89')

    assert bikes_rental.bill_booking('10505155') == 5 * HOUR_PRICE


def test_billing_for_rent_bike_for_less_than_an_hour():
    bikes_rental = BikesRental()
    bikes_rental.rent_bike_per_hour('10505155', 'EETT89', start_time=(now - timedelta(minutes=15)))
    bikes_rental.return_bike('EETT89')

    assert bikes_rental.bill_booking('10505155') == HOUR_PRICE


def test_return_a_bike():
    bikes_rental = BikesRental()
    bikes_rental.rent_bike_per_hour('10505155', 'EETT89')
    assert bikes_rental.return_bike('EETT89') == 'EETT89'


def test_return_a_bike_that_was_not_rented():
    bikes_rental = BikesRental()
    assert bikes_rental.return_bike('EETT89') is None


def test_delete_rental_after_billed():
    bikes_rental = BikesRental()
    bikes_rental.rent_bike_per_hour('10505155', 'EETT89')
    bikes_rental.return_bike('EETT89')
    bikes_rental.bill_booking('10505155')
    assert bikes_rental.return_bike('EETT89') is None
