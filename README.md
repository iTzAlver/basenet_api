# BaseNet: A simpler way to build AI models.

<p align="center">
    <img src="https://raw.githubusercontent.com/iTzAlver/basenet_api/main/doc/multimedia/basenet_logo.png" width="400px">
</p>

<p align="center">
    <a href="https://github.com/iTzAlver/basenet_api/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/iTzAlver/basenet_api?color=purple&style=plastic" /></a>
    <a href="https://github.com/iTzAlver/basenet_api/tree/main/test">
        <img src="https://img.shields.io/badge/tests-passed-green?color=green&style=plastic" /></a>
    <a href="https://github.com/iTzAlver/basenet_api/blob/main/requirements.txt">
        <img src="https://img.shields.io/badge/requirements-pypi-red?color=red&style=plastic" /></a>
    <a href="https://htmlpreview.github.io/?https://github.com/iTzAlver/basenet_api/blob/main/doc/basenet.html">
        <img src="https://img.shields.io/badge/doc-available-green?color=yellow&style=plastic" /></a>
    <a href="https://github.com/iTzAlver/BaseNet-API/releases/tag/1.5.0-release">
        <img src="https://img.shields.io/badge/release-1.5.0-white?color=white&style=plastic" /></a>
</p>

<p align="center">
    <a href="https://www.tensorflow.org/">
        <img src="https://img.shields.io/badge/dependencies-tensorflow-red?color=orange&style=for-the-badge" /></a>
    <a href="https://keras.io/">
        <img src="https://img.shields.io/badge/dependencies-keras-red?color=red&style=for-the-badge" /></a>
    <a href="https://www.ray.io/">
        <img src="https://img.shields.io/badge/dependencies-ray-red?color=blue&style=for-the-badge" /></a>
</p>

# Basenet API Package - 1.9.5:  (2.0.0 Is coming!!)

This package implements an API over Keras and Tensorflow to build Deep Learning models easily without losing the
framework flexibility. BaseNet API tries to implement almost everything from a few lines of code.

> **Disclaimer**: This API is under development. This means that there isn't a stable release yet.
> However, some features are stable and can be used. Check the tutorials for more info. 
> Please, check the roadmap below to see the future updates.

> Any feature request is wellcome and appreciated; and has a high probability to be implemented.

> Any issue is wellcome and appreciated; and it will often be inspected.

## About ##

    Author: A.Palomo-Alonso (a.palomo@uah.es)
    Universidad de Alcalá.
    Escuela Politécnica Superior.
    Departamento de Teoría De la Señal y Comunicaciones (TDSC).
    ISDEFE Chair of Research.

## Features

#### **MACHINE LEARNING**
* **Feature 01:** Database train, validation and test automatic and random segmentation for DeepLearning.
* **Feature 02:** Solving optimization problems for MetaHeuristic models.

#### **EFFICIENCY**
* **Feature 03:** Real multiprocessing training process (CPU usage optimization).
* **Feature 04:** Automatic and custom GPU usage and assignment.

#### **SIMPLICITY**
* **Feature 05:** Easy-to-use API.
* **Feature 06:** API documentation.
* **Feature 07:** JuPyter Notebooks tutorials included.
* **Feature 08:** Python Packaging and PyPi indexing.

#### **MONITORIZATION**
* **Feature 09:** Real-time logging.
* **Feature 10:** Dashboards included.
* **Feature 11:** Model printing and easy debugging.

#### **CONNECTIVITY**
* **Feature 12:** Model merging and multiple model inputs.
* **Feature 13:** Computational cluster linking.
* **Feature 14:** The different parts of the API are designed to interact.
* **Feature 15:** It allows to create dynamic databases for data ingestion and math problems that require synthetic data.

#### **RELIABILITY**
* **Feature 16:** Depends on huge and reliable frameworks: KERAS, TENSORFLOW, RAY.
* **Feature 17:** Code updating and active support.


### Cons:
#### **FLEXIBILITY**
* An API must look for a balance between simplicity and flexibility. In this case, we bet on simplicity; but the API
is still highly flexible.
* The API is designed for high level research and design. But it is not optimal for low-level research.

#### **DEPENDENCE**
* This API is built over highly reliable frameworks, however, the API depends on those frameworks to run the models.

#### **DEPLOYMENT**
* The API can not deploy models by itself yet in this current version. But I am planning!


### Roadmap:
#### Discipline coverage:
- [x] Database building.
- [x] Supervised learning.
- [x] MetaHeuristic optimization.
- [ ] Unsupervised learning. (Planning in 3.0 release)
- [ ] Reinforcement learning. (Planning in 4.0 release)
- [ ] Computer Vision. (Planning in 5.0 release)
- [ ] Natural Language Processing. (Will be in development from 3.0 to 6.0)

#### Feature roadmap:

- [x] Feeder databases.
- [x] Computational clustering.
- [x] Monitoring.


- [ ] BaseNetDeployment: 
  - Deploy your model in your infrastructure with high connectivity and scalability. 
  - With preprocess, model, postprocess and front-end sector.
  - Automatic workload balance (probably with ``Ray`` or ``Spark`` clusters).
  - Dynamic training after deployment. The model will still be learning from input data if desired.


- [ ] Reinforcement learning:
  - This will be hard to add in deployment.
  - Custom environments.
  - Connectivity with BaseNetCompiler: It will work with RL policy and DL!
  - State-of-the-art RL.


- [ ] Computer Vision:
  - It is already possible to be implemented in DeepLearning API; but can be improved.
  - Database visualization.
  - Database size optimization.
  - Computer vision utils.


- [ ] Natural Language Processing:
  - Hard to tell here, this discipline is very ad-hoc, and it is hard to pack it in an API.
  - Transformers, LSTM and Word Vectorization will be included.
  - Preprocessing will be a must.
  - Probably will use ``HuggingFace`` package.
  - Will be in constant development.


## What's new?

### < 0.1.0
1. BaseNetModel included.
2. BaseNetDatabase included.
3. BaseNetCompiler included.
4. Inheritance from CorNetAPI project.
5. Multi-processing fitting.
6. Tensorboard launching.

### 0.2.0
1. BaseNetResults included (working).
2. Now the model is callable.
3. Switched print to logging.
4. Project documentation.


### 1.0.0 - 1.0.3
1. Python packaging
3. 1.0.x: Upload bug solving.

### 1.1.0
1. Functional package.
2. PyPi indexing.

### 1.2.0:
1. Loss results included in the BaseNetResults while multiprocessing.
2. GPU auto set up to avoid TensorFlow memory errors.
3. Method ``BaseNetCompiler.set_up_devices()`` configures the GPUs according to the free RAM to be used in the API.

### 1.3.0
1. Included WindowDiff to the project scope.

### 1.4.0
1. Solved python packaging problems.
2. Included force stop callback in the ```BaseNetModel.fit_stop()``` method.

### 1.5.0
1. BaseNetDatabase now has the attributes ``BaseNetDatabase.size`` and ``BaseNetDatabase.distribution``.
2. Solved forced stopping bugs with multiprocessing in the method ``BaseNetDatabase.fit_stop()``.
3. ```BaseNetModel._threshold()``` private method now takes a set of outputs instead only one. 
This was only for optimization.
4. Solved wrong ```BaseNetModel.recover()```.
5. **Auto recover implemented**, now ```BaseNetModel.recover()``` is a private method: ```BaseNetModel._recover()```.
Now the used does not need to recover it. *The model recovers by itself. -- Hans Niemann 2022.* 
**NOTE**: RECOVER IS NECESARY WHEN THE MODEL IS EARLY STOPPED; CONSIDER RECOVERING ALWAYS THE MODEL.

### 1.5.1 - 1.5.3
1. Solved a bug where ``BaseNetDatabase`` modified the incoming list of instances in the database; avoiding checkpoints
for large database generators.
2. Exception handler for ``nvml`` library if NVIDIA Drivers are not installed`in the machine.

### 1.5.4
1. Added some ``BaseNetDatabase`` utils: merge and split databases.
2. Added ``BaseNetDatabase`` equality check.
3. Added a ``BaseNetDatabase._reversion()``, ``BaseNetCompiler._reversion()`` and ``BaseNetModel.__version__``. Which
rebuilds the Classes to the current version of the API.

### 1.6.0
1. Start to develop the second branch of the API: ``BaseNetHeuristic``
2. Start to create JuPyter Notebook tutorials of the API.
3. Included ``BaseNetDatabase`` binarization and normalization of databases.
4. Included in ``BaseNetDatabase`` to read ``TensorFlow`` and ``Pandas`` databases.
5. Some rework was done for bug-fixing and providing more logging information.

### 1.7.0 - 1.9.1
1. Reworked ``BaseNetDatabase`` for minor bug fixing. (1.7.0)
2. Added the ``BaseNetFeeder`` Class to generate dynamic ``BaseNetDatabase``s. (1.7.0)
3. Jupyter tutorials. (1.8.0)
4. Added the ``BaseNetDeployment`` Class to deploy scalable Machine Learning models (in alpha, do not use until 3.0).
(1.9.0)
5. Added ``BaseNetHeuristic`` algorithms that implements MetaHeuristic methods such as PSO. (1.8.0)

### 1.9.2
1. Added ``BaseNetLMSE``, solving linear problems with matrix multiplication.

### 1.9.3 - 1.9.5
1. Added ``CassandraDatabase``.
2. Added ``categorical`` entry to ``compile_options`` in the ``BaseNetCompiler``. 
This allows the user to build a classifier in the DeepLearning module. By default, it is a regression model.
3. Added a minimum of 1 GPU in ``BaseNetCompiler.set_up_devices()``
4. Added the output mapping function to the ``BaseNetDatabase`` as ``.define_map()`` and the mapping method ``map()``.
5. Added the attribute ``shape`` to the ``BaseNetDatabase`` telling the input-output data shapes.
6. Added Fuzzy-Logic feature in ``BaseNetDatabase`` for Fuzzy-Logic mapping.
7. Added `BaseNetCVVisualizer` and ``basenet_cv_gui`` for computer vision dataset and results visualization.
8. Added `BaseNetStackRoom`, which is a Database manager for big databases.

### 1.9.6
1. Added multi-block to ``BaseNetCompiler`` so it can be built from several YAML files.


## Basic and fast usage

There are Jupyter Notebooks with usage tutorials! Refer to them 
[HERE](https://github.com/iTzAlver/BaseNet-API/tree/main/jupyter). You should run your notebook creating a 
virtual environment in this README path.

### Cite as

Please, cite this library as:


    @misc{basenetapi,
      title={BaseNet: A simpler way to build AI models.},
      author={A. Palomo-Alonso},
      booktitle={PhD in TIC: Machine Learning and NLP.},
      year={2022}
    }
