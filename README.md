<div align="center">
      <img src="./logo.webp" width="40%">
</div>

<h1 align="center">PyPi server</h1>

<p align="center">
Private PyPi packages index
</p>

---

<p align="center">
  <a href="#description">Description</a> •
  <a href="#usage">Usage</a> •
  <a href="#references">References</a>
</p>

---


## Description

This repository is a Github page used as a PyPi index, conform to [PEP503](https://www.python.org/dev/peps/pep-0503/).

You can use it to group all your packages in one place, and access it easily through `pip`, almost like any other package publicly available !

---

_While the PyPi index is public, private packages indexed here are kept private : you will need Github authentication to be able to retrieve it._

## Usage


***Install the package `sample-package`:***

```sh
alias python=python3 # on macOS/Linux

python -m pip install sample-package --extra-index-url https://pypkghub.github.io/PyIndexServer/packages/ # first insatllation

python -m pip install sample-package --upgrade --extra-index-url https://pypkghub.github.io/PyIndexServer/packages/ # upgrade
```

_It will also install all depencies packages automatically !_


***Install a specific version***

```sh
alias python=python3 # on macOS/Linux

python -m pip install sample-package==0.1 --extra-index-url https://pypkghub.github.io/PyIndexServer/packages/ # first insatllation
```

***Example of requirements.txt:***

--extra-index-url `https://pypkghub.github.io/PyIndexServer/packages/`
sample-package==0.1

---

## Useful links & Credits ✨
- [github-hosted-pypi](https://github.com/astariul/github-hosted-pypi)

---