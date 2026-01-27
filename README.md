# ebc-fridge-prod-sim
Project for course on Event Base Control at Wroclaw University of Science and Technology. The project is a visualization app the serves the role of scheduler and visualizer of tasks needed to create fridges in factory using Discrete Event System (DES) and Petri Nets

## Instalation

To run application first make sure that you have `Poetry` and `Python3.10`.
Then use below commands:

```shell
$ make setup-env
$ poetry env activate
(venv) $ poetry run make run
```

## Ruff

To run ruff check and ruff fix

```shell
(venv) $ make ruff_check
(venv) $ make ruff_fix
```
