#coding:utf-8

with open('log', 'r') as log_f:
    log = log_f.read().replace(' ', ',').split('\n')

with open('log.csv', 'w') as out:
    for l in log:
        l = l.replace(':','')
        out.write(l)
        out.write('\r\n')
