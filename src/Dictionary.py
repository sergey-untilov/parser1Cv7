#!/usr/bin/env python2
import sys
from src.PayEl import PayEl
from src.PayFund import PayFund
from sets import Set
from datetime import datetime


ARC_SIZE_YEAR = 1


class Dictionary:
    def __init__(self, src_path, dst_path):
        self.TaxCode = {}
        self.PayElID = {}
        self.PayFundID = {}
        self.DepartmentID = {}
        self.DictPositionName = {}
        self.PayElCode = Set()
        self.AccrualSize = {}
        self.SkipEmployee = Set()
        self.error_count = 0
        self.src_path = src_path
        self.dst_path = dst_path
        self.arcMinDate = datetime.date(datetime.now().replace(year= datetime.now().year - ARC_SIZE_YEAR, month=1, day=1))
        self.DictFundSourceID = {}
        print('Minimal arc date is %s\n' % self.arcMinDate)

    def setDictFundSourceID(self, code, id):
        self.DictFundSourceID[code] = id

    def getDictFundSourceID(self, code):
        try:
            return self.DictFundSourceID[code] and self.DictFundSourceID[code] or 1
        except:
            self.DictFundSourceID[code] = 1
            return 1

    def addAccrualSize(self, tabNum):
        self.AccrualSize[tabNum] = 1

    def getAccrualSize(self, tabNum):
        try:
            return self.AccrualSize[tabNum] and self.AccrualSize[tabNum] or 0
        except:
            self.AccrualSize[tabNum] = 0
            return 0

    def setSkipEmployee(self, tabNum):
        if (tabNum not in self.SkipEmployee):
            self.SkipEmployee.add(tabNum)

    def isSkipEmployee(self, tabNum):
        return (tabNum in self.SkipEmployee)

    def setPayElCode(self, code): 
        if (code not in self.PayElCode):
            self.PayElCode.add(code)

    def getPayElCode(self, code): 
        return (code in self.PayElCode)

    def set_DepartmentID(self, code, ID):
        self.DepartmentID[code] = ID

    def get_DepartmentID(self, code):
        try:
            return self.DepartmentID[code] and self.DepartmentID[code] or ''
        except:
            self.error_count += 1
            print 'Error [' + str(self.error_count) + ']. Not found Department code: ' + code + '.'
            return ''

    def set_DictPositionName(self, code, name):
        self.DictPositionName[code] = name

    def get_DictPositionName(self, code):
        try:
            return self.DictPositionName[code] and self.DictPositionName[code] or ''
        except:
            self.error_count += 1
            print 'Error [' + str(self.error_count) + ']. Not found dictPosition code: ' + code + '.'
            return ''


    def set_TaxCode(self, tabNum, taxCode):
        self.TaxCode[tabNum] = taxCode

    def get_TaxCode(self, tabNum):
        try:
            return self.TaxCode[tabNum] and self.TaxCode[tabNum] or ''
        except:
            self.error_count += 1
            print 'Error [' + str(self.error_count) + ']. Not found tabNum: ' + tabNum + '.'
            return ''

    def set_PayElID(self, cd, payElID):
        self.PayElID[cd] = payElID

    def get_PayElID(self, code):
        try:
            return self.PayElID[code] and self.PayElID[code] or 0
        except:
            ID = len(self.PayElID) + 1                    
            ID = _append_hr_payEl(ID, code, code, self.src_path, self.dst_path)
            if (ID == 0):
                self.error_count += 1
                print 'Error [' + str(self.error_count) + ']. Not found PayElCd: ' + code + '.'
            else:
                self.set_PayElID(code, ID)
            return ID

    def set_PayFundID(self, cd, payFundID):
        self.PayFundID[cd] = payFundID

    def get_PayFundID(self, code):
        try:
            return self.PayFundID[code] and self.PayFundID[code] or 0
        except:
            ID = len(self.PayFundID) + 1                    
            ID = _append_hr_payFund(ID, code, code, self.src_path, self.dst_path)
            if (ID == 0):
                self.error_count += 1
                print 'Error [' + str(self.error_count) + ']. Not found PayFundCd: ' + code + '.'
            else:
                self.set_PayFundID(code, ID)
            return ID


def _append_hr_payEl(ID, code, name, src_path, dst_path):
    dst_file = dst_path + 'hr_payEl.csv'
    try:
        f = open(dst_file, 'a+')
        payEl = PayEl()
        payEl.ID = ID
        payEl.code = code[:32]
        payEl.name = name
        payEl.description = name + '(' + code + ')'
        payEl.write_record(f)
        print 'Append', dst_file, ID, code, name
        return ID
    except:
        print 'Not added', dst_file, sys.exc_info()[1]
        return 0


def _append_hr_payFund(ID, code, name, src_path, dst_path):
    dst_file = dst_path + 'hr_payFund.csv'
    try:
        f = open(dst_file, 'a+')
        payFund = PayFund()
        payFund.ID = ID
        payFund.code = code[:32]
        payFund.name = name
        payFund.description = name + '(' + code + ')'
        payFund.write_record(f)
        print 'Append', dst_file, ID, code, name
        return ID
    except:
        print 'Not added', dst_file, sys.exc_info()[1]
        return 0
