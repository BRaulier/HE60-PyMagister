import numpy as np
import scipy.integrate as integrate
from scipy.special import eval_legendre
import matplotlib.pyplot as plt

from HE60PY.Tools import olympus
from HE60PY.Tools.phase_function_discretizer import *



def calculate_assym(theta, pf):
    theta_rad = theta * np.pi / 180
    return 2 * np.pi * integrate.simps(pf * np.cos(theta_rad) * np.sin(theta_rad), x=theta_rad)

class PhaseFunction:
    def __init__(self):
        self.p = None
        self.theta = np.linspace(0, np.pi, 1000)
        self.theta_deg = np.linspace(0, np.pi, 1000) * 180 / np.pi

    def moment(self, n):
        to_integrate = lambda mu: mu**n * self.density(mu)*self.normalization_factor
        res, err = integrate.quad(to_integrate, -1, 1)
        return res

    @property
    def mean(self):
        return self.moment(n=1)

    @property
    def variance(self):
        return self.moment(n=2)

    @property
    def skewness(self):
        return self.moment(n=3)

    def normalize(self, p_mu):
        res, err = integrate.quad(p_mu, -1, 1, epsrel=1e-6, limit=500)
        self.p = self.p / res
        return 1/res

    def already_discretized(self):
        path_to_dpf = f"/Applications/HE60.app/Contents/data/phase_functions/HydroLight/{self.dpf_name}.txt"
        return DoesThisExist(path_to_dpf)

    def discretize_if_needed(self):
        if self.already_discretized() is False:
            print(f"Discretizing phase function {self.tab_name}...")
            create_executable_discretizer()
            create_tabulated_file(angle_beta_array=np.vstack((self.theta_deg, self.p_deg)), tab_filename=self.tab_name, pf_type=self.pf_type)
            create_input_file(input_filename=self.tab_name, dpf_filename=self.tab_name, tab_filename=self.tab_name)
            run_executable_discretizer(input_filename=self.tab_name)
            print(f"Discretization completed, available in HE library as '{self.dpf_name}.txt'!")


class OTHG(PhaseFunction):
    def __init__(self, g):
        super().__init__()
        self.g = g
        self.p =  self.density(mu=np.cos(self.theta))
        self.normalize(p_mu=self.density)
        self.p_deg = self.p/(2*np.pi)

        self.dpf_name = f'dpf_OTHG_{self.g:.2f}'.replace('.', '_')
        self.tab_name = f'OTHG_{self.g:.2f}'.replace('.', '_')
        self.pf_type = "One term Henyey Greenstein"

    def density(self, mu):
        p = 1/2 * (1-self.g**2) / (1 + self.g**2 - 2*self.g*mu)**(3/2)
        return p


class OTHGStar(PhaseFunction):
    def __init__(self, g):
        super().__init__()
        self.g = g
        self.p =  self.density(mu=np.cos(self.theta))
        self.normalize(p_mu=self.density)
        self.p_deg = self.p/(2*np.pi)

        self.dpf_name = f'dpf_OTHG_star_{self.g:.2f}'.replace('.', '_')
        self.tab_name = f'OTHG_star_{self.g:.2f}'.replace('.', '_')
        self.pf_type = "One term Henyey Greenstein star version"

    def density(self, mu):
        p = 3/2 * (1-self.g**2)/(2+self.g**2) * (1+mu**2)/(1+self.g**2-2*self.g*mu)**(3/2)
        return p


class ThreeTHG(PhaseFunction): # A THREE-PARAMETER ANALYTIC PHASE FUNCTION FOR MULTIPLE SCATTERING CALCULATIONS GEORGE W. KATIAWAR
    def __init__(self, g, h, t):
        super().__init__()
        self.g, self.h, self.t = g, h, t
        self.g2, self.g1, self.a = self.solve()
        self.p = self.density(mu=np.cos(self.theta))
        self.normalization_factor = self.normalize(p_mu=self.density)
        self.p_deg = self.p/(2*np.pi)

        self.dpf_name = f'dpf_ThreeTHG_g{self.g:.3f}_h{self.h:.3f}_t{self.t:.3f}'.replace('.', '_')
        self.tab_name = f'ThreeTHG_g{self.g:.3f}_h{self.h:.3f}_t{self.t:.3f}'.replace('.', '_')
        self.pf_type = "Three term Henyey Greenstein (Kattawar)"

    def solve(self): # Equations 15, 16, and 17
        g, h, t = self.g, self.h, self.t # To avoid 1 kilometer long expression below
        g2 = (t - h * g - ((h * g - t)**2 - 4 * (h - g**2)*(t * g - h**2))**(1/2)) / (2*(h - g**2))
        g1 = (g * g2 -  h)/(g2 - g)
        a = (g - g2)/(g1 - g2)
        assert np.abs(g2) < 1, "Current implementation doesn't deal with abs(g2) greater than one!!"
        return g2, g1, a

    def density(self, mu):
        term_1 = (1-self.g1**2)/(1-2*self.g1*mu+self.g1**2)**(3/2)
        term_2 = (1-self.g2**2)/(1-2*self.g2*mu+self.g2**2)**(3/2)
        return self.a * term_1 + (1 - self.a) * term_2


class IDHG(PhaseFunction): # A note on double Henyey–Greenstein phase function Feng Zhang Jiangnan Li
    def __init__(self, g, h, l):
        super().__init__()
        self.g, self.h, self.l = g, h, l
        self.g2, self.g1, self.a = self.solve()
        self.p = self.density(mu=np.cos(self.theta))
        self.normalization_factor = self.normalize(p_mu=self.density)

    def solve(self):
        g, h, l = self.g, self.h, self.l  # To avoid 1 kilometer long expression below
        assert 4*(h-g**2) * (g*l-h**2) < (g*h-l)**2
        w = (g*h-l)**2 - 4*(h-g**2) * (g*l-h**2)
        g1 = (l-g*h + w**(1/2))/(2*(h-g**2))
        g2 = (l-g*h - w**(1/2))/(2*(h-g**2))
        a = 0.5 + (3*g*h-2*g**3-l)/(2*w**(1/2))
        if np.abs(g2) <= np.abs(g1):
            g1_prime = g2
            g2_prime = g1
            a = 0.5 - (3*g*h-2*g**3-l)/(2*w**(1/2))
            return g2_prime, g1_prime, a
        else:
            return g2, g1, a

    def density(self, mu):
        term_1 = (1-self.g1**2)/(1-2*self.g1*mu+self.g1**2)**(3/2)
        term_2 = (1-self.g2**2)/(1-2*self.g2*mu+self.g2**2)**(3/2)
        return self.a * term_1 + (1 - self.a) * term_2


class TwoTHG(PhaseFunction): # A One-parameter two-term Henyey-Greenstein phase function for light scattering in seawater
    def __init__(self, g, g1, a):
        super().__init__()
        self.g, self.g1, self.a = g, g1, a
        self.g2 = (self.a*self.g1 - self.g)/(1-self.a)
        self.p = self.density(mu=np.cos(self.theta))
        self.normalization_factor = self.normalize(p_mu=self.density)
        self.p_deg = self.p/(2*np.pi)

        self.dpf_name = f'dpf_TwoTHG_g{self.g:.3f}_h{self.g1:.3f}_a{self.a:.3f}'.replace('.', '_')
        self.tab_name = f'TwoTHG_g{self.g:.3f}_h{self.g1:.3f}_a{self.a:.3f}'.replace('.', '_')
        self.pf_type = "Two term Henyey Greenstein (Vladimir I. Haltrin)"

    def density(self, mu):
        term_1 = (1-self.g1**2)/(1-2*self.g1*mu+self.g1**2)**(3/2)
        term_2 = (1-self.g2**2)/(1-2*self.g2*mu+self.g2**2)**(3/2)
        return self.a * term_1 + (1 - self.a) * term_2


class TwoTHG_star(PhaseFunction): # A One-parameter two-term Henyey-Greenstein phase function for light scattering in seawater
    def __init__(self, a, g1, g2):
        super().__init__()
        self.a, self.g1, self.g2 = a, g1, g2
        self.p = self.density(mu=np.cos(self.theta))
        self.normalization_factor = self.normalize(p_mu=self.density)

    def density(self, mu):
        term_1 = (1-self.g1**2)/(1-2*self.g1*mu+self.g1**2)**(3/2)
        self.g2 = -1*self.g2
        term_2 = (1-self.g2**2)/(1-2*self.g2*mu+self.g2**2)**(3/2)
        return self.a * term_1 + (1 - self.a) * term_2



def run_tests():
    test_hg = HenyeyGreenstein(g=0.5)
    assert np.isclose(test_hg.moment(n=1), 0.5), "First moment should be equal to g value given"
    print(test_hg.moment(n=2), test_hg.moment(n=3))
    print("Henyey Greenstein okay!")






if __name__ == "__main__":
    test_dis = TwoTHG(g=0.95, g1=0.99, a=0.975)
    # test_dis.discretize_if_needed()
    test_hg = OTHG(g=0.99)
    plt.semilogy(test_hg.theta, test_hg.p, label=f"g=0.99")
    plt.semilogy(test_dis.theta, test_dis.p, label=f"g={test_dis.moment(n=1)}, g2={test_dis.g2}")
    plt.legend()
    plt.show()
    # # run_tests()

    # test_hgstar = HGStar(g=0.98)
    # plt.semilogy(test_hgstar.theta, test_hgstar.p)
    # plt.show()
    # test_RL = RL(a=11, b=10)
    # plt.semilogy(test_RL.theta, test_RL.p, label=f"RL g={test_RL.moment(n=1)}")
    # test_RL = RL(a=11, b=1)
    # plt.semilogy(test_RL.theta, test_RL.p, label=f"RL g={test_RL.moment(n=1)}")
    #
    # g = 0.98
    # h = 0.10
    # t = 0.34
    # test_dhg = DHG(g=g, h=h, t=t)
    # plt.semilogy(test_dhg.theta, test_dhg.p, label=f"g={g} h={h}, t={t}")
    # g = 0.98
    # h = 1.5
    # t = 0.0
    # test_idhg = IDHG(g=g, h=h, l=t)
    # plt.semilogy(test_idhg.theta, test_idhg.p, label=f"g={g} h={h}, t={t}")
    #
    # test_othg = OTHG(g=0.98)
    # plt.semilogy(test_othg.theta, test_othg.p, label=f"g={g} ")
    #
    # g=0.98
    # g1 = 0.01
    # a = 0.50
    # test_tthg = TTHG(g=g, g1=g1, a=a)
    # plt.semilogy(test_tthg.theta, test_tthg.p, label=f"g={g} g1={g1} a={a}, g2={test_tthg.g2}")
    #
    #
    #
    # g1 = 0.98
    # a = 0.999
    # g2 = 0.10
    #
    # test_tthg_star = TTHG_star(g1=g1, a=a, g2=g2)
    # g=test_tthg_star.moment(n=1)
    # plt.semilogy(test_tthg_star.theta, test_tthg_star.p, label=f"g1={g1} g2={test_tthg_star.g2} a={a} g={g}")
    # g1 = 0.98
    # a = 0.8
    # g2 = 0.24
    #
    # test_tthg_star = TTHG_star(g1=g1, a=a, g2=g2)
    # g=test_tthg_star.moment(n=1)
    # plt.semilogy(test_tthg_star.theta, test_tthg_star.p, label=f"g1={g1} g2={test_tthg_star.g2} a={a} g={g}")
    #
    # plt.legend()
    # plt.show()
    #
    #
    # print(test_tthg.moment(n=1), test_tthg.g2)
    # print(test_tthg.moment(n=2), test_tthg.g1)
    # print(test_tthg.moment(n=3), test_tthg.a)
    #
    # print(test_dhg.moment(n=1))
    # print(test_dhg.moment(n=2))
    # print(test_dhg.moment(n=3))
    # print(test_dhg.a*test_dhg.g1**3 + (1-test_dhg.a)*test_dhg.g2**3)













