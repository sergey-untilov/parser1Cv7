#!/usr/bin/env python2
import sys
from datetime import datetime
import re
from dbfpy import dbf


def hr_employeePosition(src_path, dst_path):
    dst_file = dst_path + 'hr_employeePosition.csv'
    try:
        dataset = dbf.Dbf(src_path + 'PRK.DBF')
        f = open(dst_file, 'w+')
        f.write('ID;employeeID;taxCode;tabNum;employeeNumberID;departmentID;positionID;dateFrom;dateTo;changeDateTo;workScheduleID;workerType;mtCount' +
            ';description;dictRankID;dictStaffCatID;payElID;accrualSum;raiseSalary;isIndex;isActive;workPlace;dictFundSourceID;dictCategoryECBID;accountID\r\n')
        ID = 0
        for record in dataset:
            ID += 1
            employeeID = record['TN']
            taxCode = ''
            tabNum = record['TN']
            employeeNumberID = record['TN']
            departmentID = record['PDR']
            positionID = record['DOL'] > 0 and str(record['DOL']) or ''
            dateFrom = record['BEG'] and record['BEG'] or ''
            dateTo = ''
            changeDateTo = ''
            workScheduleID = ''
            workerType = ''
            mtCount = str(record['STV'])
            description = ''
            dictRankID = record['RAN'] > 0 and str(record['RAN']) or ''
            dictStaffCatID = re.sub('^0*', '', record['KAD'])
            payElID = ''
            accrualSum = record['OKL']
            raiseSalary = ''
            isIndex = ''
            isActive = ''
            workPlace = ''
            dictFundSourceID = ''
            dictCategoryECBID = ''
            accountID = ''
            f.write('%d,%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\r\n' % 
                (ID,employeeID,taxCode,tabNum,employeeNumberID,departmentID,positionID,dateFrom,dateTo,changeDateTo,workScheduleID,workerType,mtCount,
                    description,dictRankID,dictStaffCatID,payElID,accrualSum,raiseSalary,isIndex,isActive,workPlace,dictFundSourceID,dictCategoryECBID,accountID))
        dataset.close()
    except:
        print 'Error making ', dst_file, sys.exc_info()[1]
