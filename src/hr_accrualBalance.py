#!/usr/bin/env python2
# coding=cp1251
import sys
from datetime import datetime
from datetime import timedelta
from dbfpy import dbf
from Dictionary import Dictionary
from AccrualBalance import AccrualBalance


def hr_accrualBalance(src_path, dst_path, dictionary):
    dst_file = dst_path + 'hr_accrualBalance.csv'
    try:
        f = open(dst_file, 'w+')
        entity = AccrualBalance()
        entity.write_header(f)
        _read_DBF(src_path + 'RL.DBF', entity, f, dictionary)
    except:
        print 'Error making ', dst_file, sys.exc_info()

class Balance:
    def __init__(self):
        self.balance = {}

    def set(self, key, val):
        self.balance[key] = val

    def get(self, key):
        try:
            return self.balance[key]
        except:
            return (0,0)

    def write(self, f, dictionary):
        entity = AccrualBalance()
        for k, v  in self.balance:
            try:
                entity.employeeNumberID = k
                entity.periodCalc = v
                entity.sumFrom, entity.sumTo = self.get((k,v))
                entity.ID += 1
                entity.dictFundSourceID = dictionary.getDictFundSourceID('1')
                entity.write_record(f)
            except:
                print 'Error accrual balance tabNum:', entity.employeeNumberID, sys.exc_info()[1]


def _read_DBF(src_file, entity, f, dictionary):
    dataset = dbf.Dbf(src_file)
    balance = Balance()
    for record in dataset:
        if (dictionary.isSkipEmployee(record['TN'])):
            continue
        if (record['UP'] is not None and record['UP'] < dictionary.arcMinDate):
            continue
        if (record['CD'] == '���������������'):
            try:
                employeeNumberID = record['TN']
                periodCalc = record['UP']
                sumFrom, sumTo = balance.get((employeeNumberID, periodCalc))
                sumFrom = record['SM']
                balance.set((employeeNumberID, periodCalc), (sumFrom, sumTo))
                prevPeriodCalc = (periodCalc + timedelta(days=-1)).replace(day=1)
                sumFrom, sumTo = balance.get((employeeNumberID, prevPeriodCalc))
                sumTo = record['SM']
                balance.set((employeeNumberID, prevPeriodCalc), (sumFrom, sumTo))
            except:
                print 'Error accrual balance tabNum:', record['TN'], sys.exc_info()[1]
    dataset.close()
    balance.write(f, dictionary)
