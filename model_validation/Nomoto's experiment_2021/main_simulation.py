from model import ReceptorModel
import plot_experimental_conditions as condition
df = condition.df
print(df)


# input_normalized_radiation_spectrum = config.INPUT_SPECTRUM_PATH
# print(input_normalized_radiation_spectrum)

model = ReceptorModel()
model.t_core = 34
# model.q_spectrum =
model.add_phase(duration=100, t_db=25, t_r=25, q_irradiance=0)
model.add_phase(duration=20, t_db=25, t_r=25, q_irradiance=100)
simulation_results = model.simulate()
print(simulation_results)