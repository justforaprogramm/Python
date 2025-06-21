x = 7
print(x//2)
# int division 
print((x / 2) if (x % 2) == 0 else int((x - 1) / 2))
# dividiion 

# int division 
#   0           RESUME                   0

#   1           LOAD_NAME                0 (print)
#               PUSH_NULL
#               LOAD_NAME                1 (x)
#               LOAD_CONST               0 (2)
#               BINARY_OP                2 (//)
#               CALL                     1
#               POP_TOP
#               RETURN_CONST             1 (None)

# dividiion 
#   0           RESUME                   0

#   1           LOAD_NAME                0 (print)
#               PUSH_NULL
#               LOAD_NAME                1 (x)
#               LOAD_CONST               0 (2)
#               BINARY_OP                6 (%)
#               LOAD_CONST               1 (0)
#               COMPARE_OP              88 (bool(==))
#               POP_JUMP_IF_FALSE       10 (to L1)
#               LOAD_NAME                1 (x)
#               LOAD_CONST               0 (2)
#               BINARY_OP               11 (/)
#               CALL                     1
#               POP_TOP
#               RETURN_CONST             3 (None)
#       L1:     LOAD_NAME                2 (int)
#               PUSH_NULL
#               LOAD_NAME                1 (x)
#               LOAD_CONST               2 (1)
#               BINARY_OP               10 (-)
#               LOAD_CONST               0 (2)
#               BINARY_OP               11 (/)
#               CALL                     1
#               CALL                     1
#               POP_TOP
#               RETURN_CONST             3 (None)