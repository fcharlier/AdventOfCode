#!/usr/bin/python


buf = [0]
step = 380
pos = 0

for n in xrange(1, 2018):
    pos = (pos + step) % n + 1
    buf.insert(pos, n)

print "Buffer is %d values long" % len(buf)
print buf[(buf.index(2017) + 1) % len(buf)]

pos = 0
pos1 = 0
for n in xrange(1, 50000001):
    pos = (pos + step) % n + 1
    if pos == 1:
        pos1 = n
print "After too much iterations, value after 0 (index 1) is %d" % pos1
