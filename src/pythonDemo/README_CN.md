# Hello Ontology

[English](README.md) | 中文

- [1. 简介](#1-简介)
- [2. 配置开发环境](#2-配置开发环境)
- [3. 快速开始](#3-快速开始)
    - [3.1. 什么是 Punica Suite？](#31-什么是-punica-suite)
    - [3.2. 什么是 Punica Box？](#32-什么是-punica-box)
    - [3.3. 下载项目库](#33-下载项目库)

## 1. 简介

欢迎来到本体，一个去中心化的世界正在等待着你。 `hello-ontology` 是一个教程性的 `python` 项目，它提供了有关如何使 用`ontology-python-sdk` 与本体区块链中的智能合约进行交互的基本示例。

## 2. 配置开发环境

在我们开始之前，有一些技术要求。 请安装以下内容：

- [python 3.7](https://www.python.org/downloads/release/python-370/)
- [git](https://git-scm.com/)

## 3. 快速开始

### 3.1. 什么是 Punica Suite？

Punica Suite 是一个本体 dApp 开发框架，它（几乎）具有开发本体 dApp 所需的一切。

现在，我们的 Punica Suite 中有 Punica CLI、Punica Box和Solo Chain。更强大的dApp开发工具正在开发中。

### 3.2. 什么是 Punica Box？

在过去，当我们想要开始使用本体区块链的时候，我们可能会问的第一个问题是：“我从哪里开始？”。

现在，我们有一个简明的回答：“从 Punica Box 开始。“

Punica Box 是示例性本体应用程序和样板文件的集合，它将免费的工具和库放入到一个易于下载的软件包之中。每个 Punica Box 都附带已经预装的库和工具，使用这些库和工具的代码、外部脚本（如果需要）以及有用的 `README` 和文档。所有 Punica Box 都集成到了 Punica 命令行中，你只需要输入 `punica unbox <box name>` 即可直接下载。

在我们开始一段美妙的旅程之前，请确保在打开第一个 box 之前已经安装了最新版本的 Punica。

### 3.3. 下载项目库

安装 Punica。

```shell
pip install punica
```

下载 `hello-python-box`。

```shell
punica init
```

创建虚拟环境（可选的）。

```shell
virtualenv --no-site-packages venv
```

如果你选择创建虚拟环境，你也许需要去激活你项目中的虚拟环境。

```shell
.\venv\scripts\activate
```

安装必要的依赖文件。


```shell
pip install -r requirements.txt
```