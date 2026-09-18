"""Лабораторийн орчин зөв тохируулагдсан эсэхийг шалгах smoke тест."""

import importlib
import sys

import pytest

REQUIRED_PACKAGES = ["numpy", "pandas", "matplotlib", "pytest", "ipykernel"]


def test_python_version():
    """Лаборатори Python 3.11+ шаарддаг."""
    assert sys.version_info >= (3, 11), f"Python 3.11+ шаардлагатай, одоо {sys.version_info}"


@pytest.mark.parametrize("package", REQUIRED_PACKAGES)
def test_package_importable(package):
    """Шаардлагатай сан бүр import хийгдэх ёстой."""
    assert importlib.import_module(package) is not None


def test_matplotlib_headless_backend():
    """Тест дотор график зурахад дэлгэц шаардахгүй backend ашиглана."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    plt.close(fig)
