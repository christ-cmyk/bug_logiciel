p = 'server.py'
lines = open(p).readlines()
out = []
for i, l in enumerate(lines):
    if '@app.route' in l and 'logout' in l:
        j = i - 1
        blanks = 0
        while j >= 0 and lines[j].strip() == '':
            blanks += 1
            j -= 1
        while blanks < 3:
            out.append('\n')
            blanks += 1
    out.append(l)
open(p, 'w').write(''.join(out))
# conftest
p2 = 'tests/conftest.py'
t = open(p2).read().rstrip() + '\n'
open(p2, 'w').write(t)
print('ok')
