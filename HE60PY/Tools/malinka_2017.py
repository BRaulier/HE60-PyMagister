# -*- coding: utf-8 -*-
"""
Phase function for large inclusions inside sea ice (air bubbles and brines) according to their volume fraction ratio.
"""

# Module importation
import miepython
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps

# Other modules


def calculate_assym_g(theta, pf):
    theta_rad = theta * np.pi / 180
    return 2 * np.pi * integrate.simps(pf * np.cos(theta_rad) * np.sin(theta_rad), x=theta_rad)

# Function and classes
def pf_brines_malinka_2017(angles):
    """
    Phase function for optically soft and large particles according to Malinka et al (2017).
    :param angles: scattering angles [degrees] - array
    :return: phase function normalized to 1, asymmetry param - tuple
    """
    # Angles
    arad = angles * np.pi / 180
    mu = np.cos(arad)

    # Size parameter
    nb = 1.024
    x = 1 / (nb - 1)
    pf = (2 * x ** 2 * (1 + mu ** 2)) / (1 + 2 * (x ** 2) * (1 - mu)) ** 2

    # Calculate normalization param
    norm = 2 * np.pi * simps(pf * np.sin(arad), x=arad)  # Should be close to 4pi

    # Asymmetry parameter
    g = 1 - (np.log(2 * x) - 1) / x ** 2

    return pf / norm, g


def pf_bubbles_malinka_2017_psd(angles, verbose=False):
    """
    Mie simulation for air bubbles in sea ice with size distribution given by Light et al. 2010 (n(r) = r **-1.5, for
    r between 4 um and 70 um. The wavelength for calculation is 0.650 um and the relative refractive index 0.763.

    :param angles: scattering angles [degrees] - array
    :return: phase function normalized to 1, asymmetry param - tuple
    """
    # Air bubbles effective radius
    ra = np.linspace(4, 70, 500)  # microns, r_avg = 42.55 um

    ang_rad = angles * np.pi / 180
    mu = np.cos(ang_rad)

    # Refractive indexes # TODO: Update will refractive indexes of ice in litterature
    m = 0.763
    n_ice = 1.0 / m

    # Wavelength
    wave_rel = 0.650 / n_ice  # 650 nm

    # LOOP over all bubbles sizes
    pf = np.zeros((angles.shape[0], ra.shape[0]))
    qsc_mesh = pf.copy()
    g_arr = np.zeros(ra.shape[0])

    for i, r in enumerate(ra):

        # Size parameter
        x = 2 * np.pi * r / wave_rel

        # Mie calculation
        s1, s2 = miepython.mie_S1_S2(m, x, mu)
        qext, qsca, qback, g = miepython.mie(m, x)

        pf_unscaled = 0.5 * (abs(s1) ** 2 + abs(s2) ** 2) # should be normalized to albedo, in this case a = Qsca/Qext = 1

        pf[:, i] = pf_unscaled * qext / qsca
        qsc_mesh[:, i] = qsca
        g_arr[i] = g

        if verbose:
            print("Qext:{0}, Qsca = {1}, Qback = {2}, g = {3}".format(qext, qsca, qback, g))

    # Scaled by size distribution
    n = ra ** (-1.5)  # Size distribution - comes from Light et al. 2010
    n_mesh = np.tile(n, (angles.shape[0], 1))
    r_mesh = np.tile(ra, (angles.shape[0], 1))

    pf_avg = simps(np.pi * r_mesh ** 2 * qsc_mesh * pf * n_mesh, x=r_mesh, axis=1) / \
             simps(np.pi * r_mesh ** 2 * qsc_mesh * n_mesh, x=r_mesh, axis=1)

    g_avg = simps(np.pi * r_mesh[0, :] ** 2 * qsc_mesh[0, :] * g_arr * n_mesh[0, :], x=r_mesh[0, :]) / \
            simps(np.pi * r_mesh[0, :] ** 2 * qsc_mesh[0, :] * n_mesh[0, :], x=r_mesh[0, :])

    #print(g_avg)
    #plt.figure()
    #plt.plot(angles, pf_avg)
    #plt.gca().set_yscale("log")

    # Calculate normalization to 1
    norm = 2 * np.pi * simps(pf_avg * np.sin(ang_rad), x=ang_rad)

    return pf_avg / norm, g_avg


def sea_ice_pf_malinka_2017(angles, fraction_ratio=6e-3):
    """
    Phase function considering both air bubbles and brines as a function of the fraction ratio of volume concentration
    of air over brines.

    :param angles: scattering angles [degrees] - array
    :param fraction_ratio: fraction ratio of volume concentration - float
    :return: total phase function [1/sr]- array
    """
    ph_func_b, gb = pf_brines_malinka_2017(angles)
    ph_func_a, ga = pf_bubbles_malinka_2017_psd(angles)

    rb = 100
    ra = 42.55
    sa_over_sb = (rb / ra) * fraction_ratio

    sb_over_s = 1 / (1 + sa_over_sb)
    sa_over_s = 1 - sb_over_s

    pf_tot = sb_over_s * ph_func_b + sa_over_s * ph_func_a

    return pf_tot


if __name__ == "__main__":

    # Estimation of effective radius of size distribution of bubbles

    r_bubbles = np.linspace(4, 70, 500)  # microns
    N_bubbles = r_bubbles ** (-1.5)

    r_eff_bubbles = np.trapz((r_bubbles ** 3) * N_bubbles) / np.trapz((r_bubbles ** 2) * N_bubbles)  # effective radius - should be 42.55 microns

    # Brines PF
    a = np.linspace(0, 180, 1000)  # angles in degrees
    a_radians = a * np.pi / 180  # angles in radians

    pf_b, g_b = pf_brines_malinka_2017(a)
    g_b_calcu = calculate_asymmetry_g(a, pf_b)

    # Bubbles PF
    pf_a, g_a = pf_bubbles_malinka_2017_psd(a)

    # Figure
    fig1, ax1 = plt.subplots(1, 1)

    ax1.plot(a, pf_b, label="Brines")
    ax1.plot(a, pf_a, label="Bubbles")

    ax1.set_yscale("log")
    ax1.legend(loc="best")
    ax1.set_xlabel(r"Scattering angle $\theta$ [°]")
    ax1.set_ylabel(r"$p(\theta)$ [1/sr]")

    # Sea ice tot
    fig2, ax2 = plt.subplots(1, 1)
    fr = [0, 6e-3, 6e-2, 6e-1, np.inf]  # fraction ratio to loop

    for frac in fr:

        pf_tot = sea_ice_pf_malinka_2017(a, fraction_ratio=frac)
        ax2.plot(a, pf_tot * 4*np.pi, label="$C_{{a}}^{{v}} / C_{{b}}^{{v}}$={0}".format(frac))  # in Paper PF are normalized to 4pi

        print(2 * np.pi * simps(pf_tot * np.sin(a_radians), x=a_radians))

    ax2.set_ylim((0.0001, 10**6))
    ax2.set_xlim((0, 180))
    ax2.set_yscale("log")
    ax2.legend(loc="best")
    ax2.set_xlabel(r"Scattering angle $\theta$ [°]")
    ax2.set_ylabel(r"$p(\theta)$ [1/sr]")

    plt.show()
