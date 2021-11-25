import numpy as np
import matplotlib.pyplot as plt


def fournier_forand_pf(n, mu, phi):
    def delta(theta=phi):
        delta = 4 / (3 * (n - 1)**2) * np.sin(theta / 2) ** 2
        return delta
    nu = (3-mu)/2
    beta = 1/(4*np.pi*(1-delta())**2*delta()**nu) * (nu*(1-delta()) - (1-delta()**nu) +
             (delta()*(1-delta()**nu)-nu*(1-delta())) * np.sin(phi/2)**(-2)) +\
           (1-delta(np.pi)**nu)/(16*np.pi*(delta(np.pi)-1)*delta(np.pi)**nu)*(3*np.cos(phi)**2 -1)
    return beta


def henvey_greenstein_pf(phi, g):
    mu = np.cos(phi)
    beta = (1/(4*np.pi))*((1-g**2)/(1+g**2-2*g*mu)**(3/2))
    return beta


def henvey_greenstein_bb(g):
    bb= (1-g)/(2*g)*((1+g)/np.sqrt(1+g**2)-1)
    return bb


_30_angle, _30_pf = np.loadtxt("ressources/_minus_30_sea_ice_phase_function.txt", skiprows=2).T
_10_angle, _10_pf = np.loadtxt("ressources/_minus_10_sea_ice_phase_function.txt", skiprows=2).T


_ns = [1.021, 1.040, 1.08, 1.175, 1.15]
_mus = [3.0742, 3.2010, 3.483, 4.065, 4.874]
_bbs = [0.0001, 0.001, 0.01, 0.1, 0.4]

_gs = np.linspace(0.98, 0.98, 1)
_phis = np.linspace(0, np.pi, 100)

plt.scatter(_10_angle*np.pi/180, _10_pf)
plt.scatter(_30_angle*np.pi/180, _30_pf)
for _g in _gs:
    _beta_HG = henvey_greenstein_pf(phi=_phis, g=_g)
    _HG_bb = henvey_greenstein_bb(g=_g)
    plt.semilogy(_phis, _beta_HG, label='g={:.2f}, bb={:.4f}'.format(_g, _HG_bb))
for _n, _mu, _bb in zip(_ns, _mus, _bbs):
    _beta_FF = fournier_forand_pf(n=_n, mu=_mu, phi=_phis)
    plt.semilogy(_phis, _beta_FF, linestyle='--', label='bb={:.4f}'.format(_bb))
plt.legend()
plt.show()

#plt.plot(_gs, henvey_greenstein_bb(_gs))
#plt.show()