# -*- coding: utf-8 -*-

__author__ = 'Ilya Shoshin'
__copyright__ = 'Copyright 2015, Ilya Shoshin'

import numpy as np

def MD(original, modified):
    """
    Максимальная разность
    """
    diff = np.absolute(np.subtract(original, modified))
    return np.amax(diff)

def AD(original, modified):
    """
    Средняя абсолютная разность
    """
    n = len(original)
    diff = np.absolute(np.subtract(original, modified))
    return np.sum(diff) / float(n)

def NAD(original, modified):
    """
    Нормированная средняя абсолютная разность
    """
    diff = np.absolute(np.subtract(original, modified))
    sum1 = np.sum(diff)
    sum2 = np.sum(np.absolute(original))
    return sum1 / float(sum2)

def MSE(original, modified):
    """
    Среднеквадратическая ошибка
    """
    n = len(original)
    diff = np.subtract(original, modified)
    diff **= 2
    return np.sum(diff) / float(n)

def NMSE(original, modified):
    """
    Нормированная среднеквадратическая ошибка
    """
    orig = np.array(original, dtype=np.int32)
    orig **= 2
    sum1 = np.sum(orig)

    diff = np.subtract(original, modified)
    diff **= 2
    sum2 = np.sum(diff)

    return sum2 / float(sum1)

def LpNorm(original, modified, p):
    """
    Lp - норма
    """
    n = len(original)
    diff = np.absolute(np.subtract(original, modified))
    diff = np.power(diff, p)
    s = np.sum(diff)
    return np.power(s / float(n), 1.0 / p)


def SNR(original, modified):
    """
    Отношение сигнал/шум
    """
    orig = np.array(original, dtype=np.int32)
    orig **= 2
    sum1 = np.sum(orig)

    diff = np.subtract(original, modified)
    diff **= 2
    sum2 = np.sum(diff)

    return sum1 / sum2

def PSNR(original, modified):
    """
    Максимальное отношение сигнал/шум
    """
    n = len(original)
    orig = np.array(original, dtype=np.int32)
    orig **= 2
    m = np.amax(orig)

    diff = np.subtract(original, modified)
    diff **= 2
    sum2 = np.sum(diff)

    return n * m / sum2

def AF(original, modified):
    """
    Качество звучания
    """
    return 1 - NMSE(original, modified)

def NC(original, modified):
    """
    Нормированная взаимная корреляция
    """

    multiply = np.multiply(original, modified)
    sum1 = np.sum(multiply)

    orig = np.array(original, dtype=np.int32)
    orig **= 2
    sum2 = np.sum(orig)

    return sum1 / float(sum2)

def CQ(original, modified):
    """
    Качество корреляции
    """
    multiply = np.multiply(original, modified)
    sum1 = np.sum(multiply)

    orig = np.array(original, dtype=np.int32)
    sum2 = np.sum(orig)

    return sum1 / float(sum2)

def SC(original, modified):
    """
    Структурное содержание
    """
    orig = np.array(original, dtype=np.int32)
    orig **= 2
    sum1 = np.sum(orig)

    mod = np.array(modified, dtype=np.int32)
    mod **= 2
    sum2 = np.sum(mod)

    return sum1 / float(sum2)

def all(original, modified, p=2):

    n = len(original)
    adiff = np.absolute(np.subtract(original, modified))
    md = np.amax(adiff)

    ad = np.sum(adiff) / float(n)
    sum1 = np.sum(adiff)
    sum2 = np.sum(np.absolute(original))
    nad = sum1 / float(sum2)

    diff = np.subtract(original, modified)
    diff_2 = diff ** 2
    sum_diff_2 = np.sum(diff_2)
    mse = sum_diff_2 / float(n)

    orig = np.array(original, dtype=np.int32)
    orig_2 = orig ** 2
    sum_orig_2 = np.sum(orig_2)

    nmse = sum_diff_2 / float(sum_orig_2)

    adiff_p = np.power(adiff, p)
    sum_adiff_p = np.sum(adiff_p)
    lp = np.power(sum_adiff_p / float(n), 1.0 / p)

    snr = sum_orig_2 / sum_diff_2

    amax_orig_2 = np.amax(orig_2)

    psnr = n * amax_orig_2 / sum_diff_2

    af = 1 - nmse

    multiply = np.multiply(original, modified)
    sum_mult = np.sum(multiply)

    nc = sum_mult / float(sum_orig_2)

    sum_orig = np.sum(orig)

    cq = sum_mult / float(sum_orig)

    mod = np.array(modified, dtype=np.int32)
    mod **= 2
    sum_mod_2 = np.sum(mod)

    sc = sum_orig_2 / float(sum_mod_2)

    return (md, ad, nad, mse, nmse, lp, snr, psnr, af, nc, cq, sc)







