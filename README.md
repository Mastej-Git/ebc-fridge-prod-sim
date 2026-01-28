# ebc-fridge-prod-sim
Project for course on Event Base Control at Wroclaw University of Science and Technology. The project is a visualization app the serves the role of scheduler and visualizer of tasks needed to create fridges in factory using Discrete Event System (DES) and Petri Nets

## Instalation

To run application first make sure that you have `Poetry (version 2.2.0)` and `Python3.10 (or higher)`.
Then use the application below commands:

```shell
$ git clone https://github.com/Mastej-Git/ebc-fridge-prod-sim.git
$ make setup-env 
$ poetry env activate
(venv) $ make run
```

## Ruff

To run ruff check and ruff fix

```shell
(venv) $ make ruff_check
(venv) $ make ruff_fix
```
