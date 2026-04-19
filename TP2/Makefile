# ==============================
# CONFIG
# ==============================

CC = gcc
CFLAGS = -Wall -Wextra -O0 -g
ASFLAGS = --64 -g

TARGET = c/program

SRC_C = c/main_i2.c c/file_reader.c
SRC_ASM = c/process_value.s

OBJ = c/main_i2.o c/file_reader.o c/process_value.o

DATA_FILE = data/gini_values.txt

# ==============================
# DEFAULT
# ==============================

all: run

# ==============================
# DATA GENERATION
# ==============================

$(DATA_FILE):
	@echo "Generating data file..."
	python3 python/data_formatter.py

# ==============================
# COMPILATION
# ==============================

c/main_i2.o: c/main_i2.c
	$(CC) $(CFLAGS) -c $< -o $@

c/file_reader.o: c/file_reader.c
	$(CC) $(CFLAGS) -c $< -o $@

c/process_value.o: c/process_value.s
	as $(ASFLAGS) -o $@ $<

# ==============================
# LINKING
# ==============================

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $(OBJ)

# ==============================
# RUN
# ==============================

run: $(DATA_FILE) $(TARGET)
	@echo "Running program..."
	./$(TARGET)

# ==============================
# DEBUG
# ==============================

debug: $(DATA_FILE) $(TARGET)
	gdb ./$(TARGET)

# ==============================
# CLEAN
# ==============================

clean:
	rm -f c/*.o $(TARGET)