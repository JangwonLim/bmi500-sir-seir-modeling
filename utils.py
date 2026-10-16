import numpy as np
# ========================= SIR Model ========================= 
# modeling
def sir_model(t, y, beta=0.125*1e-3, gamma=0.1):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return np.array([dSdt, dIdt, dRdt])

# numerical solvers for the SIR model
def euler(f, y, t, beta=0.125*1e-3, gamma=0.1):
    dt = t[1] - t[0]
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
    
    
# ========================= SEIR Model ========================= 
def seir_modeling(t, y, beta, gamma, sigma, mu, N=2000):
    S, E, I, R = y
    dSdt = mu*N - beta*S*I - mu*S
    dEdt = beta*S*I - (sigma + mu)*E
    dIdt = sigma*E - (gamma + mu)*I
    dRdt = gamma*I - mu*R

    return np.array([dSdt, dEdt, dIdt, dRdt])

def seir_runge_kutta(f, y, t, beta, gamma, sigma, mu, N=2000):
    for i in range(1, len(t)):
        dt = t[i] - t[i-1]
        k1 = f(t[i-1], y[i-1], beta, gamma, sigma, mu, N)
        k2 = f(t[i-1] + dt/2, y[i-1] + dt/2 * k1, beta, gamma, sigma, mu, N)
        k3 = f(t[i-1] + dt/2, y[i-1] + dt/2 * k2, beta, gamma, sigma, mu, N)
        k4 = f(t[i-1] + dt, y[i-1] + dt * k3, beta, gamma, sigma, mu, N)
        y[i] = y[i-1] + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
    return t, y

# Use runge_kutta to solve the SEIR model
def seir_solver(f, y0, days, dt, beta, gamma, sigma, mu, N=2000):
    t = np.arange(0, days + dt, dt)
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    t, y = seir_runge_kutta(f, y, t, beta, gamma, sigma, mu, N)
    return t, y