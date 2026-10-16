import numpy as np

# modeling
def sir_model(t, y, beta=0.125*1e-3, gamma=0.1):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return np.array([dSdt, dIdt, dRdt])

# numerical solvers for the SIR model
def euler(f, y, t, beta=0.125*1e-3, gamma=0.1):
    for i in range(1, len(t)):
        y[i] = y[i-1] + dt * f(t[i-1], y[i-1], beta=beta, gamma=gamma)
    return t, y


def runge_kutta(f, y, t, beta=0.125*1e-3, gamma=0.1):
    for i in range(1, len(t)):
        dt = t[i] - t[i-1]
        k1 = f(t[i-1], y[i-1], beta=beta, gamma=gamma)
        k2 = f(t[i-1] + dt/2, y[i-1] + dt/2 * k1, beta=beta, gamma=gamma)
        k3 = f(t[i-1] + dt/2, y[i-1] + dt/2 * k2, beta=beta, gamma=gamma)
        k4 = f(t[i-1] + dt, y[i-1] + dt * k3, beta=beta, gamma=gamma)
        y[i] = y[i-1] + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
    return t, y

# custom solver
def sir_solver(f, y0, days, dt, method="euler", beta=0.125*1e-3, gamma=0.1):
    t = np.arange(0, days + dt, dt)
    y = np.zeros((len(t), len(y0)))
    # initial population values
    y[0] = y0
    
    if method == "euler":
        return euler(f, y, t, beta=beta, gamma=gamma)
    elif method == "runge_kutta":
        return runge_kutta(f, y, t, beta=beta, gamma=gamma)
    
