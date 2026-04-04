    .global process_value_asm
    .text

process_value_asm:
    cvttss2si %xmm0, %eax
    add $1, %eax
    ret
