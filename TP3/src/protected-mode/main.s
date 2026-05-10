.code16
.global _start

_start:
    cli  # Disable interrupts

     # Set up the GDT (Global Descriptor Table)
    xor %ax, %ax
    mov %ax, %ds

    # =======================================
    # Load the GDT
    # =======================================
    lgdt gdt_descriptor

    # =======================================
    # Enable protected mode
    # =======================================
    mov %cr0, %eax
    or $0x1, %eax  # Set the PE (Protection Enable) bit
    mov %eax, %cr0

    # =======================================
    # Far jump to flush the instruction pipeline and switch to protected mode
    ljmp $0x08, $protected_mode_entry

# =======================================
# Protected mode entry point
# =======================================
.code32
protected_mode_entry:
    # Set up segment registers
    mov $0x10, %ax  # Data segment selector
    mov %ax, %ds
    mov %ax, %ss
    mov %ax, %es
    mov %ax, %fs
    mov %ax, %gs

    # set up the stack
    mov $0x90000, %esp  # Set the stack pointer to a safe location

    # =======================================
    # Access memory in protected mode to verify it's working
    # =======================================
    movl $0x12345678, data_var

hang:
    hlt  # Halt the CPU
    jmp hang  


# =======================================
# Data section
# =======================================
.align 4
data_var: .long 0x0

# =======================================
# GDT (Global Descriptor Table) setup
# =======================================
.align 8
gdt:
    # Null descriptor
    .quad 0x0000000000000000

    # =======================================
    # CODE SEGMENT
    # base = 0x00000000
    # limit = 4GB
    # executable + readable
    # =======================================
    .quad 0x00CF9A000000FFFF

    # =======================================
    # DATA SEGMENT
    # base = 0x00100000
    # limit = 4GB
    # read-only
    # =======================================
    .quad 0x004F90001000FFFF

gdt_end:

gdt_descriptor:
    .word gdt_end - gdt - 1  # Limit (size of GDT - 1)
    .long gdt                # Base address of the GDT
