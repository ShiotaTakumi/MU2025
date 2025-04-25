CC      = g++-14
CFLAGS  = -O3 -std=c++17
TARGET  = a.out
SRCS    = main.cpp
# DEPS    = 
OBJS    = $(SRCS:.cpp=.o)
INCDIR  = -I./../../lib/TdZdd/include -I./../../lib/frontier_basic_tdzdd

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.cpp # $(DEPS)
	$(CC) $(CFLAGS) $(INCDIR) -c $< -o $@

clean:
	rm -f a.out $(OBJS) $(TARGET)
