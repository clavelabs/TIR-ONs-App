import datetime
from scipy import optimize


def xnpv(rate, cashflows):
    chron_order = sorted(cashflows, key=lambda x: x[0])
    t0 = chron_order[0][0]  # t0 is the date of the first cash flow

    return sum([cf / (1 + rate) ** ((t - t0).days / 365.0) for (t, cf) in chron_order])


def xirr(cashflows, guess=0.1):
    return optimize.newton(lambda r: xnpv(r, cashflows), guess) * 100


def tir(cashflow, precio, plazo=1):
    flujo_total = [
        (datetime.datetime.today() + datetime.timedelta(days=plazo), -precio)
    ]
    for i in range(len(cashflow)):
        if cashflow.iloc[
            i, 0
        ].to_pydatetime() > datetime.datetime.today() + datetime.timedelta(days=plazo):
            flujo_total.append(
                (cashflow.iloc[i, 0].to_pydatetime(), cashflow.iloc[i, 1])
            )

    return round(xirr(flujo_total, guess=0.1), 2)


def duration(cashflow, precio, plazo=2):
    r = tir(cashflow, precio, plazo=plazo)
    denom = []
    numer = []
    for i in range(len(cashflow)):
        if cashflow.iloc[
            i, 0
        ].to_pydatetime() > datetime.datetime.today() + datetime.timedelta(days=plazo):
            tiempo = (
                cashflow.iloc[i, 0] - datetime.datetime.today()
            ).days / 365  # tiempo al cupon en años
            cupon = cashflow.iloc[i, 1]
            denom.append(cupon * (1 + r / 100) ** tiempo)  # sum (C(1+r)^t)
            numer.append(tiempo * (cupon * (1 + r / 100) ** tiempo))

    return round(sum(numer) / sum(denom), 2)


# OJO ACA, cashflows es una variable global, arreglar para poder utilizar.
def modified_duration(cashflow, precio, plazo=2):
    duration = duration(cashflow, precio, plazo)
    return round(duration / (1 + tir(cashflow, precio, plazo) / 100), 2)
