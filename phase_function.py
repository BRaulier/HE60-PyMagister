import numpy as np
import matplotlib.pyplot as plt


def fournier_forand_pf(n, mu, phi):
    def delta(theta=phi):
        delta = 4 / (3 * (n - 1)**2) * np.sin(theta / 2) ** 2
        return delta
    nu = (3-mu)/2
    beta = 1/(4*np.pi*(1-delta())**2 *delta()**nu) * (nu*(1-delta()) - (1-delta()**nu) +
             (delta()*(1-delta()**nu)-nu*(1-delta())) * np.sin(phi/2)**(-2)) +\
           (1-delta(np.pi)**nu)/(16*np.pi*(delta(np.pi)-1)*delta(np.pi)**nu)*(3*np.cos(phi)**2 -1)
    normalised_beta = beta/np.sum(beta)
    return beta


def compute_g_fournier_forand(n, mu):
    thetas = np.linspace(0.000001, np.pi, 100000)
    d_theta = np.pi/1e3
    normaliz_factor = 2*np.pi*np.sum(fournier_forand_pf(n, mu, thetas)*np.sin(thetas)*d_theta)
    g = 2*np.pi*np.sum(fournier_forand_pf(n, mu, thetas) * np.cos(thetas)*np.sin(thetas)*d_theta)
    return g/normaliz_factor

def henvey_greenstein_pf(phi, g):
    mu = np.cos(phi)
    beta = (1/(4*np.pi))*((1-g**2)/(1+g**2-2*g*mu)**(3/2))
    # normalised_beta = beta/np.sum(beta)
    return beta


def henvey_greenstein_bb(g):
    bb= (1-g)/(2*g)*((1+g)/np.sqrt(1+g**2)-1)
    return bb


_30_angle, _30_pf = np.loadtxt("ressources/_minus_30_sea_ice_phase_function.txt", skiprows=2).T
_10_angle, _10_pf = np.loadtxt("ressources/_minus_10_sea_ice_phase_function.txt", skiprows=2).T

#
# _ns = [1.021, 1.040, 1.08, 1.175, 1.15]
# _mus = [3.0742, 3.2010, 3.483, 4.065, 4.874]
# _bbs = [0.0001, 0.001, 0.01, 0.1, 0.4]
_ns = [1.040, 1.08, 1.175]
_mus = [3.2010, 3.483, 4.065]
_bbs = [0.001, 0.01, 0.1]           #    0.995       0.95        0.6582

_gs = [0.995, 0.954, 0.6582, .85, .985, .94]
# _gs = np.linspace(0.6582, 0.85, 10)
_phis = np.linspace(0.001, np.pi, 100000)



# plt.scatter(_10_angle*np.pi/180, _10_pf)
# plt.scatter(_30_angle*np.pi/180, _30_pf)

colors = ['red', 'blue', 'green', 'green', 'orange', 'black', 'grey', 'yellow', 'brown', 'olive']
for i, _g in enumerate(_gs):
    _beta_HG = henvey_greenstein_pf(phi=_phis, g=_g)
    _HG_bb = henvey_greenstein_bb(g=_g)
    plt.semilogy(_phis, _beta_HG, label='HG g={:.3f}, bb/b={:.5f}'.format(_g, _HG_bb), color=colors[i])

for i, (_n, _mu, _bb) in enumerate(zip(_ns, _mus, _bbs)):
    _beta_FF = fournier_forand_pf(n=_n, mu=_mu, phi=_phis)
    _g_FF = compute_g_fournier_forand(n=_n, mu=_mu)
    plt.semilogy(_phis, _beta_FF, linestyle='--', label='FF bb/b={:.4f}'
                                                        '\n {:.7f}'.format(_bb,_g_FF ), color=colors[i])
plt.xlabel(r'$\theta$ [rad]')
plt.ylabel(r'p($\theta$) [-]')
plt.legend()
plt.show()




#plt.plot(_gs, henvey_greenstein_bb(_gs))
#plt.show()