SECTIONS{
    . = 0x7C00;

    .text :
    {
        *(.text)
        . = 0x1FE;
        SHORT(0xAA55)
    }
}