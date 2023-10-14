import sys
import timeit

try:
  with open("example11.txt", 'r') as f:
    flag = True
    sequence = []
    current_seq = ""
    for line in f:
      if line.startswith('>'):
        flag = False
        # > 를 한번 더 만날 때 까지 sequence 를 받기 때문에 현재까지의 문자열을 리스트에 추가
        if current_seq:
          sequence.append(current_seq.strip().replace('\n', ''))
          current_seq = ""
        continue
      # Correct format check
      # 이 코드는 txt 파일의 가장 처음 시작 문자가 >가 아닌 경우에만 실행 되는 코드이다
      if flag:
        if not line.startswith('>'):
          print("No correct format")
          sys.exit(0)
      else :
        line = line.replace("\n","").replace(" ","").replace("\t","").upper()
        # 하나의 sequence가 \n을 기준으로 여러 문장으로 돼 있을 경우를 대비 하여 바로 리스트에 추가하지 않고 문자열 변수에 넣는다.
        current_seq += line

    # 마지막 > 의 경우 > 를 만나지 않고 반복문이 종료 되기 때문에 리스트에 추가하기 위한 조건문을 써주어야 한다.
    if current_seq:
      sequence.append(current_seq.strip().replace('\n', ''))

except FileNotFoundError:
  print("No input file")
  sys.exit(0)

print(sequence)

# f가 빈 값인 경우 for lie in f 반복문은 실행 되지 않는다.
# txt 파일이 비어있을 경우
if len(sequence) == 0:
  print("No DNA sequence")
  sys.exit(0)

if len(sequence) == 1:
  print('Need more sequences')
  sys.exit(0)

# ATGC 로만 이루어진 STR 인지 확인 하는 함수
def check_dna(sequence_list):
  allowed_chars = set(['A','T','G','C'])
  for seq in sequence_list:
    # seq 와 allowed_chars 는 대문자인지 소문자인지 일치 시켜야 한다
    # seq 가 atgc 만을 포함 하고 있으면 해당 조건문은 0 이 되어서 조건문을 실행 시키지 않는다.
    if (set(seq) - allowed_chars):
      print(set(seq) - allowed_chars)
      print("No DNA sequence")
      sys.exit(0)

check_dna(sequence)


def anti_monotonic_algorithm(strings):
  # 문자열의 길이를 구함
  n = len(strings[0])

  # 문자열의 길이에 따라 모든 가능한 패턴 길이를 확인
  patterns = []
  max_length = 0

  for length in range(n, 0, -1):
    # 문자열의 모든 가능한 시작 인덱스를 확인
    for start in range(n - length + 1):
      pattern = strings[0][start:start + length]
      is_anti_monotonic = True

      # 나머지 문자열에서 패턴이 증가하는지 감소하는지 확인
      for s in strings[1:]:
        if pattern in s:
          # 패턴이 증가하는 경우
          if s.index(pattern) < s.rindex(pattern):
            is_anti_monotonic = False
            break
        else:
          is_anti_monotonic = False
          break

      # Anti-monotonic 패턴이면 결과 저장
      if is_anti_monotonic:
        patterns.append(pattern)
        max_length = max(max_length, length)

  # 저장된 패턴들 반환
  return [pattern for pattern in patterns if len(pattern) == max_length]


# 주어진 문자열 777
x1 = 'cctgatagacgctatctggctatccacgtacgtaggtcctctgtgcgaatctatgcgtttccaaccatgtagt'
x2 = 'agtactggtgtacatttgatacgtacgtacaccggcaacctgaaacaaacgctcagaaccagaagtagtgc'
x3 = 'aaacgtacgtgcaccctctttcttcgtgtagtgctctggccaacgagggctgatgtataagacgaaaatttt'
#
# x1 = 'cctgatagacgctatctggctatccaggtcctctgtgcgaatctatgcgtttccaaccatacgtacgt'
# x2 = 'agtacgtacgtactggtgtacatttgatacaccggcaacctgaaacaaacgctcagaaccagaagtgc'
# x3 = 'aaacgtacgtgcaccctctttcttcgtggctctggccaacgagggctgatgtataagacgaaaatttt'

# # 2 이하의 패턴
# x1 = 'cctgatagacgctatctggctatccacacacacaggtcctctgtgcgaatctatgcgtttccaaccat'
# x2 = 'agtactggtgtacatttgatacacacacacaccggcaacctgaaacaaacgctcagaaccagaagtgc'
# x3 = 'aacacacacgcaccctctttcttcgtggctctggccaacgagggctgatgtataagacgaaaatttt'


# Anti-monotonic 알고리즘 실행
start = timeit.default_timer()
result = anti_monotonic_algorithm(sequence)
end = timeit.default_timer()

print('{0} millisec'.format((end - start) * 1000))


print(result)  # 'actgactg' 출력

if len(result) == 0:
  print("No pattern found")
  sys.exit(0)


with open("output.txt", 'w') as f2:
  for re in result:
    f2.write("Pattern : {0}\n".format(re))





