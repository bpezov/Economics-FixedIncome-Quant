import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define the SolowModel class to encapsulate model parameters and methods.
class SolowModel:
    def __init__(self, s, delta, n, g, alpha):
        """
        Initialize the Solow model with given parameters.
        
        Parameters:
            s (float): Savings rate.
            delta (float): Depreciation rate.
            n (float): Population growth rate.
            g (float): Technological growth rate.
            alpha (float): Capital share in the production function (Cobb-Douglas).
        """
        self.s = s
        self.delta = delta
        self.n = n
        self.g = g
        self.alpha = alpha
        # Combined rate representing the dilution of capital
        self.lambda_factor = self.n + self.g + self.delta

    def production(self, k):
        """
        Production function f(k) = k^alpha.
        
        Parameters:
            k (float or np.array): Capital per effective worker.
            
        Returns:
            float or np.array: Output per effective worker.
        """
        return k ** self.alpha

    def capital_accumulation(self, k):
        """
        Computes the time derivative of capital per effective worker:
          dk/dt = s*f(k) - (n + g + delta)*k
        
        Parameters:
            k (float): The capital per effective worker.
            
        Returns:
            float: The rate of change of capital per effective worker.
        """
        return self.s * self.production(k) - self.lambda_factor * k

    def steady_state(self):
        """
        Computes the steady-state value of capital per effective worker (k*).
        
        Returns:
            float: Steady-state capital per effective worker.
        """
        return (self.s / self.lambda_factor) ** (1 / (1 - self.alpha))

    def plot_phase_data(self, k_values):
        """
        Generates data for the investment function and the break-even investment line.
        
        Parameters:
            k_values (np.array): Array of capital per effective worker values.
            
        Returns:
            tuple: Two arrays for s*f(k) and (n+g+delta)*k.
        """
        invest = self.s * self.production(k_values)
        break_even = self.lambda_factor * k_values
        return invest, break_even

# Function to create an interactive phase diagram using Matplotlib sliders.
def interactive_phase_diagram():
    # Initial parameter values
    s0 = 0.3
    delta0 = 0.05
    n0 = 0.02
    g0 = 0.02
    alpha0 = 0.33
    k_values = np.linspace(0, 10, 300)

    # Instantiate the model with initial values.
    model = SolowModel(s0, delta0, n0, g0, alpha0)
    invest, break_even = model.plot_phase_data(k_values)
    
    # Create a Matplotlib figure and axis.
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.25, bottom=0.35)  # Leave space for sliders

    # Plot the initial investment and break-even lines.
    invest_line, = ax.plot(k_values, invest, label='s * f(k)')
    break_even_line, = ax.plot(k_values, break_even, label='(n+g+δ)*k')
    
    # Calculate and plot the steady state line.
    steady_state_value = model.steady_state()
    # Use a list to store the line so it can be replaced later.
    steady_state_line_obj = [ax.axvline(steady_state_value, color='red', linestyle='--', 
                                          label=f'Steady State k* = {steady_state_value:.2f}')]
    
    ax.set_xlabel('Capital per effective worker (k)')
    ax.set_ylabel('Rate of Change')
    ax.set_title('Phase Diagram of the Solow Growth Model')
    ax.legend()
    ax.grid(True)

    # Define positions for slider axes.
    axcolor = 'lightgoldenrodyellow'
    ax_s = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
    ax_delta = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
    ax_n = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    ax_g = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
    ax_alpha = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

    # Create sliders for each parameter.
    s_slider = Slider(ax_s, 'Savings rate s', 0.0, 1.0, valinit=s0, valstep=0.01)
    delta_slider = Slider(ax_delta, 'Depreciation δ', 0.0, 0.2, valinit=delta0, valstep=0.001)
    n_slider = Slider(ax_n, 'Population growth n', 0.0, 0.1, valinit=n0, valstep=0.001)
    g_slider = Slider(ax_g, 'Tech growth g', 0.0, 0.1, valinit=g0, valstep=0.001)
    alpha_slider = Slider(ax_alpha, 'Capital share α', 0.1, 0.9, valinit=alpha0, valstep=0.01)

    # Define an update function that recalculates and redraws the plot when sliders are moved.
    def update(val):
        # Retrieve current slider values.
        s = s_slider.val
        delta = delta_slider.val
        n = n_slider.val
        g = g_slider.val
        alpha = alpha_slider.val

        # Create a new model instance with updated parameters.
        new_model = SolowModel(s, delta, n, g, alpha)
        invest_new, break_even_new = new_model.plot_phase_data(k_values)
        
        # Update the plotted data for the investment and break-even lines.
        invest_line.set_ydata(invest_new)
        break_even_line.set_ydata(break_even_new)
        
        # Update the steady state line:
        steady_state = new_model.steady_state()
        # Remove the old vertical line.
        steady_state_line_obj[0].remove()
        # Create a new vertical line at the updated steady state.
        steady_state_line_obj[0] = ax.axvline(steady_state, color='red', linestyle='--', 
                                              label=f'Steady State k* = {steady_state:.2f}')
        
        # Update the legend to reflect new steady state value.
        ax.legend()
        # Redraw the figure to show updates.
        fig.canvas.draw_idle()

    # Connect each slider to the update function.
    s_slider.on_changed(update)
    delta_slider.on_changed(update)
    n_slider.on_changed(update)
    g_slider.on_changed(update)
    alpha_slider.on_changed(update)

    plt.show()

# Run the interactive phase diagram in Spyder.
interactive_phase_diagram()
