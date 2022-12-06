# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import logging
import time

import tensorflow as tf
from abc import abstractmethod
from src.baseneth.basis.constraints import HeuristicConstraints
from src.baseneth.basis.computational_scope import ComputationalScope
from src.baseneth.basis.basic_evolutive import random_initializer, basic_mutation, elitist_selection

from src.baseneth.basis.dashboard import Dashboard


# -----------------------------------------------------------
class BaseNetHeuristic:
    def __init__(self, fitness_function, number_of_individuals: int = 0, new_individuals_per_epoch: int = 0,
                 ray_ip: str = None, runtime_env: dict = None, computational_cores: int = 10, dashboard=1):
        """
        The BaseNetHeuristic abstract class is a layout to build your own Heuristic Models.
        :param fitness_function: A fitness function with the following format:
            fitness_function(*args, **kwargs) -> tf.Tensor or np.array or list[list] with MxN shape. Where M is the
            number of individuals and N is the number of parameters. The *args contains the individuals and the function
            must return an M dimensional vector with the fitness function, always to be MAXIMIZED.
        :param number_of_individuals: Number of individuals (M) in the Heuristic.
        :param new_individuals_per_epoch: New individuals to be introduced in the Heuristic.
        :param ray_ip: An IP for a RAY cluster. Check RAY documentation for more information.
        :param runtime_env: A runtime environment for the RAY workers. Check RAY documentation for more information.
        :param computational_cores: The number of cores to be used among the cluster and the cores of the user machine.
        :param dashboard: The number of epoch between a dashboard update. Select 0 for not displaying the dashboard.
        """
        self.extra_plots = []
        self.constraints: HeuristicConstraints = HeuristicConstraints()
        self.number_of_individuals: int = number_of_individuals
        self.new_individuals_per_epoch: int = new_individuals_per_epoch
        self.population: (tf.Tensor, None) = None
        self.score: (tf.Tensor, None) = None
        self.ray: tuple = (ray_ip, runtime_env, computational_cores)
        if fitness_function is not None:
            self.fitness = fitness_function
        else:
            raise ValueError('Fitness function must be defined; not None. You can change it via: '
                             'BaseNet<Heuristic>.fitness = new_fitness_function')
        if dashboard:
            self.there_is_dashboard: bool = True
        else:
            self.there_is_dashboard: bool = False
        self.each_dashboard = dashboard - 1
        self.dashboard = None

    def add_parameter(self, parameter_type: str = 'real', minimum: any = 0, maximum: any = 0):
        """
        This method adds a new parameter into the problem scope.
        :param parameter_type: The type of the parameter (real, integer or categorical) selects the behavior of the
        parameter. Categorical and integer values are treated as integers, however the categorical have a forced minimum
         at 0.
        :param minimum: Minimum value of the parameter.
        :param maximum: Maximum value of the parameter.
        :return: Self of the object.
        """
        self.constraints.add_parameter(parameter_type, minimum, maximum)
        return self

    def add_rule(self, conditioned: list[int], conditions: list[int], operator):
        """
        This method adds a new rule into the problem scope.
        :param conditioned: The index of the conditioned parameters.
        :param conditions: The index of the condition parameters.
        :param operator: An user-defined function with the following format:
            operator(conditioned, conditions) -> bool. Check that the conditioned parameters follow the rule according
            to the condition parameters. I.E: The following function checks if the conditioned parameter is the greatest
            among the condition parameters.\n
            def check_if_max_operator(conditioned: list, conditions: list): \n
                for condition in conditions: \n
                    if conditioned[0] < condition: \n
                        return False \n
                return True \n
            my_heuristic_with_10_parameters.add_rule([4], [0, 1, 2, 3, 5, 6, 7, 8, 9], check_if_max_operator)
        :return: Self of the object.
        """
        self.constraints.add_rule(conditioned, conditions, operator)
        return self

    def fit(self, epoch: int, objective=None, callback=None):
        """
        This is the fit method, call it to start the training process of the MetaHeuristic.
        :param epoch: Number of epoch to run the MetaHeuristic.
        :param objective: Objective fitness value, the fit will stop when an individual reaches this value.
        Select 'None' to ignore this feature.
        :param callback: A callback function that is called at the end of the epoch with the following format:\n
        def my_callback(epoch_number, population: tf.Tensor, score: tf.Tensor) -> bool:\n
            [...] \n
            return True \n
        The population is a MxN shape matrix, and the score is an M dimensional vector. (M is the number of individuals
        and N is the number of the parameters).\n
        If it returns True, it allows the fit method to keep working. If False, it stops the fitting method.
        :return: The trained population, the fitness score according to the population.
        """
        with ComputationalScope(self.ray[0], self.ray[1]) as cscope:
            with Dashboard(self.constraints, self.extra_plots, cscope, cnt=self.each_dashboard) as self.dashboard:
                #
                #   Initialization.
                #
                cscope.bind(self.fitness)
                self.population = self._initializer_(self.number_of_individuals, self.constraints)
                self.population = self.constraints.apply_bindings(self.population)
                for epoch_number in range(epoch):
                    performance = {'fitness': 0, 'crossover': 0, 'selection': 0}
                    tik = time.time()
                    #
                    #   Get the fitness function and sort in descending order.
                    #
                    divs = self._divide(self.population, self.ray[2])   # Divide into computational segments.
                    cscope.run(divs)                                    # Run the computational segments.
                    futures = self._collapse(cscope.get())              # Obtain and collapse the results.
                    self.score = self._idiot_proof_futures(futures)     # Some idiot proofing of the fitness function.
                    self.population, self.score = self._sort()          # Sort the individuals according to their score.
                    tak = time.time()                                   # Tik-toc.
                    performance['fitness'] = tak - tik                  # Performance store.
                    #
                    #   Crossover.
                    #
                    new_individuals = self.constraints.apply_bindings(self._crossover_(self.population))    # New pop.
                    disrespectful = self.constraints.check_constraints(new_individuals)                     # Rules.
                    while disrespectful:                                        # While the rules are not respected...
                        new = self._crossover_(self.population)                 # New individuals.
                        new_individuals = self.constraints.apply_bindings(new)  # Apply constraints (min, max, type).
                        disrespectful = self.constraints.check_constraints(new_individuals)  # Who does not respect?
                        [...]
                    tik = time.time()                                   # Tik-toc.
                    performance['crossover'] = tik - tak                # Performance store.
                    #
                    #   Selection.
                    #
                    self.population = self._selection_(self.population, new_individuals)    # Selection in the pop.
                    tak = time.time()                                                       # Tik-tok.
                    performance['selection'] = tak - tik                                    # Performance store.
                    #
                    #   Additional actions per epoch:
                    #
                    #   Callback.
                    #
                    if callback is not None:
                        if not callback(epoch_number, self.population, self.score):
                            break
                    #   Dashboard.
                    #
                    if self.there_is_dashboard:
                        self.dashboard.add(self.score, self.population, performance)
                        self.dashboard.refresh_tab()
                    #      Objective check.
                    #
                    if objective is not None:
                        if max(self.score) >= objective:
                            logging.info(f'The objective {objective} was achieved in epoch {epoch_number}.')
                            break
        return self.population, self.score

    def add_plot(self, plot_function, name='User plot'):
        """
        This method adds a plot_function to the Dashboard.
        :param plot_function: The plot function with type: plt_function(individuals) where individuals must have a
        MxN shape, where M are the number of individuals and N are the number of parameters. This function must return
        a plot. The function must have the following format:\n
        def my_plot(pp: pd.DataFrame, selector_individual: int, selector_epoch: str) -> An hvplot: \n
            [...]\n
        Where selector_individual is a value for the selector slider and selector_epoch is the epoch
        for the epoch selector slider.
        :param name: Name of the to be shown in the dashboard.
        :return: Self from the object.
        """
        self.extra_plots.append((plot_function, name))
        return self
    """
    This are the private methods of the Heuristic Model.
    """
    def _sort(self) -> tuple[tf.Tensor, tf.Tensor]:
        indices = tf.argsort(self.score, direction='DESCENDING')
        pop = tf.gather(self.population, indices)
        return pop, tf.sort(self.score, direction='DESCENDING')

    @staticmethod
    def _divide(population: tf.Tensor, divisions: int):
        individuals_per_division = round(len(population) / divisions)
        divs = list()
        for index in range(divisions - 1):
            divs.append(population[index * individuals_per_division:(index + 1) * individuals_per_division].numpy())
        divs.append(population[(divisions - 1) * individuals_per_division:].numpy())
        return divs

    @staticmethod
    def _collapse(futures):
        collapsed = list()
        for future in futures:
            collapsed.extend(future)
        return tf.convert_to_tensor(collapsed)
    """
    This are the idiot-proof wrappers for the abstract functions.
    """
    def _initializer_(self, number_of_individuals, constraints):
        try:
            _return_value_ = self.initializer(number_of_individuals, constraints)
            if len(_return_value_) == self.number_of_individuals:
                if len(_return_value_[0]) != len(self.constraints.parameters):
                    logging.warning(f'Idiot-Proof-Warning: Your initializer does not return '
                                    f'{len(self.constraints.parameters)} parameters per individual, it returns '
                                    f'{len(_return_value_[0])} parameters per individual. Fix your initializer.')
            else:
                logging.warning(f'Idiot-Proof-Warning: Your initializer does not return {number_of_individuals} '
                                f'individuals, it returns {len(_return_value_)} individuals. Fix your initializer.')
            if constraints.check_constraints(_return_value_):
                logging.warning(f'Idiot-Proof-Warning: Your initializer does not respect the constraints of the problem'
                                f'. Check your rules and your initializer.')
            if isinstance(_return_value_, tf.Tensor):
                return _return_value_
            else:
                logging.warning(f'Idiot-Proof-Comment: Your initializer does not return a tf.Tensor as a population. It'
                                f' returns a "{type(_return_value_)}" type. I am trying to convert it to "tf.Tensor".')
                return tf.convert_to_tensor(_return_value_)
        except Exception as ex:
            logging.error(f'An exception raised from the initializer method: {ex}.')
            raise ex

    def _crossover_(self, population: tf.Tensor):
        try:
            _return_value_ = self.crossover(self.new_individuals_per_epoch, population)
            if len(_return_value_) == self.new_individuals_per_epoch:
                if len(_return_value_[0]) != len(self.constraints.parameters):
                    logging.warning(f'Idiot-Proof-Warning: Your crossover method does not return '
                                    f'{len(self.constraints.parameters)} parameters per individual, it returns '
                                    f'{len(_return_value_[0])} parameters per individual. Fix your crossover.')
            else:
                logging.warning(f'Idiot-Proof-Warning: Your crossover method does not return '
                                f'{self.new_individuals_per_epoch} individuals, it returns {len(_return_value_)} '
                                f'individuals. Fix your crossover.')
            if isinstance(_return_value_, tf.Tensor):
                return _return_value_
            else:
                logging.warning(f'Idiot-Proof-Comment: Your crossover method does not return a tf.Tensor as a '
                                f'population. It'
                                f' returns a "{type(_return_value_)}" type. I am trying to convert it to "tf.Tensor".')
                return tf.convert_to_tensor(_return_value_)
        except Exception as ex:
            logging.error(f'An exception raised from the crossover method: {ex}.')
            raise ex

    def _selection_(self, population: tf.Tensor, new_individuals: tf.Tensor):
        try:
            _return_value_ = self.selection(new_individuals, population)
            if len(_return_value_) == len(population):
                if len(_return_value_[0]) != len(self.constraints.parameters):
                    logging.warning(f'Idiot-Proof-Warning: Your selection method does not return '
                                    f'{len(self.constraints.parameters)} parameters per individual, it returns '
                                    f'{len(_return_value_[0])} parameters per individual. Fix your selection.')
            else:
                logging.warning(f'Idiot-Proof-Warning: Your selection method does not return '
                                f'{len(population)} individuals, it returns {len(_return_value_)} '
                                f'individuals. Fix your selection.')
            if isinstance(_return_value_, tf.Tensor):
                return _return_value_
            else:
                logging.warning(f'Idiot-Proof-Comment: Your selection method does not return a tf.Tensor as a '
                                f'population. It'
                                f' returns a "{type(_return_value_)}" type. I am trying to convert it to "tf.Tensor".')
                return tf.convert_to_tensor(_return_value_)
        except Exception as ex:
            logging.error(f'An exception raised from the selection method: {ex}.')
            raise ex

    def _idiot_proof_futures(self, futures_values):
        _return_value_ = tf.convert_to_tensor(futures_values)
        if len(_return_value_) != len(self.population):
            logging.warning(f'Idiot-Proof-Warning: Your fitness method does not return '
                            f'{len(self.population)} values, it returns '
                            f'{len(_return_value_)} values and it should return one value per individual. '
                            f'Fix your fitness.')
        return _return_value_

    @staticmethod
    @abstractmethod
    def initializer(number_of_individuals: int, constraints: HeuristicConstraints) -> tf.Tensor:
        return random_initializer(number_of_individuals, constraints)

    @staticmethod
    @abstractmethod
    def crossover(number_of_new_individuals: int, population: tf.Tensor) -> tf.Tensor:
        return basic_mutation(number_of_new_individuals, population)

    @staticmethod
    @abstractmethod
    def selection(new_individuals: tf.Tensor, population: tf.Tensor) -> tf.Tensor:
        return elitist_selection(new_individuals, population)
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
