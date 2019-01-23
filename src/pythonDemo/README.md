# Python

English | [中文](README_CN.md)

- [1. Introduction](#1-introduction)
- [2. Setting up the environment](#2-setting-up-the-environment)
- [3. Getting started](#3-getting-started)
    - [4.1. what's the Punica Suite](#41-whats-the-punica-suite)
    - [4.2. what's the Punica Box](#42-whats-the-punica-box)
    - [4.3. Unboxing the repository](#43-unboxing-the-repository)

## 1. Introduction

Welcome to ontology, a decentralized world is waiting for your. `hello-ontology` is an tutorial `python` project, it provide basic example about how to use `ontology-python-sdk` to interact with your smart contract in ontology blockchain.

## 2. Setting up the environment

There are a few technical requirements before we start. Please install the following:

- [python 3.7](https://www.python.org/downloads/release/python-370/)
- [git](https://git-scm.com/)

## 3. Getting started

### 4.1. what's the Punica Suite

Punica Suite is a Ontology dApp Development Framework, which has (almost) everything you need for Ontology dApp development.

Now, we have Punica CLI, Punica Box and Solo Chain in our Punica Suite. More powerful dApp development tools is on the road.

### 4.2. what's the Punica Box

In the past, when we wanted to begin developing on Ontology Blockchain, the first question we may ask is, "Where do I start?".

Now, we have a brief answer, “Start from Punica Box.”

Punica Box is an example Ontology application and/or boilerplate that puts complimentary tools and libraries into a single, easily-downloadable package. Every Punica Box comes with libraries and tools already preinstalled, code that uses those libraries and tools, external scripts (if necessary), as well as helpful `README` and documentation. All Punica Boxes are directly integrated into the Punica command line, and you need only type `punica unbox <box name>` to download and prepare your box of choice.

Before we begin a wonderful journey, ensure you've installed the latest version of Punica before opening your first box.

### 4.3. Unboxing the repository

Install Punica.

```shell
pip install punica
```

Download the `hello-python-box`.

```shell
punica init
```

Create virtual environments (optional).

```shell
virtualenv --no-site-packages venv
```

If you choose to create a virtual environment, you may need to activate your project's virtual environment.

```shell
.\venv\scripts\activate
```

Install the necessary dependencies.

```shellDemo
pip install -r requirements.txt
```