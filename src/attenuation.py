import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

########## SCRIPT 4 LATEX #####
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Helvetica"
})

exponent = -2.75
material = "Lead"

def func(x, a, b):
    return a + b * x ** (exponent)

#def func(x, a, b):
#    return a + b * np.exp(-x)

def analyze_attenuation(data_file, output_image, photon_energy):
    # Load data
    data = np.loadtxt("../data/"+material + "_" + data_file, 
                      #delimiter='\t'
                      )
    energy = data[:, 0]*1000 #energy in keV
    attenuation = data[:, 1] #attenuation/density in cm^2/g

    popt, pcov = curve_fit(func, energy, attenuation, 
                           p0=(0, 10)
                           )
    a_fit, b_fit = popt

    # Print fitted parameters
    coeff = func(photon_energy, a_fit, b_fit)
    print(f'Mass Attenuation coefficient of Lead at {photon_energy} keV: {coeff} cm^2/g')

    # Generate fitted values for plotting
    energy_fit = np.linspace(min(energy), max(energy), 100)
    fitted_func = func(energy_fit, a_fit, b_fit)

    # Plot the data and the fitted curve
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(energy, attenuation, label='Measured Data', color='blue')
    ax.plot(energy_fit, fitted_func, label=r'Fit $\propto E_\gamma^{-2.75}$', color='red')
    ax.set_title("Mass attenuation coefficient for " + material)
    ax.set_xlabel(r"Photon Energy $E_\gamma$ (keV)")
    ax.set_ylabel(r"$\frac{\mu}{\rho}$ (cm$^2$/g)")
    #ax.set_yscale('log')
    ax.legend()
    ax.grid()
    line, = ax.plot(photon_energy, coeff, color='#ee8d18', lw=2)
    ax.annotate('({photon_energy} keV, {coeff:.2f} cm$^2$/g)'.format(photon_energy=photon_energy, coeff=coeff),
            xy=(photon_energy, coeff),  # positions
            xytext=(0.5, 0.5),    # fraction, fraction
            textcoords='figure fraction',
            fontsize=14,
            arrowprops=dict(facecolor='black', shrink=0.07, width=0.8, headwidth=5),
            horizontalalignment='left',
            verticalalignment='top',
            )
    # 'D' indica un marker a diamante
    ax.plot(photon_energy, coeff, marker='D', markersize=6, color='green')
    fig.savefig("../plots/"+output_image)
    fig.show()

energy = 120 # keV
#energy_peak = 57.98 # keV
#analyze_attenuation("attenuation_data.txt", "attenuation_plot.png", energy)
analyze_attenuation("attenuation_data.txt", material + "_attenuation_data_plot.png", energy)