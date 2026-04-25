.code16
.global _start

_start:
    cli  # Disable interrupts

     # Set up the GDT (Global Descriptor Table)
    xor %ax, %ax
    mov %ax, %ds

hang:
    hlt  # Halt the CPU
    jmp hang  
